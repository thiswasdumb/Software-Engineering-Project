import React from 'react';
import Link from 'next/link';
import {
  ArrowUpCircleIcon,
  ArrowDownCircleIcon,
  MinusCircleIcon,
} from '@heroicons/react/20/solid';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import ReadParams from '@/app/ui/read-params';

/**
 * Fetch the latest articles from the server
 * @returns Promise - The latest articles
 */
async function fetchArticles() {
  const response = await fetch('http://localhost:8080/api/home_articles', {
    cache: 'no-store',
  });
  if (!response.ok) {
    throw new Error('An error occurred while fetching the users.');
  }
  return response.json();
}

/**
 * Home page component
 * @returns Promise - Home page component
 */
export default async function HomeComponent() {
  const articles: any[] = await fetchArticles(); // Wait for the promise to resolve
  dayjs.extend(relativeTime);

  return (
    <>
      <ReadParams url='' />
      <div className='rounded-lg bg-slate-200 p-8 md:m-8'>
        <h1 className='text-2xl'>Welcome to TradeTalk.</h1>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <p>
          Stay informed about the latest news sentiment in the financial
          markets.
        </p>
        <br></br>
        <div className='rounded-lg bg-slate-300 p-4'>
          <h2 className='text-xl'>Recent articles</h2>
          {articles.map((article, index) => (
            <div
              className='my-2 rounded-lg bg-slate-100 p-2 transition hover:bg-blue-100 hover:drop-shadow-lg'
              key={index}
            >
              <Link href={`/article/${article.id}`}>
                <div className='flex flex-row flex-wrap items-center justify-between'>
                  <h3 className='mr-2 text-lg'>{article.title}</h3>
                  <span className='text-sm text-gray-600'>
                    {dayjs(article.date).fromNow()}
                  </span>
                </div>
                <hr className='border-1 my-2 rounded-lg border-slate-300' />
                <p>{article.summary}</p>
                <hr className='border-1 my-2 rounded-lg border-slate-300' />
                <div className='flex flex-row items-center justify-between'>
                  {article.score > 0.33 ? (
                    <div className='flex flex-row items-center'>
                      <ArrowUpCircleIcon className='h-10 w-10 text-green-500' />
                      <p className='pl-2 text-green-600'>Positive</p>
                    </div>
                  ) : article.score < -0.33 ? (
                    <div className='flex flex-row items-center'>
                      <ArrowDownCircleIcon className='h-10 w-10 text-red-600 ' />
                      <p className='pl-2 text-red-600'>Negative</p>
                    </div>
                  ) : (
                    <div className='flex flex-row items-center'>
                      <MinusCircleIcon className='h-10 w-10 text-slate-400' />
                      <p className='pl-2 text-slate-500'>Neutral</p>
                    </div>
                  )}
                </div>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
