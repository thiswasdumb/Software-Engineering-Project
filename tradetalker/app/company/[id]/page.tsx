import React, { Suspense } from 'react';
import CompanyPage from '@/app/ui/company/company';
import Loading from '@/app/ui/loading';
import { cookies } from 'next/headers';

/**
 * Single company page.
 * @param id - Company ID from the URL
 * @returns JSX.Element - Company page component
 */
export default function Company({ params }: { params: { id: string } }) {
  // Check if the user is logged in
  const session = cookies().get('session') !== undefined;

  return (
    <Suspense fallback={<Loading message={'Loading company...'} />}>
      <CompanyPage id={params.id} isLoggedIn={session} />
    </Suspense>
  );
}
