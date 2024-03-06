'use client';
import {
  UserIcon,
  AtSymbolIcon,
  KeyIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline';
import { ArrowRightIcon } from '@heroicons/react/20/solid';
import { Button } from './button';
import { useFormStatus } from 'react-dom';
import { useSearchParams } from 'next/navigation';
import React, { useState, useEffect, FormEvent, ChangeEvent } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';

export default function SignupForm({ isLoggedIn }: { isLoggedIn: boolean }) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [errorMessage, setErrorMessage] = useState('');
  const [data, setData] = useState({});
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await fetch('api/registration', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      const error = await response.json();
      if (error.url === 'dashboard') {
        router.push('/dashboard');
        toast.success('Please check your email to verify your account.');
        router.refresh();
      }
      if (error.url == 'login') {
        router.push('/login');
        toast.error('Account already exists. Please log in.');
        router.refresh();
      }
      if (error.url == 'signup') {
        setErrorMessage(error.error);
        setTimeout(() => {
          setErrorMessage('');
        }, 6000);
      }
    } catch (error) {
      toast.error('An error occurred. Please try again later.');
    }
  };

  useEffect(() => {
    if (!isLoggedIn) {
      const error = searchParams.get('error');
      if (error) {
        toast.error(error);
        router.replace('/signup', undefined);
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
          <div className='mx-auto flex w-[400px] flex-col space-y-2.5 p-4 md:w-[600px]'>
            <form
              onSubmit={handleSubmit}
              method='post'
              className='space-y-3'
              autoComplete='off'
            >
              <div className='flex-1 rounded-lg bg-gray-50 px-6 pb-4 pt-8'>
                <h1 className='mb-3 text-2xl'>
                  Sign up to begin your TradeTalk journey.
                </h1>
                <p>
                  Please choose a suitable username between 3 and 50 characters.
                  Passwords must be between 8 and 200 characters and have at
                  least 1 capital letter and 1 special character.
                </p>
                <div className='w-full'>
                  <div>
                    <label
                      className='text-md mb-3 mt-5 block font-medium text-gray-900'
                      htmlFor='email'
                    >
                      Email
                    </label>
                    <div className='relative'>
                      <input
                        className='relative block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500'
                        id='email'
                        type='email'
                        name='email'
                        onChange={handleChange}
                        placeholder='Enter your email address'
                        maxLength={100}
                        required
                      />
                      <AtSymbolIcon className='pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900' />
                    </div>
                  </div>
                  <div>
                    <label
                      className='text-md mb-3 mt-5 block font-medium text-gray-900'
                      htmlFor='username'
                    >
                      Username
                    </label>
                    <div className='relative'>
                      <input
                        className='relative block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500'
                        id='username'
                        type='text'
                        name='username'
                        placeholder='Enter a username'
                        onChange={handleChange}
                        minLength={3}
                        maxLength={50}
                        required
                      />
                      <UserIcon className='pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900' />
                    </div>
                  </div>
                  <div className='mt-4'>
                    <label
                      className='text-md mb-3 mt-5 block font-medium text-gray-900'
                      htmlFor='password'
                    >
                      Password
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
                        pattern='(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}'
                      />
                      <KeyIcon className='pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900' />
                    </div>
                  </div>
                  <p className='mt-4 text-sm'>
                    By creating an account, you agree to the{' '}
                    <a
                      href='/terms'
                      className='text-blue-600 underline hover:text-blue-500'
                    >
                      Terms
                    </a>{' '}
                    and{' '}
                    <a
                      href='/privacy'
                      className='text-blue-600 underline hover:text-blue-500'
                    >
                      Privacy Policy
                    </a>
                    .
                  </p>
                </div>
                <SignupButton />
                <div
                  className='flex h-8 items-end space-x-1'
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
      )}
    </>
  );
}

function SignupButton() {
  const { pending } = useFormStatus();
  return (
    <Button type='submit' className='mt-5 w-full' aria-disabled={pending}>
      <div className='text-base'>Sign up</div>{' '}
      <ArrowRightIcon className='ml-auto h-5 w-5 text-gray-50' />
    </Button>
  );
}
