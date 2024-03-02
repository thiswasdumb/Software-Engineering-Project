'use client';
import React, { useEffect, useState } from 'react';

export function CommentForm({
  articleId,
  isLoggedIn,
}: {
  articleId: string;
  isLoggedIn: boolean;
}) {
  const [commentData, setCommentData] = useState<any[]>([]);

  useEffect(() => {
    setCommentData(commentData);
  }, [commentData]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const comment = formData.get('comment');
    if (comment) {
      const response = await fetch(
        `http://localhost:8080/api/add_article_comment/${articleId}`,
        {
          method: 'post',
          body: JSON.stringify({ articleId, comment }),
        }
      );
      if (response.ok) {
        const newComment = await response.json();
        commentData.push(newComment);
      }
    }
  };
  if (isLoggedIn) {
    return (
      <div className='flex w-full flex-row md:max-w-[80%]'>
        <form onSubmit={handleSubmit} method='post' className='w-full'>
          <input
            className='bg-white w-full rounded-lg p-2 transition hover:drop-shadow-lg'
            placeholder='Add a comment...'
            type='text'
            name='comment'
            maxLength={10000}
          />
        </form>
        <button
          type='button'
          className='bg-blue-500 text-white hover:bg-blue-600 ml-2 rounded-lg p-2 transition hover:drop-shadow-lg'
          onClick={() => handleSubmit}
        >
          Comment
        </button>
      </div>
    );
  } else {
    return (
      <div>
        <p>You must be logged in to comment.</p>
      </div>
    );
  }
}

export function ReplyForm({
  articleId,
}: {
  articleId: string;
  commentId: number;
}) {
  const [commentData, setCommentData] = useState<any[]>([]);

  useEffect(() => {
    setCommentData(commentData);
  }, [commentData]);

  const handleReplySubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const comment = formData.get('comment');
    if (comment) {
      const response = await fetch(
        `http://localhost:8080/api/add_article_reply/${articleId}`,
        {
          method: 'post',
          body: JSON.stringify({ articleId, comment }),
        }
      );
      if (response.ok) {
        const newComment = await response.json();
        commentData.push(newComment);
      }
    }
  };

  return (
    <form onSubmit={handleReplySubmit} method='post'>
      <input
        className='bg-blue-600 w-full rounded-lg p-2 hover:drop-shadow-lg'
        placeholder='Enter a reply...'
        type='text'
        name='reply'
      />
    </form>
  );
}
