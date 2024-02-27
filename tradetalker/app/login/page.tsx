import React from 'react';
import { Metadata } from 'next';
import LoginForm from '@/app/ui/login-form';
import { cookies } from 'next/headers';

export const metadata: Metadata = {
  title: 'Log In',
};

export default function LoginPage() {
  const session = cookies().get('session') !== undefined;
  return (
    <div className='md:p-10'>
      <LoginForm isLoggedIn={session} />
    </div>
  );
}
