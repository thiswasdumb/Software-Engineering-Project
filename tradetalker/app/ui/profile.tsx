'use client';
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';
import Link from 'next/link';
import { Button } from 'app/ui/button';
import Logout from 'app/ui/logout';

export default function ProfileComponent({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [data, setData] = useState<Record<string, any>>({});
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

  const DeleteUser = async (isLoggedIn: boolean) => {
    if (isLoggedIn) {
      fetch('/api/delete_user', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((response) => response.json())
        .then(() => {
          window.location.href = '/home';
          toast.success('Account deleted successfully.');
        })
        .catch(() => {
          toast.error('Error deleting account.');
        });
    } else {
      window.location.href = '/login';
      toast.error('You must be logged in.');
    }
  };

  return (
    isLoggedIn && (
      <div className='m-8 flex flex-col rounded-lg bg-slate-200 p-8'>
        <div className='text-2xl'>Profile</div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <div>
          <div className='text-xl'>Username: {data.username}</div>
          <div className='text-xl'>Email: {data.email}</div>
        </div>
        <Link href='/api/reset_password'>
          <Button
            type='button'
            className='mt-4 rounded-lg bg-blue-500 p-4 text-white transition hover:bg-blue-600 hover:shadow-lg'
          >
            Reset password
          </Button>
        </Link>
        <div onClick={() => Logout(isLoggedIn)}>
          <button
            type='button'
            className='mt-4 rounded-lg bg-red-500 p-4 text-white transition hover:bg-red-600 hover:shadow-lg active:bg-red-700'
          >
            Log out
          </button>
        </div>
        <div onClick={() => DeleteUser(isLoggedIn)}>
          <button
            type='button'
            className='mt-4 rounded-lg bg-red-500 p-4 text-white transition hover:bg-red-600 hover:shadow-lg active:bg-red-700'
          >
            Delete account
          </button>
        </div>
      </div>
    )
  );
}
