import { BookmarkIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import clsx from 'clsx';

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
      >
        <button type='button'>
          <BookmarkIcon className='h-8 w-8 md:h-6 md:w-6' />
        </button>
      </Link>
    </>
  );
}
