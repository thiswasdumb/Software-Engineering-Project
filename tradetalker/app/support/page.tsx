import React, { Suspense } from 'react';
import { Metadata } from 'next';
import Loading from '@/app/ui/loading';
import Questions from '@/app/ui/questions';

export const metadata: Metadata = {
  title: 'Support',
};

export default function Support() {
  return (
    <Suspense fallback={<Loading message={'Loading questions...'} />}>
      <Questions />
    </Suspense>
  );
}
