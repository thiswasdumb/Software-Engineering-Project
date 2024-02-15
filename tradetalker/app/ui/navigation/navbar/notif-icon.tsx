'use client';
import Link from 'next/link';
import clsx from 'clsx';
import { BellIcon } from '@heroicons/react/24/outline';

export default function NotifButton() {
  return (
    <>
      <Link href="/notifications"
        className={clsx(
          'flex items-center justify-center p-2 hover:opacity-50',
        )}>
        <BellIcon className="w-6 h-6" />
      </Link>
    </>
  );
}