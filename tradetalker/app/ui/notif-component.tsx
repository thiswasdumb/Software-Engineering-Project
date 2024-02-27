'use client';
import { useRouter } from 'next/navigation';
import React, { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';

export default function NotifComponent({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [data, setData] = useState<any[]>([]);
  const router = useRouter();

  useEffect(() => {
    if (isLoggedIn) {
      fetch('/api/get_notifications')
        .then((response) => response.json())
        .then((data) => {
          setData(data);
        })
        .catch(() => {
          toast.error('Error fetching notification data.');
        });
    } else {
      router.push('/login');
      toast.error('You must be logged in.');
    }
  }, [setData, isLoggedIn, router]);

  return (
    isLoggedIn && (
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='text-2xl'>Notifications</div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <div>
          {data.length === 0 && <p>No notifications.</p>}
          {data.length > 0 &&
            data.map((notif, index) => (
              <div
                className='m-4 overflow-scroll rounded-lg bg-slate-100 p-2'
                key={index}
              >
                <p>Timestamp: {notif.Time}</p>
                <p>Message: {notif.Content}</p>
              </div>
            ))}
        </div>
      </div>
    )
  );
}
