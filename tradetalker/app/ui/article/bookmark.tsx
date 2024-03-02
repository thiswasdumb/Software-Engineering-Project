'use client';
import React, { useState, useEffect } from 'react';
import { BookmarkIcon } from '@heroicons/react/24/outline';
import { BookmarkIcon as SolidBookmarkIcon } from '@heroicons/react/24/solid';
import { toast } from 'react-hot-toast';

export default function Bookmark({ isBookmarked }: { isBookmarked: boolean }) {
  const [bookmarked, setBookmarked] = useState(false);

  useEffect(() => {
    // Set the bookmarked state accordingly
    setBookmarked(isBookmarked);
  }, [setBookmarked, isBookmarked]);

  const handleClick = () => {
    setBookmarked(!bookmarked);
    toast.success(
      bookmarked ? 'Removed from bookmarks.' : 'Added to bookmarks.'
    );
  };

  return !bookmarked ? (
    <BookmarkIcon
      type='button'
      cursor='pointer'
      className='h-10 w-10 text-gray-400 transition hover:text-blue-500'
      onClick={handleClick}
    />
  ) : (
    <SolidBookmarkIcon
      type='button'
      cursor='pointer'
      className='h-10 w-10 text-blue-500 transition hover:drop-shadow-lg'
      onClick={handleClick}
    />
  );
}
