'use client';
import React, { useState, useEffect } from 'react';
import { BookmarkIcon } from '@heroicons/react/24/outline';
import { BookmarkIcon as SolidBookmarkIcon } from '@heroicons/react/24/solid';
import { toast } from 'react-hot-toast';

export default function Bookmark({
  isBookmarked,
  isLoggedIn,
  id,
}: {
  isBookmarked: boolean;
  isLoggedIn: boolean;
  id: string;
}) {
  const [bookmarked, setBookmarked] = useState(false);

  useEffect(() => {
    // Set the bookmarked state accordingly
    setBookmarked(isBookmarked);
  }, [setBookmarked, isBookmarked]);

  const handleClick = async () => {
    setBookmarked(!bookmarked);
    if (isLoggedIn) {
      if (!bookmarked) {
        try {
          const response = await fetch(`/api/add_bookmark/${id}`, {
            credentials: 'include',
          });
          const data: Record<string, any> = response.json();
          if (data.success) {
            setBookmarked(true);
          }
        } catch (error) {
          console.error('Error adding bookmark:', error);
        }
      } else {
        try {
          const response = await fetch(`/api/remove_bookmark/${id}`, {
            credentials: 'include',
          });
          const data: Record<string, any> = response.json();
          if (data.success) {
            setBookmarked(false);
          }
        } catch (error) {
          console.error('Error removing bookmark:', error);
        }
      }
    } else {
      toast.error('You must be logged in.');
    }
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
