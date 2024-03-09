import { Metadata } from 'next';
import { Suspense, lazy } from 'react';
import Loading from '@/app/ui/loading';

export const metadata: Metadata = {
  title: 'Welcome!',
};

/**
 * Home page.
 * @returns JSX.Element - Home page component
 */
export default function Home() {
  // Lazy load the Home component
  const HomeComponent = lazy(() => import('@/app/ui/home/homepage')); // Lazy load the component

  return (
    <Suspense fallback={<Loading message={'Loading home...'} />}>
      <HomeComponent />
    </Suspense>
  );
}
