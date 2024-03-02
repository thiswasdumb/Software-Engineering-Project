'use client';
import React, { useState, useEffect, FormEvent, ChangeEvent } from 'react';
import {
  AtSymbolIcon,
  KeyIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline';
import { ArrowRightIcon } from '@heroicons/react/20/solid';
import { Button } from './button';
import { useFormStatus } from 'react-dom';
import { useSearchParams } from 'next/navigation';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';

export default function LoginForm({ isLoggedIn }: { isLoggedIn: boolean }) {
  const [errorMessage, setErrorMessage] = useState('');
  const searchParams = useSearchParams();
  const router = useRouter();
  const [data, setData] = useState({});
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };
  // Handle the form submission
  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevent the default refresh
    try {
      const response = await fetch('api/login_form', {
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

  // Show popup if user not logged in, otherwise redirect to dashboard
  useEffect(() => {
    if (!isLoggedIn) {
      const error = searchParams.get('error');
      if (error) {
        toast.error(error);
        router.replace('/login', undefined);
      }
    } else {
      router.push('/dashboard');
      toast.error('You are already logged in.');
    }
  }, [router, searchParams, isLoggedIn]);

  return (
    <>
      {!isLoggedIn && (
        <div className='mt-10 flex items-center justify-center'>
          <div className='mx-auto flex w-full max-w-[400px] flex-col space-y-2.5 p-4'>
            <form
              onSubmit={handleSubmit}
              method='post'
              className='space-y-3'
              autoComplete='off'
            >
              <div className='bg-gray-50 flex-1 rounded-lg px-6 pb-4 pt-8'>
                <h1 className='mb-3 text-2xl'>
                  Log in to continue your TradeTalker journey.
                </h1>
                <div className='w-full'>
                  <div>
                    <label
                      className='text-gray-900 mb-3 mt-5 block text-base font-medium'
                      htmlFor='username'
                    >
                      Username
                    </label>
                    <div className='relative'>
                      <input
                        className='border-gray-200 placeholder:text-gray-500 relative block w-full rounded-md border py-[9px] pl-10 text-sm outline-2'
                        id='username'
                        type='text'
                        name='username'
                        placeholder='Enter your username'
                        onChange={handleChange}
                        minLength={3}
                        maxLength={50}
                        required
                      />
                      <AtSymbolIcon className='text-gray-500 peer-focus:text-gray-900 pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2' />
                    </div>
                  </div>
                  <div className='mt-4'>
                    <label
                      className='text-gray-900 mb-3 mt-5 block text-base font-medium'
                      htmlFor='password'
                    >
                      Password
                    </label>
                    <div className='relative'>
                      <input
                        className='border-gray-200 placeholder:text-gray-500 relative block w-full rounded-md border py-[9px] pl-10 text-sm outline-2'
                        id='password'
                        type='password'
                        name='password'
                        placeholder='Enter password'
                        onChange={handleChange}
                        required
                        minLength={8}
                        maxLength={200}
                        pattern='(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}'
                      />
                      <KeyIcon className='text-gray-500 peer-focus:text-gray-900 pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2' />
                    </div>
                  </div>
                </div>
                <LoginButton />
                <ForgotPassword />
                <div
                  className='flex h-8 items-end space-x-1 overflow-hidden'
                  aria-live='polite'
                  aria-atomic='true'
                >
                  {errorMessage && (
                    <>
                      <ExclamationCircleIcon className='text-red-500 h-5 w-5' />
                      <p className='text-red-500 text-sm'>{errorMessage}</p>
                    </>
                  )}
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}

function LoginButton() {
  const { pending } = useFormStatus();
  return (
    <Button
      className='mt-5 w-full transition hover:drop-shadow-lg'
      aria-disabled={pending}
    >
      <div className='text-base'>Log in</div>
      <ArrowRightIcon className='text-gray-50 ml-auto h-5 w-5' />
    </Button>
  );
}

function ForgotPassword() {
  return (
    <Button className='bg-slate-500 hover:bg-slate-400 active:bg-slate-500 mt-3'>
      <a href='/forgot-password'>Forgot password?</a>
    </Button>
  );
}
