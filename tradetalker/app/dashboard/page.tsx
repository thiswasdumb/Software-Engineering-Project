import React, { Suspense, lazy } from 'react';
import { Metadata } from 'next';
import { cookies } from 'next/headers';
import Loading from '@/app/ui/loading';

export const metadata: Metadata = {
  title: 'Dashboard',
};

/**
 * Dashboard page.
 * @returns JSX.Element - Dashboard page component
 */
export default function Dashboard() {
  // Check if the user is logged in
  const session = cookies().get('session') !== undefined;
  // Lazy load the Dashboard component
  const DashboardComponent = lazy(() => import('app/ui/dashboard/dashboard'));

  return (
    <Suspense fallback={<Loading message={'Loading dashboard...'} />}>
      <DashboardComponent isLoggedIn={session} />
    </Suspense>
  );
}
