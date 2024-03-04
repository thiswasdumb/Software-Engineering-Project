import React, { Suspense } from 'react';
import CompanyPage from '@/app/ui/company/company';
import Loading from '@/app/ui/loading';
import { cookies } from 'next/headers';

export default function Company({ params }: { params: { id: string } }) {
  const session = cookies().get('session') !== undefined;
  return (
    <Suspense fallback={<Loading message={'Loading company...'} />}>
      <CompanyPage id={params.id} isLoggedIn={session} />
    </Suspense>
  );
}
