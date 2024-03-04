'use client';
import React, { useState, useEffect } from 'react';
import { HeartIcon } from '@heroicons/react/24/outline';
import { HeartIcon as SolidHeartIcon } from '@heroicons/react/24/solid';
import toast from 'react-hot-toast';

export default function Like({
  isLiked,
  articleId,
  isLoggedIn,
}: {
  isLiked: boolean;
  articleId: string;
  isLoggedIn: boolean;
}) {
  const [liked, setLiked] = useState(false);

  useEffect(() => {
    setLiked(isLiked);
  }, [setLiked, isLiked]);

  const handleClick = async () => {
    setLiked(!liked);
    if (isLoggedIn) {
      if (!liked) {
        try {
          const response = await fetch(`/api/like_article/${articleId}`, {
            credentials: 'include',
          });
          const data: Record<string, any> = response.json();
          if (data.success) {
            setLiked(true);
          }
        } catch (error) {
          console.error('Error adding like:', error);
        }
      } else {
        try {
          const response = await fetch(`/api/unlike_article/${articleId}`, {
            credentials: 'include',
          });
          const data: Record<string, any> = response.json();
          if (data.success) {
            setLiked(false);
          }
        } catch (error) {
          console.error('Error removing like:', error);
        }
      }
    } else {
      toast.error('You must be logged in.');
    }
    toast.success(liked ? 'Removed from likes.' : 'Added to likes.');
  };

  return !liked ? (
    <HeartIcon
      type='button'
      cursor='pointer'
      className={`h-10 w-10 text-gray-400 transition hover:text-red-500 ${liked ? 'text-red-500' : ''}`}
      onClick={handleClick}
    />
  ) : (
    <SolidHeartIcon
      type='button'
      cursor='pointer'
      className={`h-10 w-10 text-red-500 transition hover:drop-shadow-lg ${liked ? 'text-red-500' : ''}`}
      onClick={handleClick}
    />
  );
}
