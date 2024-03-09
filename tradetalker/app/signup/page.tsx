import React from 'react';
import { Metadata } from 'next';
import SignupForm from '@/app/ui/signup-form';
import { cookies } from 'next/headers';

export const metadata: Metadata = {
  title: 'Sign Up',
};

/**
 * Signup page.
 * @returns JSX.Element - Signup page component
 */
export default function LoginPage() {
  // Check if the user is logged in
  const session = cookies().get('session') !== undefined;

  return (
    <div className='md:p-10'>
      <SignupForm isLoggedIn={session} />
    </div>
  );
}
