'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

/**
 * NewsFeed component
 * @returns JSX.Element - NewsFeed component
 */
export default function NewsFeed() {
  const [articles, setArticles] = useState<any[]>([]);
  const [clicked, setClicked] = useState(false);
  dayjs.extend(relativeTime);

  // Fetch the latest 3 articles from the past week
  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await fetch('/api/get_week_newsfeed');
        const data = await response.json();
        setArticles(data);
      } catch (error) {
        console.error('Error fetching articles:', error);
      }
    };
    fetchArticles();
  }, [setArticles]);

  // When button is clicked, hide the button and fetch all articles from the past week
  const handleClick = async () => {
    setClicked(true);
    await fetchFullWeekArticles();
  };

  // Fetch all articles from the past week
  const fetchFullWeekArticles = async () => {
    try {
      const response = await fetch('/api/get_week_newsfeed_full');
      const data = await response.json();
      setArticles(data);
    } catch (error) {
      console.error('Error fetching articles:', error);
    }
  };

  return (
    <div className='my-2 rounded-lg bg-slate-300 p-4'>
      <h2 className='text-xl'>News feed</h2>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <div className='flex max-h-[60vh] flex-col overflow-scroll rounded-lg'>
        {articles.length === 0 && <p>No recent news.</p>}
        {articles.map((article, index) => (
          <Link
            href={`/article/${article.id}`}
            key={index}
            className='opacity:30 my-2 w-full rounded-lg bg-slate-100 p-2 transition hover:bg-blue-100 hover:drop-shadow-lg'
          >
            <div className='flex flex-row flex-wrap items-center justify-between'>
              <span className='mr-2'>{article.title}</span>
              <span className='text-sm text-gray-500'>
                {dayjs(article.date).fromNow()}
              </span>
            </div>
            <p className='text-sm'>{article.summary}</p>
          </Link>
        ))}
      </div>
      {!clicked && (
        <button
          onClick={() => handleClick()}
          className='mt-2 w-full rounded-lg bg-slate-400 p-2 text-white transition hover:bg-slate-500 active:bg-slate-600'
        >
          Show all articles from the past week
        </button>
      )}
    </div>
  );
}
