import React from 'react';
import { Metadata } from 'next';
import SearchBar from '@/app/ui/search';

export const metadata: Metadata = {
  title: 'Search',
};

export default function Search() {
  return (
    <div className='md:p-10'>
      <SearchBar placeholder='Search for an article or company...' />
    </div>
  );
}
