// Notification management utilities

export function generateJobId(): string {
  return `job-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

export async function sendCompletionNotification(jobId: string): Promise<void> {
  try {
    await fetch('/api/notify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'notify',
        jobId,
        title: 'Transcription Complete ✓',
        message: 'Your transcription is ready!',
      }),
    });
  } catch (error) {
    console.error('Failed to send completion notification:', error);
    // Silently fail - don't disrupt user experience
  }
}

export function clearNotificationPreference(jobId: string): void {
  localStorage.removeItem(`notify-${jobId}`);
}

export function isNotificationSupported(): boolean {
  return (
    typeof window !== 'undefined' &&
    'Notification' in window &&
    'serviceWorker' in navigator &&
    'PushManager' in window
  );
}

export function getNotificationPermission(): NotificationPermission | null {
  if (!isNotificationSupported()) {
    return null;
  }
  return Notification.permission;
}
