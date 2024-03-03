import React, { Suspense, lazy } from 'react';
import { Metadata } from 'next';
import { cookies } from 'next/headers';
import Loading from '@/app/ui/loading';

export const metadata: Metadata = {
  title: 'Profile',
};

export default function Profile() {
  const session = cookies().get('session') !== undefined;
  const ProfileComponent = lazy(() => import('app/ui/profile'));
  return (
    <Suspense fallback={<Loading message={'Loading profile...'} />}>
      <ProfileComponent isLoggedIn={session} />
    </Suspense>
  );
}
