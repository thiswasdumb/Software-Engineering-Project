import React, { Suspense, lazy } from 'react';
import { Metadata } from 'next';
import { cookies } from 'next/headers';
import Loading from '@/app/ui/loading';

export const metadata: Metadata = {
  title: 'Bookmarks',
};

/**
 * Bookmarks page.
 * @returns JSX.Element - Bookmarks page component
 */
export default function Bookmarks() {
  // Check if the user is logged in
  const session = cookies().get('session') !== undefined;
  // Lazy load the Bookmarks component
  const BookmarkComponent = lazy(() => import('app/ui/bookmarks'));

  return (
    <Suspense fallback={<Loading message={'Loading bookmarks...'} />}>
      <BookmarkComponent isLoggedIn={session} />
    </Suspense>
  );
}
