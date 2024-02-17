import React from 'react';
import { notFound } from 'next/navigation';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Company title',
};

export default async function CompanyPage({ params }: { params: { id: string } }) {
  const id = params.id;
  console.log(id);
  const company = true;

  if (!company) return notFound();

  return (
    <div>Article here.</div>
  );
}