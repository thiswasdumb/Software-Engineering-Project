'use client';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';

export default function NotifClientComponent({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [notifs, setNotifs] = useState<any[]>([]);
  const router = useRouter();

  useEffect(() => {
    if (isLoggedIn) {
      const fetchNotifications = async () => {
        try {
          const response = await fetch('/api/get_notifications', {
            credentials: 'include',
          });
          const data = await response.json();
          setNotifs(data);
        } catch (error) {
          toast.error('Error fetching notifications.');
        }
      };
      fetchNotifications();
    } else {
      router.push('/login');
      toast.error('You must be logged in.');
    }
  }, [isLoggedIn, setNotifs, router]);

  const deleteNotification = async (id: string) => {
    try {
      const response = await fetch(`/api/delete_notification/${id}`);
      const message = await response.json();
      if (message.success) {
        const updatedNotifs = notifs.filter((notif) => notif.id !== id);
        setNotifs(updatedNotifs);
        toast.success('Notification deleted.');
      } else {
        toast.error('Error deleting notification.');
      }
    } catch (error) {
      toast.error('Error deleting notification.');
    }
  };

  return (
    isLoggedIn && (
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='text-2xl'>Notifications</div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        {notifs.length === 0 && <p>No notifications.</p>}
        {notifs.length > 0 && (
          <div className='rounded-lg bg-slate-300 p-2'>
            {notifs.map((notif, index) => (
              <div className='flex flex-row justify-between' key={index}>
                <Link
                  href={`/article/${notif.article_id}`}
                  className='grow transition hover:drop-shadow-lg'
                >
                  <div className='text-sm'>
                    {formatNotificationTime(notif.time)}
                  </div>
                  <div className='text-lg'>{notif.content}</div>
                </Link>
                <button
                  type='button'
                  className='float-right m-2 rounded-lg bg-red-500 p-2 text-sm text-white transition hover:bg-red-600 hover:shadow-lg active:bg-red-700'
                  onClick={() => deleteNotification(notif.id)}
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    )
  );
}

function formatNotificationTime(time: string) {
  const date = new Date(time);
  return date.toLocaleString();
}
