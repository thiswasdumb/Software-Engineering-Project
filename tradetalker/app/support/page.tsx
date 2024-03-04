import React, { Suspense } from 'react';
import { Metadata } from 'next';
import Loading from '@/app/ui/loading';
import Questions from '@/app/ui/support/questions';
import { cookies } from 'next/headers';

export const metadata: Metadata = {
  title: 'Support',
};

export default function Support() {
  const session = cookies().get('session') !== undefined;
  return (
    <Suspense fallback={<Loading message={'Loading questions...'} />}>
      <Questions isLoggedIn={session} />
    </Suspense>
  );
}
