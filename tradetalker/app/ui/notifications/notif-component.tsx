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
    console.log(isLoggedIn);
    if (isLoggedIn) {
      const fetchNotifications = async () => {
        try {
          const response = await fetch(
            'http://localhost:8080/api/get_notifications',
            { credentials: 'include' }
          );
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
      <div className='bg-slate-200 m-8 rounded-lg p-8'>
        <div className='text-2xl'>Notifications</div>
        <hr className='border-slate-400 my-2 rounded-lg border-2' />
        {notifs.length === 0 && <p>No notifications.</p>}
        {notifs.length > 0 && (
          <div className='bg-slate-300 rounded-lg p-2'>
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
                  className='bg-red-500 text-white hover:bg-red-600 active:bg-red-700 float-right m-2 rounded-lg p-2 text-sm transition hover:shadow-lg'
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
