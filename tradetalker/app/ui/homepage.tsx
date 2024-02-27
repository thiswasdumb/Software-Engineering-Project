'use client';
import React, { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { toast } from 'react-hot-toast';

export default function HomeComponent() {
  // Showing how to fetch data from the backend
  const [data, setData] = useState<any[]>([]);
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    fetch('/api/example')
      .then((response) => response.json())
      .then((data) => {
        setData(data);
      });
  }, [setData]);

  useEffect(() => {
    const error = searchParams.get('error');
    const success = searchParams.get('success');
    if (error) {
      toast.error(error);
    }
    if (success) {
      toast.success(success);
    }
    router.replace('/', undefined);
    router.refresh();
  }, [router, searchParams]);

  return (
    <>
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='text-2xl'>Welcome to TradeTalker.</div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <p>
          Stay informed about the latest news sentiment in the financial
          markets.
        </p>
        <br></br>
        <p>Below should show all users in the database.</p>
        <div className='rounded-lg bg-slate-300 p-4'>
          {data.map((user, index) => (
            <div
              className='m-4 overflow-scroll rounded-lg bg-slate-100 p-2'
              key={index}
            >
              <p>User ID: {user.id}</p>
              <p>Username: {user.Username}</p>
              <p>Password: {user.Password}</p>
              <p>Email: {user.Email}</p>
              <p>Preferences: {user.Preferences}</p>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
