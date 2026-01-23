# Web Push Notifications

Non-annoying "Notify me when ready" feature for DAWT-Transcribe web app.

## UX Principles

✅ **No permission prompt on load** - Users are never nagged on page load
✅ **Inline toggle after 5-8s** - Appears naturally during processing
✅ **One alert per job** - No spam, just useful completion notifications
✅ **Silent fallback** - If permission denied, no nagging or error messages
✅ **Auto-cleanup** - Subscriptions cleared after sending to prevent repeats

## Architecture

### 1. Service Worker (`public/sw.js`)
- Handles push events and shows notifications
- Handles notification clicks (focuses existing window or opens new one)
- Already integrated with PWA caching system

### 2. API Route (`app/api/notify/route.ts`)
- **POST /api/notify** with `action: 'subscribe'` - Stores subscription for jobId
- **POST /api/notify** with `action: 'notify'` - Sends notification and clears subscription
- Uses in-memory Map for storage (jobId → subscription)
- Production should use Redis or database for multi-instance support

### 3. UI Component (`components/NotificationToggle.tsx`)
- Appears after 5-8 seconds of processing (randomized delay)
- Toggle switch for enabling notifications
- "Enable notifications" button shown if permission needed
- Stores preference in localStorage per job
- Silently hides if notifications not supported or permission denied

### 4. Notification Utils (`lib/notifications.ts`)
- `generateJobId()` - Creates unique job identifier
- `sendCompletionNotification(jobId)` - Triggers notification via API
- `clearNotificationPreference(jobId)` - Cleans up localStorage
- `isNotificationSupported()` - Feature detection
- `getNotificationPermission()` - Check current permission state

## Setup

### 1. Install Dependencies

```bash
npm install web-push
```

### 2. Generate VAPID Keys

```bash
npx web-push generate-vapid-keys
```

### 3. Configure Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_VAPID_PUBLIC_KEY=your_public_key_here
VAPID_PRIVATE_KEY=your_private_key_here
```

### 4. Add to Vercel Environment Variables

In your Vercel project settings, add:
- `NEXT_PUBLIC_VAPID_PUBLIC_KEY` (public key from step 2)
- `VAPID_PRIVATE_KEY` (private key from step 2)

## Usage Flow

1. User starts transcription (record/upload/URL)
2. After 5-8 seconds, notification toggle appears with microcopy
3. User toggles ON → subscribe to push notifications for this job
4. If permission not granted → "Enable notifications" button appears
5. User clicks button → browser shows permission prompt (one-time)
6. If granted → subscription stored on server (jobId → subscription mapping)
7. Transcription completes → server sends push notification
8. Notification shown → subscription cleared (no repeat notifications)

## Storage Strategy

**Development/Single Instance:**
- In-memory Map in API route (current implementation)
- Simple, no external dependencies
- Cleared on server restart

**Production/Multi-Instance:**
- Use Redis or database to store subscriptions
- Schema: `{ jobId: string, subscription: PushSubscription, createdAt: timestamp }`
- Add TTL/expiry (e.g., 1 hour) to prevent stale subscriptions
- Example with Redis:
  ```typescript
  redis.set(`notify:${jobId}`, JSON.stringify(subscription), 'EX', 3600);
  ```

## Example Redis Implementation

```typescript
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_URL,
  token: process.env.UPSTASH_REDIS_TOKEN,
});

// Subscribe
await redis.set(
  `notify:${jobId}`,
  JSON.stringify(subscription),
  { ex: 3600 } // 1 hour TTL
);

// Notify
const data = await redis.get(`notify:${jobId}`);
if (data) {
  const subscription = JSON.parse(data as string);
  await webpush.sendNotification(subscription, payload);
  await redis.del(`notify:${jobId}`); // Clear after sending
}
```

## Browser Compatibility

- ✅ Chrome 50+
- ✅ Firefox 44+
- ✅ Safari 16+ (iOS 16.4+)
- ✅ Edge 79+
- ❌ Older iOS versions (silent fallback)

## Security Notes

- VAPID keys authenticate push notifications
- Private key NEVER exposed to client
- Public key embedded in client code
- Service worker runs in secure context (HTTPS required)
- Push subscriptions tied to service worker registration

## Testing

### Local Testing

1. Start dev server: `npm run dev`
2. Open browser DevTools → Application → Service Workers
3. Verify service worker registered
4. Start a transcription
5. Wait 5-8 seconds for toggle to appear
6. Enable notifications and grant permission
7. Wait for transcription to complete
8. Notification should appear

### Production Testing

1. Deploy to Vercel with VAPID keys configured
2. Open PWA on phone or desktop
3. Follow same flow as local testing
4. Verify notification appears on completion

## Future Enhancements

- [ ] Add notification sound preference
- [ ] Support multiple job notifications (history/queue)
- [ ] Rich notifications with transcript preview
- [ ] Notification actions (View, Share, Dismiss)
- [ ] Email fallback for unsupported browsers
- [ ] Analytics on notification engagement
