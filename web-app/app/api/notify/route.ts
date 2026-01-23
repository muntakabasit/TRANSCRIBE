import { NextRequest, NextResponse } from 'next/server';
import webpush from 'web-push';

// Configure VAPID keys (these should be in environment variables)
const vapidKeys = {
  publicKey: process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY || '',
  privateKey: process.env.VAPID_PRIVATE_KEY || '',
};

if (vapidKeys.publicKey && vapidKeys.privateKey) {
  webpush.setVapidDetails(
    'mailto:support@dawt-transcribe.com',
    vapidKeys.publicKey,
    vapidKeys.privateKey
  );
}

// In-memory storage for subscriptions (jobId → subscription)
// In production, use Redis or a database
const subscriptions = new Map<string, PushSubscription>();

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, jobId, subscription, title, message } = body;

    if (action === 'subscribe') {
      // Store subscription for this job
      if (!jobId || !subscription) {
        return NextResponse.json(
          { error: 'Missing jobId or subscription' },
          { status: 400 }
        );
      }

      subscriptions.set(jobId, subscription);
      return NextResponse.json({ success: true });
    }

    if (action === 'notify') {
      // Send notification for completed job
      if (!jobId) {
        return NextResponse.json(
          { error: 'Missing jobId' },
          { status: 400 }
        );
      }

      const subscription = subscriptions.get(jobId);
      if (!subscription) {
        // No subscription for this job (user didn't opt in)
        return NextResponse.json({ success: true, skipped: true });
      }

      // Send push notification
      const payload = JSON.stringify({
        title: title || 'Transcription Complete',
        body: message || 'Your transcription is ready!',
        url: '/',
      });

      try {
        await webpush.sendNotification(subscription, payload);

        // Clear subscription after sending (one notification per job)
        subscriptions.delete(jobId);

        return NextResponse.json({ success: true, sent: true });
      } catch (error) {
        console.error('Failed to send push notification:', error);

        // Clean up failed subscription
        subscriptions.delete(jobId);

        return NextResponse.json({ success: true, failed: true });
      }
    }

    return NextResponse.json(
      { error: 'Invalid action' },
      { status: 400 }
    );
  } catch (error) {
    console.error('Notification API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
