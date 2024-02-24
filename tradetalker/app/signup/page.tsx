import React from 'react';
import { Metadata } from 'next';
import SignupForm from '@/app/ui/signup-form';

export const metadata: Metadata = {
  title: 'Sign Up',
};

export default function LoginPage() {
  return (
    <main className='mt-10 flex items-center justify-center'>
      <div className='mx-auto flex w-full max-w-[400px] flex-col space-y-2.5 p-4'>
        <SignupForm />
      </div>
    </main>
  );
}
