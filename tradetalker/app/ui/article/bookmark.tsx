'use client';
import React, { useState, useEffect } from 'react';
import { BookmarkIcon } from '@heroicons/react/24/outline';
import { BookmarkIcon as SolidBookmarkIcon } from '@heroicons/react/24/solid';
import { toast } from 'react-hot-toast';

/**
 * Bookmark component.
 * @param articleId - Article ID
 * @param isLoggedIn - Flag to check if the user is logged in
 * @returns JSX.Element - Bookmark component
 */
export default function Bookmark({
  articleId,
  isLoggedIn,
}: {
  articleId: string;
  isLoggedIn: boolean;
}) {
  const [bookmarked, setBookmarked] = useState(false);

  useEffect(() => {
    // Set the bookmarked state accordingly
    if (isLoggedIn) {
      const fetchBookmarkStatus = async () => {
        try {
          const response = await fetch(
            `/api/get_article_bookmark_status/${articleId}`
          );
          const data = await response.json();
          setBookmarked(data.bookmark_status);
        } catch (error) {
          console.error('Error fetching bookmark status:', error);
        }
      };
      fetchBookmarkStatus();
    }
  }, [isLoggedIn, articleId]);

  const handleClick = async () => {
    setBookmarked(!bookmarked);
    if (isLoggedIn) {
      if (!bookmarked) {
        try {
          const response = await fetch(`/api/add_bookmark/${articleId}`, {
            credentials: 'include',
          });
          const data = await response.json();
          if (data.success) {
            setBookmarked(!bookmarked);
            toast.success('Added bookmark.');
          }
        } catch (error) {
          console.error('Error adding bookmark:', error);
        }
      } else {
        try {
          const response = await fetch(`/api/delete_bookmark/${articleId}`, {
            credentials: 'include',
          });
          const data = await response.json();
          if (data.success) {
            setBookmarked(!bookmarked);
            toast.success('Removed bookmark.');
          }
        } catch (error) {
          console.error('Error removing bookmark:', error);
        }
      }
    } else {
      toast.error('You must be logged in.');
    }
  };

  <BookmarkIcon
    type='button'
    cursor='pointer'
    className='h-10 w-10 text-gray-400 transition hover:text-blue-500'
    onClick={handleClick}
  />;

  return (
    isLoggedIn &&
    (bookmarked ? (
      <SolidBookmarkIcon
        type='button'
        title='Remove bookmark'
        cursor='pointer'
        className='h-10 w-10 text-blue-500 transition hover:drop-shadow-lg'
        onClick={handleClick}
      />
    ) : (
      <BookmarkIcon
        type='button'
        title='Bookmark this article'
        cursor='pointer'
        className='h-10 w-10 text-gray-400 transition hover:text-blue-500'
        onClick={handleClick}
      />
    ))
  );
}
