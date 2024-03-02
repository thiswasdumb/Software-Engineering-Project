'use client';
import { Metadata } from 'next';
import { Button } from 'app/ui/button';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Not Found',
};

export default function NotFound() {
  return (
    <div className='bg-slate-200 m-8 rounded-lg p-8'>
      <div className='text-2xl'>404 Not Found</div>
      <hr className='border-slate-400 my-2 rounded-lg border-2' />
      <div className='text-xl'>Could not find requested resource.</div>
      <Button
        type='button'
        className='bg-blue-500 text-white hover:bg-blue-600 mt-2 justify-center rounded-lg p-4 text-lg transition '
      >
        <Link href='/home'>Return to home</Link>
      </Button>
    </div>
  );
}
