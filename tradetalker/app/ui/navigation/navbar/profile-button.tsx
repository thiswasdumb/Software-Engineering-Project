'use client';
import Link from 'next/link';
import clsx from 'clsx';

export default function ProfileButton() {
  return (
    <>
      <Link href="/profile"
        className={clsx(
          'flex items-center justify-center p-2 hover:opacity-50',
        )}>
        Username here
      </Link>
    </>
  );
}