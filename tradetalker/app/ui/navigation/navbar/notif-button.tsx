'use client';
import Link from 'next/link';
import clsx from 'clsx';
import { BellIcon } from '@heroicons/react/24/outline';

export default function NotifButton({ notifCount }: { notifCount: number }) {
  return (
    <>
      <Link
        href='/notifications'
        className={clsx(
          'relative flex items-center justify-center p-2 hover:opacity-50'
        )}
      >
        <BellIcon className='h-6 w-6' />
        {notifCount > 0 && (
          <span className='absolute right-0 top-0 rounded-full bg-red-500 px-1 py-0.5 text-xs text-white'>
            {notifCount}
          </span>
        )}
      </Link>
    </>
  );
}
