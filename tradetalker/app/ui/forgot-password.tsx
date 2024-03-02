'use client';
import React, { useState } from 'react';
import {
  AtSymbolIcon,
  ExclamationCircleIcon,
  ArrowRightIcon,
} from '@heroicons/react/20/solid';
import { toast } from 'react-hot-toast';
import { useFormStatus } from 'react-dom';
import { Button } from 'app/ui/button';

export default function ForgotPasswordComponent() {
  const [errorMessage, setErrorMessage] = useState('');
  const [data, setData] = useState({});
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await fetch('api/forgot_password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      const error = await response.json();
      if (error.error) {
        setErrorMessage(error.error);
        setTimeout(() => {
          setErrorMessage('');
        }, 6000);
      }
      if (response.ok) {
        toast.success('Success! A password reset link is sent to your email.');
      }
    } catch (error) {
      toast.error('An error occurred. Please try again later.');
    }
  };

  return (
    <div className='mt-10 flex items-center justify-center'>
      <div className='mx-auto flex w-full max-w-[400px] flex-col space-y-2.5 p-4'>
        <form onSubmit={handleSubmit} method='post' className='space-y-3'>
          <div className='bg-gray-50 flex-1 rounded-lg px-6 pb-4 pt-8'>
            <h1 className='mb-3 text-2xl'>
              To reset your password, enter your email address and we&apos;ll
              send you a link to do so.
            </h1>
            <div className='w-full'>
              <div>
                <label
                  className='text-md text-gray-900 mb-3 mt-5 block font-medium'
                  htmlFor='email'
                >
                  Email
                </label>
                <div className='relative'>
                  <input
                    className='border-gray-200 placeholder:text-gray-500 relative block w-full rounded-md border py-[9px] pl-10 text-sm outline-2'
                    id='email'
                    type='email'
                    name='email'
                    onChange={handleChange}
                    placeholder='Enter your email address'
                    maxLength={100}
                    required
                  />
                  <AtSymbolIcon className='text-gray-500 peer-focus:text-gray-900 pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2' />
                </div>
              </div>
            </div>
            <LoginButton />
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
  );
}

function LoginButton() {
  const { pending } = useFormStatus();
  return (
    <Button className='mt-5 w-full' aria-disabled={pending}>
      <div className='text-base'>Submit</div>
      <ArrowRightIcon className='text-gray-50 ml-auto h-5 w-5' />
    </Button>
  );
}
