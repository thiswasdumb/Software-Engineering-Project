import React from 'react';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Support',
};

export default function Support() {
  return (
    <div className='m-8 rounded-lg bg-slate-200 p-8'>
      <div className='text-2xl'>Support</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      {/* FAQ stuff here */}
    </div>
  );
}
