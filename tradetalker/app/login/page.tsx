import React from 'react';
import { Metadata } from 'next';
import LoginForm from '@/app/ui/login-form';

export const metadata: Metadata = {
  title: 'Log In',
};

export default function LoginPage() {
  return (
    <main className='mt-10 flex items-center justify-center'>
      <div className='mx-auto flex w-full max-w-[400px] flex-col space-y-2.5 p-4'>
        <LoginForm />
      </div>
    </main>
  );
}
