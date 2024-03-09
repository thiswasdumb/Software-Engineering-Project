'use client';
import React, { useEffect, useState } from 'react';
import toast from 'react-hot-toast';

/**
 * Comment form component.
 * @param articleId - Article ID
 * @param isLoggedIn - Flag to check if the user is logged in
 * @param isVerified - Flag to check if the user is verified
 * @returns JSX.Element - Comment form component
 */
export function CommentForm({
  articleId,
  isLoggedIn,
  isVerified,
}: {
  articleId: string;
  isLoggedIn: boolean;
  isVerified: boolean;
}) {
  const [commentData, setCommentData] = useState<any[]>([]);
  const [comment, setComment] = useState('');

  // Set the comment data
  useEffect(() => {
    setCommentData(commentData);
  }, [commentData]);

  // Handle the comment form submission
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    fetch(`/api/add_article_comment/${articleId}`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ articleId, comment }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          toast.error(data.error);
        }
        if (data.success) {
          window.location.reload(); // Reload the page to show the new comment
          setComment('');
        }
      })
      .catch((error) => console.error(error));
  };

  // Return the comment form if the user is logged in and verified
  if (isLoggedIn && isVerified) {
    return (
      <div className='flex w-full flex-row md:max-w-[80%]'>
        <form
          onSubmit={handleSubmit}
          method='post'
          className='flex w-full flex-row'
        >
          <label className='hidden' htmlFor='comment'>
            Comment
          </label>
          <input
            className='w-full rounded-lg bg-white p-2 transition hover:drop-shadow-lg'
            placeholder='Add a comment...'
            type='text'
            name='comment'
            minLength={1}
            maxLength={10000}
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            required
          />
          <button
            type='submit'
            className='ml-2 rounded-lg bg-blue-500 p-2 text-white transition hover:bg-blue-600 hover:drop-shadow-lg'
          >
            Comment
          </button>
        </form>
      </div>
    );
  } else {
    if (isLoggedIn && !isVerified) {
      return (
        <div>
          <p>You must be verified before you can comment.</p>
        </div>
      );
    } else {
      return (
        <div>
          <p>
            You must&nbsp;
            <a
              href='/login'
              className='text-blue-600 underline hover:text-blue-700 active:text-orange-400'
            >
              log in
            </a>
            &nbsp;and be verified before you can comment.
          </p>
        </div>
      );
    }
  }
}

/**
 * Reply form component.
 * @param articleId - Article ID
 * @param commentId - Comment ID
 * @returns JSX.Element - Reply form component
 */
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

  // Handle the reply form submission
  const handleReplySubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const comment = formData.get('comment');
    if (comment) {
      const response = await fetch(
        `http://localhost:8080/api/add_article_reply/${articleId}`,
        {
          method: 'POST',
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
        className='w-full rounded-lg bg-white p-2 hover:drop-shadow-lg'
        placeholder='Enter a reply...'
        type='text'
        name='reply'
      />
    </form>
  );
}
