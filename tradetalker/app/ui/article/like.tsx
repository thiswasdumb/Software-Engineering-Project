'use client';
import React, { useState, useEffect } from 'react';
import { HeartIcon } from '@heroicons/react/24/outline';
import { HeartIcon as SolidHeartIcon } from '@heroicons/react/24/solid';
import toast from 'react-hot-toast';

/**
 * Like component.
 * @param articleId - Article ID
 * @param isLoggedIn - Flag to check if the user is logged in
 * @returns JSX.Element - Like component
 */
export default function Like({
  articleId,
  isLoggedIn,
}: {
  articleId: string;
  isLoggedIn: boolean;
}) {
  const [liked, setLiked] = useState(false);

  // Set the liked state accordingly
  useEffect(() => {
    if (isLoggedIn) {
      const fetchLikeStatus = async () => {
        try {
          const response = await fetch(
            `/api/get_article_like_status/${articleId}`
          );
          const data = await response.json();
          setLiked(data.like_status);
        } catch (error) {
          console.error('Error fetching like status:', error);
        }
      };
      fetchLikeStatus();
    }
  }, [isLoggedIn, articleId]);

  // Handle the like button click
  const handleClick = async () => {
    if (!liked) {
      try {
        const response = await fetch(`/api/like_article/${articleId}`, {
          credentials: 'include',
        });
        const data = await response.json();
        if (data.success) {
          setLiked(!liked);
          toast.success('Liked article.');
        }
      } catch (error) {
        console.error('Error adding like:', error);
      }
    } else {
      try {
        const response = await fetch(`/api/unlike_article/${articleId}`, {
          credentials: 'include',
        });
        const data = await response.json();
        if (data.success) {
          setLiked(!liked);
          toast.success('Unliked article.');
        }
      } catch (error) {
        console.error('Error removing like:', error);
      }
    }
  };

  return (
    isLoggedIn &&
    (liked ? (
      <SolidHeartIcon
        type='button'
        title='Unlike this article'
        cursor='pointer'
        className={`h-10 w-10 text-red-500 transition hover:drop-shadow-lg ${liked ? 'text-red-500' : ''}`}
        onClick={handleClick}
      />
    ) : (
      <HeartIcon
        type='button'
        title='Like this article'
        cursor='pointer'
        className={`h-10 w-10 text-gray-400 transition hover:text-red-500 ${liked ? 'text-red-500' : ''}`}
        onClick={handleClick}
      />
    ))
  );
}
