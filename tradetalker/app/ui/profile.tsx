'use client';
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';
import Link from 'next/link';
import { Button } from 'app/ui/button';
import Logout from 'app/ui/logout';
import { XMarkIcon } from '@heroicons/react/20/solid';

/**
 * Profile component.
 * @param isLoggedIn - Whether the user is logged in
 * @returns JSX.Element - Profile component
 */
export default function ProfileComponent({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [data, setData] = useState<Record<string, any>>({});
  const [verified, setVerified] = useState(false);
  const [disabled, setDisabled] = useState(false);
  const router = useRouter();

  // Fetch the user's profile data
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

  // Check if the user is verified
  useEffect(() => {
    if (isLoggedIn) {
      fetch('/api/check_verified', { credentials: 'include' })
        .then((response) => response.json())
        .then((data) => {
          if (data.verified) {
            setVerified(true);
          }
        })
        .catch(() => {
          console.error('Error verifying user.');
        });
    }
  }, [isLoggedIn]);

  // Verify the user's email
  function VerifyUser() {
    fetch('/api/verify_email', {
      credentials: 'include',
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          toast.success('We have sent you an email to verify your account.');
          setDisabled(true);
        }
      })
      .catch(() => {
        toast.error('Error verifying user.');
      });
  }

  return (
    isLoggedIn && (
      <div className='rounded-lg bg-slate-200 p-8 md:m-8'>
        <h1 className='text-2xl'>Profile</h1>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <div className='flex flex-col items-start rounded-lg bg-slate-200'>
          <div>
            <p className='text-xl'>Username: {data.username}</p>
            <div className='flex flex-row items-center'>
              <p className='text-xl'>Email: {data.email}</p>
              <div className='ml-4'>
                {verified ? (
                  <div className='rounded-lg bg-green-500 p-2 text-white'>
                    Verified
                  </div>
                ) : (
                  <button
                    disabled={disabled}
                    type='button'
                    onClick={() => VerifyUser()}
                    className='rounded-lg bg-blue-500 p-2 text-white hover:bg-blue-600 hover:drop-shadow-lg active:bg-blue-700'
                  >
                    Verify
                  </button>
                )}
              </div>
            </div>
            <Button
              type='button'
              className='mt-4 rounded-lg bg-blue-500 p-4 text-white transition hover:bg-blue-600 hover:shadow-lg active:bg-blue-700'
            >
              <Link href='/forgot-password'>Reset password</Link>
            </Button>
            <div>
              <button
                type='button'
                className='mt-4 rounded-lg bg-red-500 p-4 text-white transition hover:bg-red-600 hover:shadow-lg active:bg-red-700'
                onClick={() => Logout(isLoggedIn)}
              >
                Log out
              </button>
            </div>
            <DeleteUserModal />
          </div>
        </div>
      </div>
    )
  );
}

/**
 * Delete user modal
 * @returns JSX.Element - Delete user modal
 */
export function DeleteUserModal() {
  const [showModal, setShowModal] = React.useState(false);

  return (
    <>
      <div className='mt-4' onClick={() => setShowModal(true)}>
        <button
          type='button'
          className='rounded-lg bg-red-500 p-4 text-white transition hover:bg-red-600 hover:shadow-lg active:bg-red-700'
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
                  >
                    <Link href='/api/delete_user'>Delete account</Link>
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
