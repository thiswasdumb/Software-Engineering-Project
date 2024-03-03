import React, { Suspense, lazy } from 'react';
import { Metadata } from 'next';
import { cookies } from 'next/headers';
import Loading from '@/app/ui/loading';

export const metadata: Metadata = {
  title: 'Bookmarks',
};

export default function Bookmarks() {
  const session = cookies().get('session') !== undefined;
  const BookmarkComponent = lazy(() => import('app/ui/bookmarks'));
  return (
    <Suspense fallback={<Loading message={'Loading bookmarks...'} />}>
      <BookmarkComponent isLoggedIn={session} />
    </Suspense>
  );
}
