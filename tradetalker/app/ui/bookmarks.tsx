'use client';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';
import dayjs from 'dayjs';
import LocalizedFormat from 'dayjs/plugin/localizedFormat';

export default function BookmarkComponent({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [bookmarks, setBookmarks] = useState<any[]>([]);
  const router = useRouter();
  dayjs.extend(LocalizedFormat);

  useEffect(() => {
    if (isLoggedIn) {
      const fetchBookmarks = async () => {
        try {
          const response = await fetch('/api/get_bookmarks', {
            credentials: 'include',
          });
          const data = await response.json();
          setBookmarks(data);
        } catch (error) {
          toast.error('Error fetching notifications.');
        }
      };

      fetchBookmarks();
    } else {
      router.push('/login');
      toast.error('You must be logged in.');
    }
  }, [isLoggedIn, setBookmarks, router]);

  const deleteBookmark = async (id: string) => {
    try {
      const response = await fetch(`/api/delete_bookmark/${id}`);
      const message = await response.json();
      if (message.success) {
        const updatedBookmarks = bookmarks.filter(
          (bookmark) => bookmark.id !== id
        );
        setBookmarks(updatedBookmarks);
        toast.success('Bookmark deleted.');
      } else {
        toast.error('Error deleting bookmark.');
      }
    } catch (error) {
      toast.error('Error deleting bookmark.');
    }
  };

  return (
    isLoggedIn && (
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='text-2xl'>Bookmarks</div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        {bookmarks.length === 0 && <p>No bookmarks.</p>}
        {bookmarks.length > 0 &&
          bookmarks.map((bookmark, index) => (
            <div key={index} className='my-2 rounded-lg bg-slate-300 p-2'>
              <div className='flex flex-row items-center justify-between'>
                <Link
                  href={`/article/${bookmark.article_id}`}
                  className='grow transition hover:drop-shadow-lg'
                >
                  <div className='text-sm'>
                    {dayjs(bookmark.date).format('D MMM YYYY LT')}
                  </div>
                  <div className='text-lg'>{bookmark.title}</div>
                  <div className='truncate text-sm'>{bookmark.summary}</div>
                </Link>
                <button
                  type='button'
                  className='float-right m-2 rounded-lg bg-red-500 p-2 text-sm text-white transition hover:bg-red-600 hover:shadow-lg active:bg-red-700'
                  onClick={() => deleteBookmark(bookmark.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
      </div>
    )
  );
}
