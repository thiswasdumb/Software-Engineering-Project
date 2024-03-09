'use client';
import { ChatBubbleOvalLeftIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';

/**
 * Comments button component.
 * @param id - Article ID
 * @param comments - Number of comments
 * @returns JSX.Element - Comments button component
 */
export default function CommentsButton({
  id,
  comments,
}: {
  id: string;
  comments: number;
}) {
  return (
    <Link href={`/article/${id}#comments`} className='flex flex-row'>
      <button
        type='button'
        className='flex flex-row items-center text-start hover:drop-shadow-lg'
        onClick={(event) => event.stopPropagation()}
      >
        <ChatBubbleOvalLeftIcon className='h-6 w-6 text-slate-400' />
        <p className='pl-2 text-slate-500'>{comments}</p>
      </button>
    </Link>
  );
}
