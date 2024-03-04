'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';

export default function NewsFeed() {
  const [articles, setArticles] = useState<any[]>([]);
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
      <div className='text-xl'>News feed</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <div className='flex flex-col'>
        {articles.length === 0 && <p>No recent news.</p>}
        {articles.map((article, index) => (
          <Link
            href={`/article/${article.id}`}
            key={index}
            className='opacity:30 my-2 w-full rounded-lg bg-slate-100 p-2 transition hover:bg-slate-200 hover:drop-shadow-lg'
          >
            <div>{article.title}</div>
            <div className='text-sm text-gray-500'>{article.date}</div>
            <div>{article.summary}</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
