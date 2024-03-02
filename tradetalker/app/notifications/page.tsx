import React, { Suspense } from 'react';
import { Metadata } from 'next';
import { cookies } from 'next/headers';
import Loading from '@/app/ui/loading';
import NotifClientComponent from '@/app/ui/notifications/notif-component';

export const metadata: Metadata = {
  title: 'Notifications',
};

export default function Notifications() {
  const session = cookies().get('session') !== undefined;

  return (
    <Suspense fallback={<Loading message={'Loading notifications...'} />}>
      <NotifClientComponent isLoggedIn={session} />
    </Suspense>
  );
}
