import React from 'react';
import { Metadata } from 'next';
import SignupForm from '@/app/ui/signup-form';
import { cookies } from 'next/headers';

export const metadata: Metadata = {
  title: 'Sign Up',
};

export default function LoginPage() {
  const session = cookies().get('session') !== undefined;
  return (
    <div className='md:p-10'>
      <SignupForm isLoggedIn={session} />
    </div>
  );
}
