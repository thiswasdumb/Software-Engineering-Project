import React from 'react';
import { notFound } from 'next/navigation';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Company title',
};

export default async function CompanyPage({
  params,
}: {
  params: { id: string };
}) {
  const id = params.id;
  console.log(id);
  const company = true;

  if (!company) return notFound();

  return (
    <div className='m-8 rounded-lg bg-slate-200 p-8'>
      <div className='text-2xl'>Company name</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      {/* Company stuff here */}
    </div>
  );
}
