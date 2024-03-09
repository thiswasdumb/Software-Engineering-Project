'use client';
import Link from 'next/link';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

/**
 * Search button component.
 * @param props.isOpen - Whether the mobile navbar is open
 * @param props.toggle - Function to toggle the mobile navbar
 * @returns JSX.Element - Search button component
 */
export default function SearchButton(props: {
  isOpen: boolean;
  toggle: () => void;
}) {
  return (
    <>
      <Link
        href='/search'
        className='flex items-center justify-center p-2 hover:opacity-50 '
        onClick={props.isOpen ? props.toggle : undefined}
        title='Search'
      >
        <button type='button'>
          <MagnifyingGlassIcon className='h-8 w-8 md:h-6 md:w-6' />
        </button>
      </Link>
    </>
  );
}
