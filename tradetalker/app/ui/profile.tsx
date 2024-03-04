'use client';
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';
import Link from 'next/link';
import { Button } from 'app/ui/button';
import Logout from 'app/ui/logout';
import { XMarkIcon } from '@heroicons/react/20/solid';

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
        <DeleteUserModal isLoggedIn={isLoggedIn} />
      </div>
    )
  );
}

export function DeleteUserModal({ isLoggedIn }: { isLoggedIn: boolean }) {
  const [showModal, setShowModal] = React.useState(false);

  const DeleteUser = async (isLoggedIn: boolean) => {
    if (isLoggedIn) {
      fetch('/api/delete_user', {
        headers: {
          'Content-Type': 'application/json',
          credentials: 'include',
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
    <>
      <div onClick={() => setShowModal(true)}>
        <button
          type='button'
          className='mt-4 rounded-lg bg-red-500 p-4 text-white transition hover:bg-red-600 hover:shadow-lg active:bg-red-700'
        >
          Delete account
        </button>
      </div>
      {showModal ? (
        <>
          <div className='fixed inset-0 z-50 mx-2 flex items-center justify-center overflow-y-auto overflow-x-hidden'>
            <div className='relative mx-auto my-6 w-auto max-w-3xl'>
              <div className='relative flex w-full flex-col rounded-lg border-0 bg-white shadow-lg outline-none focus:outline-none'>
                <div className='border-blueGray-200 flex items-start justify-between rounded-t border-b border-solid p-5'>
                  <h3 className='text-3xl font-semibold'>Delete account</h3>
                  <button
                    className='float-right ml-auto border-0 p-1 text-3xl text-slate-400 transition hover:text-black'
                    onClick={() => setShowModal(false)}
                  >
                    <span className='block h-8 w-8 focus:outline-none'>
                      <XMarkIcon />
                    </span>
                  </button>
                </div>
                <div className='relative flex-auto p-6'>
                  <p className='my-4 text-xl'>
                    Are you sure you want to delete your account? NOTE: this
                    action is irreversible!
                  </p>
                </div>
                <div className='border-blueGray-200 flex items-center justify-end gap-4 rounded-b border-t border-solid p-6'>
                  <button
                    className='mb-1 mr-1 rounded-lg px-6 py-3 text-lg text-gray-500 transition-all duration-150 ease-linear hover:bg-slate-200 focus:outline-none'
                    type='button'
                    onClick={() => setShowModal(false)}
                  >
                    Close
                  </button>
                  <button
                    className='mb-1 mr-1 rounded-lg bg-red-500 px-6 py-3 text-lg text-white shadow outline-none transition-all duration-150 ease-linear hover:shadow-lg focus:outline-none active:bg-red-600'
                    type='button'
                    onClick={() => DeleteUser(isLoggedIn)}
                  >
                    Delete account
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div className='fixed inset-0 z-40 bg-black opacity-25'></div>
        </>
      ) : null}
    </>
  );
}
