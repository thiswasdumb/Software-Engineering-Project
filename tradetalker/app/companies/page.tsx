import React from 'react';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Companies',
};

export default function Companies() {
  return (
    <div className='m-8 rounded-lg bg-slate-200 p-8'>
      <div className='text-2xl'>Companies</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      {/* Companies here */}
    </div>
  );
}
