'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';
import dayjs from 'dayjs';
import LocalizedFormat from 'dayjs/plugin/localizedFormat';

/**
 * Notifications component.
 * @param isLoggedIn - Whether the user is logged in
 * @returns JSX.Element - Notifications component
 */
export default function NotifClientComponent({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [notifs, setNotifs] = useState<any[]>([]);
  const router = useRouter();
  dayjs.extend(LocalizedFormat);

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
      <div className='rounded-lg bg-slate-200 p-8 md:m-8'>
        <h1 className='text-2xl'>Notifications</h1>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        {notifs.length === 0 && <p>No notifications.</p>}
        {notifs.length > 0 &&
          notifs.map((notif, index) => (
            <div className='my-2 rounded-lg bg-slate-300 p-2' key={index}>
              <div className='flex flex-row items-center justify-between'>
                {notif.article_id ? (
                  <Link
                    href={`/article/${notif.article_id}`}
                    className='grow transition hover:drop-shadow-lg'
                  >
                    <p className='text-sm'>
                      {dayjs(notif.time).format('D MMM YYYY LT')}
                    </p>
                    <p className='text-lg'>{notif.content}</p>
                  </Link>
                ) : (
                  <Link
                    href='/stocks'
                    className='grow transition hover:drop-shadow-lg'
                  >
                    <p className='text-sm'>
                      {dayjs(notif.time).format('D MMM YYYY LT')}
                    </p>
                    <p className='text-lg'>{notif.content}</p>
                  </Link>
                )}
                <button
                  type='button'
                  className='float-right m-2 rounded-lg bg-red-500 p-2 text-sm text-white transition hover:bg-red-600 hover:shadow-lg active:bg-red-700'
                  onClick={() => deleteNotification(notif.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
      </div>
    )
  );
}
