import React from 'react';
import { notFound } from 'next/navigation';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Article title',
};

export default async function ArticlePage({ params }: { params: { id: string } }) {
  const id = params.id;
  console.log(id);
  const article = true;

  if (!article) return notFound();

  return (
    <div>Article here.</div>
  );
}