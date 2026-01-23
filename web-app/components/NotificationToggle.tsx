'use client';

import { useState, useEffect } from 'react';

interface Props {
  jobId: string;
  processingStartTime: number; // timestamp when processing started
}

export default function NotificationToggle({ jobId, processingStartTime }: Props) {
  const [showToggle, setShowToggle] = useState(false);
  const [enabled, setEnabled] = useState(false);
  const [needsPermission, setNeedsPermission] = useState(false);
  const [permissionDenied, setPermissionDenied] = useState(false);

  useEffect(() => {
    // Check if notifications are supported
    if (!('Notification' in window) || !('serviceWorker' in navigator)) {
      return;
    }

    // Show toggle after 5-8 seconds of processing
    const delay = 5000 + Math.random() * 3000; // 5-8 seconds
    const timer = setTimeout(() => {
      setShowToggle(true);
    }, delay);

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    // Check current permission state
    if ('Notification' in window) {
      const permission = Notification.permission;
      setPermissionDenied(permission === 'denied');
    }
  }, []);

  const handleToggle = async () => {
    if (!('Notification' in window) || !('serviceWorker' in navigator)) {
      return;
    }

    if (permissionDenied) {
      // Silently fail if permission denied
      return;
    }

    if (enabled) {
      // Disable notifications
      setEnabled(false);
      setNeedsPermission(false);
      localStorage.removeItem(`notify-${jobId}`);
      return;
    }

    // Check permission
    if (Notification.permission === 'granted') {
      // Already granted, subscribe immediately
      await subscribeToNotifications();
    } else if (Notification.permission === 'default') {
      // Show enable button
      setNeedsPermission(true);
      localStorage.setItem(`notify-${jobId}`, 'pending');
    }
  };

  const handleEnablePermission = async () => {
    if (!('Notification' in window)) {
      return;
    }

    try {
      const permission = await Notification.requestPermission();

      if (permission === 'granted') {
        await subscribeToNotifications();
        setNeedsPermission(false);
      } else if (permission === 'denied') {
        setPermissionDenied(true);
        setNeedsPermission(false);
        setEnabled(false);
        localStorage.removeItem(`notify-${jobId}`);
      }
    } catch (error) {
      console.error('Failed to request notification permission:', error);
      setNeedsPermission(false);
    }
  };

  const subscribeToNotifications = async () => {
    try {
      const registration = await navigator.serviceWorker.ready;

      // Get VAPID public key
      const vapidPublicKey = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY;
      if (!vapidPublicKey) {
        console.error('VAPID public key not configured');
        return;
      }

      // Subscribe to push notifications
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(vapidPublicKey),
      });

      // Send subscription to server
      await fetch('/api/notify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'subscribe',
          jobId,
          subscription: subscription.toJSON(),
        }),
      });

      setEnabled(true);
      localStorage.setItem(`notify-${jobId}`, 'enabled');
    } catch (error) {
      console.error('Failed to subscribe to notifications:', error);
      setEnabled(false);
    }
  };

  // Don't show if not supported or permission denied
  if (!showToggle || permissionDenied) {
    return null;
  }

  return (
    <div className="mt-4 p-3 bg-dawt-background rounded-lg border border-dawt-divider">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-[13px] font-medium text-dawt-text-primary">
            Notify me when it's ready
          </p>
          <p className="text-[11px] text-dawt-text-secondary mt-0.5">
            One alert. No spam.
          </p>
        </div>
        <button
          onClick={handleToggle}
          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
            enabled ? 'bg-dawt-accent' : 'bg-gray-300'
          }`}
          aria-label="Toggle notifications"
        >
          <span
            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
              enabled ? 'translate-x-6' : 'translate-x-1'
            }`}
          />
        </button>
      </div>

      {needsPermission && (
        <button
          onClick={handleEnablePermission}
          className="mt-3 w-full py-2 px-3 text-[13px] font-medium text-dawt-accent bg-dawt-card border border-dawt-accent rounded-lg hover:bg-gray-50 transition-colors"
        >
          Enable notifications
        </button>
      )}
    </div>
  );
}

// Helper function to convert VAPID key
function urlBase64ToUint8Array(base64String: string): Uint8Array {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/\-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}
