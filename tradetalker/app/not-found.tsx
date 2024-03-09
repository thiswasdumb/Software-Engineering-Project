'use client';
import { Metadata } from 'next';
import { Button } from 'app/ui/button';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Not Found',
};

/**
 * Not Found page.
 * @returns JSX.Element - Not Found page component
 */
export default function NotFound() {
  return (
    <div className='m-8 rounded-lg bg-slate-200 p-8'>
      <div className='text-2xl'>404 Not Found</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <div className='mb-2 text-xl'>Could not find requested resource.</div>
      <Button>
        <Link href='/home'>Return to home</Link>
      </Button>
    </div>
  );
}
