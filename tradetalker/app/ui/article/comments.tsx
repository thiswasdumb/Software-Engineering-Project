'use client';
import React, { useState, useEffect } from 'react';
import { CommentForm, ReplyForm } from './comment-form';

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
      <hr className='border-slate-400 my-2 rounded-lg border-2' />
      <CommentForm articleId={articleId} isLoggedIn={isLoggedIn} />
      <div>
        {comments.map((comment, index) => (
          <div key={index} className='my-4'>
            <div className='flex flex-row items-end'>
              <div>{comment.username}</div>
              <div className='text-slate-500 ml-2 text-sm'>{comment.time}</div>
            </div>
            <div className='flex flex-row items-center'>
              <div>{comment.content}</div>
              <div>
                <button
                  className='bg-blue-500 text-white hover:bg-blue-600 ml-4 rounded-lg p-2 text-sm transition hover:drop-shadow-lg'
                  onClick={() => {}}
                >
                  Reply
                </button>
              </div>
            </div>
            {isLoggedIn && (
              <ReplyForm articleId={articleId} commentId={comment.id} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
