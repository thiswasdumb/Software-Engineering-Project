import { BookmarkIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import clsx from 'clsx';

/**
 * Bookmark button component.
 * @param props.isOpen - Whether the mobile navbar is open
 * @param props.toggle - Function to toggle the mobile navbar
 * @returns JSX.Element - Bookmark button component
 */
export default function BookmarkButton(props: {
  isOpen: boolean;
  toggle: () => void;
}) {
  return (
    <>
      <Link
        href='/bookmarks'
        onClick={props.isOpen ? props.toggle : undefined}
        className={clsx(
          'relative flex items-center justify-center p-2 hover:opacity-50'
        )}
        title='Bookmarks'
      >
        <button type='button'>
          <BookmarkIcon className='h-8 w-8 md:h-6 md:w-6' />
        </button>
      </Link>
    </>
  );
}
