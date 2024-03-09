import React from 'react';
import Comments from './comments';
import { redirect } from 'next/navigation';
import Like from './like';
import Bookmark from './bookmark';
import Link from 'next/link';
import ScrollUp from '@/app/ui/scroll-up';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import { ClockIcon } from '@heroicons/react/24/outline';

/**
 * Get article data from the server.
 * @param id - Article ID
 * @returns Promise - Article data
 */
async function getArticle(id: string) {
  const response = await fetch(`http://localhost:8080/api/get_article/${id}`);
  if (!response.ok) {
    throw new Error('Error fetching article');
  }
  return response.json();
}

/**
 * Article page component.
 * @param id - Article ID
 * @param isLoggedIn - Flag to check if the user is logged in
 * @returns JSX.Element - Article page component
 */
export default async function ArticlePage({
  id,
  isLoggedIn,
}: {
  id: string;
  isLoggedIn: boolean;
}) {
  const articleData = await getArticle(id);
  if (articleData.error) {
    redirect('/not-found'); // Redirect to 404 page if article is not found
  }
  dayjs.extend(relativeTime); // Extend dayjs with relativeTime plugin

  return (
    <>
      <ScrollUp />
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='flex flex-row justify-between'>
          <div>
            <h1 className='text-2xl'>{articleData.title}</h1>
            <span className='flex flex-row items-center text-sm text-slate-500'>
              {dayjs(articleData.publication_date).format('D MMMM YYYY')}
              <ClockIcon className='mx-1 inline-block h-4 w-4' />
              {dayjs(articleData.publication_date).fromNow()}
            </span>
          </div>
          {isLoggedIn && (
            <div className='flex flex-row'>
              <Like articleId={id} isLoggedIn={isLoggedIn} />
              <Bookmark articleId={id} isLoggedIn={isLoggedIn} />
            </div>
          )}
        </div>

        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <div className='flex flex-row flex-wrap items-start justify-between'>
          <div>
            <div>
              {articleData.prediction_score > 0.33 ? (
                <p className='text-green-600'>
                  Positive ({articleData.prediction_score.toFixed(2)})
                </p>
              ) : articleData.prediction_score < -0.33 ? (
                <p className='text-red-600'>
                  Negative ({articleData.prediction_score.toFixed(2)})
                </p>
              ) : (
                <p className='text-gray-400'>
                  Neutral ({articleData.prediction_score.toFixed(2)})
                </p>
              )}
            </div>
            <div>
              Company:&nbsp;
              <Link
                className='underline hover:drop-shadow-lg'
                href={`/company/${articleData.company_id}`}
              >
                {articleData.company_name}
              </Link>
            </div>
            <p>Summary: {articleData.summary}</p>
          </div>
        </div>
        <hr className='border-1 my-2 rounded-lg border-slate-400' />
        <p className='mb-4'>{articleData.content}</p>
        <a
          href={articleData.url}
          target='_blank'
          className='text-blue-600 underline hover:text-blue-500 active:text-orange-400'
        >
          {articleData.url}
        </a>
        <hr className='border-1 my-2 rounded-lg border-slate-400' />
        <Comments articleId={id} isLoggedIn={isLoggedIn} />
      </div>
    </>
  );
}
