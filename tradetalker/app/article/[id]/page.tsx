import React from 'react';
import { notFound } from 'next/navigation';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Article title',
};

export default async function ArticlePage({
  params,
}: {
  params: { id: string };
}) {
  const id = params.id;
  console.log(id);
  const article = true;

  if (!article) return notFound();

  return (
    <div>
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='text-2xl'>Article headline</div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
      </div>
    </div>
  );
}
