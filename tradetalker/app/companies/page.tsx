import React from 'react';
import { Suspense } from 'react';
import Loading from '@/app/ui/loading';
import CompaniesComponent from '../ui/company/companies';

export default function Companies() {
  return (
    <Suspense fallback={<Loading message={'Loading companies...'} />}>
      <CompaniesComponent />
    </Suspense>
  );
}
