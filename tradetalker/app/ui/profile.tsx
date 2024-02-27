'use client';
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';

export default function ProfileComponent({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [data, setData] = useState<any[]>([]);
  const router = useRouter();

  useEffect(() => {
    if (isLoggedIn) {
      fetch('/api/get_profile_data')
        .then((response) => response.json())
        .then((data) => {
          setData(data);
        })
        .catch(() => {
          toast.error('Error fetching profile data.');
        });
    } else {
      router.push('/login');
      toast.error('You must be logged in.');
    }
  }, [setData, isLoggedIn, router]);

  return (
    isLoggedIn && (
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='text-2xl'>Profile</div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <div>
          <div className='text-xl'>{data}</div>
        </div>
        <a href='/api/logout'>
          <button
            type='button'
            className='mt-4 rounded-lg bg-red-600 p-4 text-white transition hover:bg-red-700'
          >
            Log out
          </button>
        </a>
      </div>
    )
  );
}
