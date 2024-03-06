'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

export default function NewsFeed() {
  const [articles, setArticles] = useState<any[]>([]);
  dayjs.extend(relativeTime);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await fetch('/api/get_newsfeed');
        const data = await response.json();
        setArticles(data);
      } catch (error) {
        console.error('Error fetching articles:', error);
      }
    };
    fetchArticles();
  }, [setArticles]);

  return (
    <div className='my-2 rounded-lg bg-slate-300 p-4'>
      <h2 className='text-xl'>News feed</h2>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <div className='flex flex-col'>
        {articles.length === 0 && <p>No recent news.</p>}
        {articles.map((article, index) => (
          <Link
            href={`/article/${article.id}`}
            key={index}
            className='opacity:30 my-2 w-full rounded-lg bg-slate-100 p-2 transition hover:bg-slate-200 hover:drop-shadow-lg'
          >
            <div className='flex flex-row flex-wrap items-center justify-between'>
              <p>{article.title}</p>
              <p className='text-sm text-gray-500'>
                {dayjs(article.date).fromNow()}
              </p>
            </div>
            <p className='text-sm'>{article.summary}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
