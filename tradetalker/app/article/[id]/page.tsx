import React, { Suspense } from 'react';
import Loading from '@/app/ui/loading';
import ArticlePage from '@/app/ui/article/article';
import { cookies } from 'next/headers';

/**
 * Single article page.
 * @param id - Article ID from the URL
 * @returns JSX.Element - Article page component
 */
export default function Article({ params }: { params: { id: string } }) {
  // Check if the user is logged in
  const session = cookies().get('session') !== undefined;

  return (
    <Suspense fallback={<Loading message={'Loading article...'} />}>
      <ArticlePage id={params.id} isLoggedIn={session} />
    </Suspense>
  );
}
