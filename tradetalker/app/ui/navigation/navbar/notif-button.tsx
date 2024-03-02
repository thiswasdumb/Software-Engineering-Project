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
        <BellIcon className='h-8 w-8 md:h-6 md:w-6' />
        {notifCount > 0 && (
          <span className='text-md bg-red-500 text-white absolute right-0 top-0 rounded-full px-1 py-0.5 md:text-xs'>
            {notifCount}
          </span>
        )}
      </Link>
    </>
  );
}
