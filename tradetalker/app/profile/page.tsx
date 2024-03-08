import React, { Suspense, lazy } from 'react';
import { Metadata } from 'next';
import { cookies } from 'next/headers';
import Loading from '@/app/ui/loading';

export const metadata: Metadata = {
  title: 'Profile',
};

/**
 * Profile page.
 * @returns JSX.Element - Profile page component
 */
export default function Profile() {
  // Check if the user is logged in
  const session = cookies().get('session') !== undefined;
  // Lazy load the Profile component
  const ProfileComponent = lazy(() => import('app/ui/profile'));

  return (
    <Suspense fallback={<Loading message={'Loading profile...'} />}>
      <ProfileComponent isLoggedIn={session} />
    </Suspense>
  );
}
