import { Metadata } from 'next';
import { Suspense, lazy } from 'react';
import Loading from '@/app/ui/loading';

export const metadata: Metadata = {
  title: 'Welcome!',
};

export default function Home() {
  const HomeComponent = lazy(() => import('@/app/ui/home/homepage')); // Lazy load the component
  return (
    <Suspense fallback={<Loading message={'Loading home...'} />}>
      <HomeComponent />
    </Suspense>
  );
}
