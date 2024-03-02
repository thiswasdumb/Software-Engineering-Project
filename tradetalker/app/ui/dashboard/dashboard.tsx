'use client';
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';

export default function DashboardComponent({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [data, setData] = useState('');
  const router = useRouter();
  useEffect(() => {
    if (isLoggedIn) {
      fetch('/api/get_dashboard_data')
        .then((response) => response.json())
        .then((data) => {
          if (data.username) {
            setData(data.username);
          }
        })
        .catch(() => {
          toast.error('Error fetching user data.');
        });
    } else {
      router.push('/login');
      toast.error('You must be logged in.');
    }
  }, [data, isLoggedIn, router]);

  return (
    isLoggedIn && (
      <div>
        <div className='m-8 rounded-lg bg-slate-200 p-8'>
          <div className='text-2xl'>Dashboard</div>
          <hr className='my-2 rounded-lg border-2 border-slate-400' />
          <div>
            <div className='text-xl'>Hi, {data}.</div>
          </div>
        </div>
      </div>
    )
  );
}
