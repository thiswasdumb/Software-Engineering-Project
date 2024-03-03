import React, { Suspense, lazy } from 'react';
import Loading from '@/app/ui/loading';

export default function Verify() {
  const VerifyUser = lazy(() => import('app/ui/verify'));
  return (
    <Suspense fallback={<Loading message={'Verifying...'} />}>
      <VerifyUser />;
    </Suspense>
  );
}
