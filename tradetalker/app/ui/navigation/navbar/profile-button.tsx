'use client';
import { UserIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import clsx from 'clsx';

export default function ProfileButton() {
  return (
    <>
      <Link
        href='/profile'
        className={clsx(
          'flex items-center justify-center p-2 hover:opacity-50'
        )}
      >
        <UserIcon className='h-6 w-6' />
      </Link>
    </>
  );
}
