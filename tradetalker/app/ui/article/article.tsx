import React from 'react';
import Comments from './comments';
import { redirect } from 'next/navigation';
import Like from './like';
import Bookmark from './bookmark';

async function getArticle(id: string) {
  const response = await fetch(`http://localhost:8080/api/get_article/${id}`);
  if (!response.ok) {
    throw new Error('Error fetching article');
  }
  return response.json();
}

async function getLikeStatus(id: string) {
  const response = await fetch(
    `http://localhost:8080/api/get_article_like_status/${id}`,
    { credentials: 'include' }
  );
  if (!response.ok) {
    throw new Error('Error fetching like status');
  }
  return response.json();
}

async function getBookmarkStatus(id: string) {
  const response = await fetch(
    `http://localhost:8080/api/get_article_bookmark_status/${id}`,
    { credentials: 'include' }
  );
  if (!response.ok) {
    throw new Error('Error fetching bookmark status');
  }
  return response.json();
}

export default async function ArticlePage({
  id,
  isLoggedIn,
}: {
  id: string;
  isLoggedIn: boolean;
}) {
  const articleData = await getArticle(id);
  if (articleData.error) {
    redirect('/not-found');
  }

  let isLiked = false;
  let isBookmarked = false;
  // Get like status
  if (isLoggedIn) {
    try {
      const likeStatus = await getLikeStatus(id);
      isLiked = likeStatus.is_liked;
      const bookmarkStatus = await getBookmarkStatus(id);
      isBookmarked = bookmarkStatus.is_bookmarked;
    } catch (error) {
      console.error('Error fetching like status:', error);
    }
  }

  return (
    <div className='bg-slate-200 m-8 rounded-lg p-8'>
      <div className='flex flex-row justify-between'>
        <div>
          <div className='text-2xl'>{articleData.title}</div>
          <div className='text-slate-500 text-sm'>
            {formatDate(articleData.publication_date)}
          </div>
        </div>
        {isLoggedIn && (
          <div className='flex flex-row'>
            <Like isLiked={isLiked} />
            <Bookmark isBookmarked={isBookmarked} />
          </div>
        )}
      </div>

      <hr className='border-slate-400 my-2 rounded-lg border-2' />
      <div className='text-lg'>Company: {articleData.company_name}</div>
      <div className='text-lg'>Summary: {articleData.summary}</div>
      <hr className='border-1 border-slate-400 my-2 rounded-lg' />
      <div className='text-lg'>{articleData.content}</div>
      <hr className='border-1 border-slate-400 my-2 rounded-lg' />
      <Comments articleId={id} isLoggedIn={isLoggedIn} />
    </div>
  );
}

export function formatDate(string: string) {
  return new Date(string).toLocaleDateString();
}
