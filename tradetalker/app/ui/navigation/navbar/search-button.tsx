'use client';
import Link from 'next/link';
import clsx from 'clsx';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

export default function SearchButton() {
  return (
    <>
      <Link href="/search"
        className={clsx(
          "items-center justify-center p-2 hover:opacity-50",
        )}>
        <MagnifyingGlassIcon className="w-8 h-8" />
      </Link>
    </>
  );
}