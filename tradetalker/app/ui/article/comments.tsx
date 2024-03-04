'use client';
import React, { useState, useEffect } from 'react';
import { CommentForm } from './comment-form';

export default function Comments({
  articleId,
  isLoggedIn,
}: {
  articleId: string;
  isLoggedIn: boolean;
}) {
  const [comments, setComments] = useState<any[]>([]);

  useEffect(() => {
    fetch(`/api/article/${articleId}/comments`)
      .then((response) => response.json())
      .then((data) => {
        setComments(data);
      })
      .catch((error) => console.error(error));
  }, [articleId, setComments]);

  return (
    <div>
      <div className='text-xl'>Comments ({comments.length})</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <CommentForm articleId={articleId} isLoggedIn={isLoggedIn} />
      <div>
        {comments.map((comment, index) => (
          <div key={index} className='my-4'>
            <div className='flex flex-row items-end'>
              <div>{comment.username}</div>
              <div className='ml-2 text-sm text-slate-500'>{comment.time}</div>
            </div>
            <div className='flex flex-row items-center'>
              <div>{comment.content}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
