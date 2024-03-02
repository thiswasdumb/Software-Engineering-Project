'use client';
import React, { useState, useEffect } from 'react';
import { HeartIcon } from '@heroicons/react/24/outline';
import { HeartIcon as SolidHeartIcon } from '@heroicons/react/24/solid';

export default function Like({ isLiked }: { isLiked: boolean }) {
  const [liked, setLiked] = useState(false);

  useEffect(() => {
    setLiked(isLiked);
  }, [setLiked, isLiked]);

  const handleClick = () => {
    setLiked(!liked); // Set liked to its opposite value
  };

  return !liked ? (
    <HeartIcon
      type='button'
      cursor='pointer'
      className={`text-gray-400 hover:text-red-500 h-10 w-10 transition ${liked ? 'text-red-500' : ''}`}
      onClick={handleClick}
    />
  ) : (
    <SolidHeartIcon
      type='button'
      cursor='pointer'
      className={`text-red-500 h-10 w-10 transition hover:drop-shadow-lg ${liked ? 'text-red-500' : ''}`}
      onClick={handleClick}
    />
  );
}
