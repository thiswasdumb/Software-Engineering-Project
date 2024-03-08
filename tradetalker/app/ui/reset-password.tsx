'use client';
import React, { useEffect, useState, FormEvent, ChangeEvent } from 'react';
import { KeyIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline';
import { ArrowRightIcon } from '@heroicons/react/20/solid';
import { Button } from './button';
import { useFormStatus } from 'react-dom';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';

/**
 * Reset password form component.
 * @param token - The reset password token
 * @returns JSX.Element - Reset password form component
 */
export default function ResetPasswordForm({ token }: { token: string }) {
  const [errorMessage, setErrorMessage] = useState('');
  const router = useRouter();
  const [data, setData] = useState({});
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  // Check if the token is valid
  useEffect(() => {
    if (!token) {
      router.push('/not-found');
    }
    fetch(`/api/reset_password/${token}`, {
      method: 'GET',
    }).then((response) => {
      if (response.status === 404) {
        router.push('/not-found');
      }
    });
  }, [token, router]);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevent the default form submission
    try {
      const response = await fetch(`/api/submit_reset_password/${token}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      const message = await response.json(); // Parse the JSON response
      if (message.error) {
        setErrorMessage(message.error);
        setTimeout(() => {
          setErrorMessage('');
        }, 6000);
      }
      if (message.success) {
        router.push('/dashboard');
        toast.success(message.success);
        router.refresh();
      }
    } catch (error) {
      toast.error('An error occurred. Please try again later.');
    }
  };

  return (
    <>
      <div className='mt-10 flex items-center justify-center'>
        <div className='mx-auto flex w-full max-w-[400px] flex-col space-y-2.5 p-4'>
          <form
            onSubmit={handleSubmit}
            method='post'
            className='space-y-3'
            autoComplete='off'
          >
            <div className='flex-1 rounded-lg bg-gray-50 px-6 pb-4 pt-8'>
              <h1 className='mb-3 text-2xl'>Enter your new password.</h1>
              <p>
                Your password must be between 8 and 200 characters and have at
                least 1 uppercase, 1 lowercase and 1 special character.
              </p>
              <div className='w-full'>
                <div className='mt-4'>
                  <label
                    className='mb-3 mt-5 block text-base font-medium text-gray-900'
                    htmlFor='password'
                  >
                    New password
                  </label>
                  <div className='relative'>
                    <input
                      className='relative block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500'
                      id='password'
                      type='password'
                      name='password'
                      placeholder='Enter password'
                      onChange={handleChange}
                      required
                      minLength={8}
                      maxLength={200}
                      pattern='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
                    />
                    <KeyIcon className='pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900' />
                  </div>
                </div>
              </div>
              <div className='w-full'>
                <div className='mt-4'>
                  <label
                    className='mb-3 mt-5 block text-base font-medium text-gray-900'
                    htmlFor='password'
                  >
                    Repeat password
                  </label>
                  <div className='relative'>
                    <input
                      className='relative block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500'
                      id='password_repeat'
                      type='password'
                      name='password_repeat'
                      placeholder='Enter password'
                      onChange={handleChange}
                      required
                      minLength={8}
                      maxLength={200}
                      pattern='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
                    />
                    <KeyIcon className='pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900' />
                  </div>
                </div>
              </div>
              <ChangePasswordButton />
              <div
                className='flex h-16 items-center space-x-1 overflow-hidden'
                aria-live='polite'
                aria-atomic='true'
              >
                {errorMessage && (
                  <>
                    <ExclamationCircleIcon className='h-5 w-5 text-red-500' />
                    <p className='text-sm text-red-500'>{errorMessage}</p>
                  </>
                )}
              </div>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}

function ChangePasswordButton() {
  const { pending } = useFormStatus();
  return (
    <Button type='submit' className='mt-5 w-full' aria-disabled={pending}>
      <div className='text-base'>Change password</div>
      <ArrowRightIcon className='ml-auto h-5 w-5 text-gray-50' />
    </Button>
  );
}
