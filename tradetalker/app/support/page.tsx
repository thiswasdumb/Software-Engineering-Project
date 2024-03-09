import React, { Suspense } from 'react';
import { Metadata } from 'next';
import Loading from '@/app/ui/loading';
import Questions from '@/app/ui/support/questions';
import { cookies } from 'next/headers';

export const metadata: Metadata = {
  title: 'Support',
};

/**
 * Support page.
 * @returns JSX.Element - Support page component
 */
export default function Support() {
  // Check if the user is logged in
  const session = cookies().get('session') !== undefined;

  return (
    <Suspense fallback={<Loading message={'Loading questions...'} />}>
      <Questions isLoggedIn={session} />
    </Suspense>
  );
}
