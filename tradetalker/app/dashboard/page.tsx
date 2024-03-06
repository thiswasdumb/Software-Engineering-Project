import React, { Suspense, lazy } from 'react';
import { Metadata } from 'next';
import { cookies } from 'next/headers';
import Loading from '@/app/ui/loading';

export const metadata: Metadata = {
  title: 'Dashboard',
};

export default function Dashboard() {
  const session = cookies().get('session') !== undefined;
  const DashboardComponent = lazy(() => import('app/ui/dashboard/dashboard'));
  return (
    <Suspense fallback={<Loading message={'Loading dashboard...'} />}>
      <DashboardComponent isLoggedIn={session} />
    </Suspense>
  );
}
