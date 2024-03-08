'use client';
import Link from 'next/link';
import clsx from 'clsx';
import { BellIcon } from '@heroicons/react/24/outline';

/**
 * Notification button component.
 * @param props.notifCount - Number of notifications
 * @returns JSX.Element - Notification button component
 */
export default function NotifButton({ notifCount }: { notifCount: number }) {
  return (
    <>
      <Link
        href='/notifications'
        className={clsx(
          'relative flex items-center justify-center p-2 hover:opacity-50'
        )}
      >
        <button type='button' onClick={() => window.location.reload()}>
          <BellIcon className='h-8 w-8 md:h-6 md:w-6' />
        </button>
        {notifCount > 0 && (
          <span className='text-md absolute right-0 top-0 rounded-full bg-red-500 px-1 py-0.5 text-white md:text-xs'>
            {notifCount}
          </span>
        )}
      </Link>
    </>
  );
}
