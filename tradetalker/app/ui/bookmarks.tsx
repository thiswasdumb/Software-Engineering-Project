'use client';
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';

export default function BookmarkComponent({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [data, setData] = useState<any[]>([]);
  const router = useRouter();

  useEffect(() => {
    if (isLoggedIn) {
      fetch('/api/get_bookmarks')
        .then((response) => response.json())
        .then((data) => {
          setData(data);
        })
        .catch(() => {
          toast.error('Error fetching bookmarks.');
        });
    } else {
      router.push('/login');
      toast.error('You must be logged in.');
    }
  }, [setData, isLoggedIn, router]);

  return (
    isLoggedIn && (
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='text-2xl'>Bookmarks</div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <div>
          {data.map((bookmark, index) => (
            <div
              className='m-4 overflow-scroll rounded-lg bg-slate-100 p-2'
              key={index}
            >
              <p>Timestamp: {bookmark.Time}</p>
              <p>Message: {bookmark.Content}</p>
            </div>
          ))}
        </div>
      </div>
    )
  );
}
