import React, { Suspense } from 'react';
import Loading from '@/app/ui/loading';
import ArticlePage from '@/app/ui/article/article';
import { cookies } from 'next/headers';

export default function Company({ params }: { params: { id: string } }) {
  const session = cookies().get('session') !== undefined;
  return (
    <Suspense fallback={<Loading message={'Loading article...'} />}>
      <ArticlePage id={params.id} isLoggedIn={session} />
    </Suspense>
  );
}
