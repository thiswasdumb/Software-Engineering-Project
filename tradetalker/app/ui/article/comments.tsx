'use client';
import React, { useState, useEffect } from 'react';
import { CommentForm } from './comment-form';

/**
 * Comments component.
 * @param articleId - Article ID
 * @param isLoggedIn - Flag to check if the user is logged in
 * @returns JSX.Element - Comments component
 */
export default function Comments({
  articleId,
  isLoggedIn,
}: {
  articleId: string;
  isLoggedIn: boolean;
}) {
  const [comments, setComments] = useState<any[]>([]);
  const [isVerified, setIsVerified] = useState(false);

  // Fetch the comments
  useEffect(() => {
    fetch(`/api/article/${articleId}/comments`)
      .then((response) => response.json())
      .then((data) => {
        setComments(data);
      })
      .catch((error) => console.error(error));
  }, [articleId, setComments]);

  // Check if the user is verified
  useEffect(() => {
    if (isLoggedIn) {
      fetch('/api/check_verified', { credentials: 'include' })
        .then((response) => response.json())
        .then((data) => {
          if (data.verified) {
            setIsVerified(true);
          }
        })
        .catch(() => {
          console.error('Error verifying user.');
        });
    }
  }, [isLoggedIn]);

  return (
    <div id='comments'>
      <h2 className='text-xl'>Comments ({comments.length})</h2>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <CommentForm
        articleId={articleId}
        isLoggedIn={isLoggedIn}
        isVerified={isVerified}
      />
      <div>
        {comments.map((comment, index) => (
          <div key={index} className='my-4'>
            <div className='flex flex-row items-end'>
              <div>{comment.username}</div>
              <div className='ml-2 text-sm text-slate-500'>{comment.time}</div>
            </div>
            <div className='flex flex-row items-center'>
              <p>{comment.content}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
