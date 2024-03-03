import React, { Suspense } from 'react';
import CompanyPage from '@/app/ui/company/company';
import Loading from '@/app/ui/loading';

export default function Company({ params }: { params: { id: string } }) {
  return (
    <Suspense fallback={<Loading message={'Loading company...'} />}>
      <CompanyPage id={params.id} />
    </Suspense>
  );
}
