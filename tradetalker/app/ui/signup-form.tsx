'use client';
import {
  UserIcon,
  AtSymbolIcon,
  KeyIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline';
import { ArrowRightIcon } from '@heroicons/react/20/solid';
import { Button } from './button';
import { useFormState, useFormStatus } from 'react-dom';
import { authenticate } from '@/app/lib/actions';

export default function SignupForm() {
  const [errorMessage, dispatch] = useFormState(authenticate, undefined);
  return (
    <form action={dispatch} className='space-y-3' autoComplete='off'>
      <div className='flex-1 rounded-lg bg-gray-50 px-6 pb-4 pt-8'>
        <h1 className='mb-3 text-2xl'>
          Sign up to begin your TradeTalker journey.
        </h1>
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
                placeholder='Enter your email address'
                maxLength={254}
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
                minLength={3}
                maxLength={30}
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
                required
                minLength={8}
              />
              <KeyIcon className='pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900' />
            </div>
          </div>
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
  );
}

function SignupButton() {
  const { pending } = useFormStatus();
  return (
    <Button className='mt-5 w-full' aria-disabled={pending}>
      <div className='text-base'>Sign up</div>{' '}
      <ArrowRightIcon className='ml-auto h-5 w-5 text-gray-50' />
    </Button>
  );
}
