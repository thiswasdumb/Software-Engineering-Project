'use client';
import React, { useEffect, useState } from 'react';
import {
  ArrowUpCircleIcon,
  ArrowDownCircleIcon,
  MinusCircleIcon,
} from '@heroicons/react/20/solid';
import Link from 'next/link';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import CommentsButton from '@/app/ui/comments-button';

export default function RecommendedArticles() {
  const [articles, setArticles] = useState<any[]>([]);
  dayjs.extend(relativeTime);

  useEffect(() => {
    fetch('/api/home_articles') // Replace with actual route
      .then((response) => response.json())
      .then((data) => {
        setArticles(data);
      })
      .catch((error) => {
        console.error('Error fetching articles:', error);
      });
  }, [setArticles]);

  return (
    <div className='my-2 rounded-lg bg-slate-300 p-4'>
      <h2 className='text-xl'>Your suggested articles</h2>
      {articles.length === 0 && <p>No suggested articles.</p>}
      {articles.map((article, index) => (
        <div
          className='my-2 overflow-scroll rounded-lg bg-slate-100 p-2 transition hover:bg-blue-100 hover:drop-shadow-lg'
          key={index}
        >
          <Link href={`/article/${article.id}`}>
            <div className='flex flex-row flex-wrap items-center justify-between'>
              <p className='text-lg'>{article.title}</p>
              <p className='text-sm text-gray-600'>
                {dayjs(article.date).fromNow()}
              </p>
            </div>
            <hr className='border-1 my-2 rounded-lg border-slate-300' />
            <p>{article.summary}</p>
            <hr className='border-1 my-2 rounded-lg border-slate-300' />
            <div className='flex flex-row items-center justify-between'>
              {article.score > 0.5 ? (
                <div className='flex flex-row items-center'>
                  <ArrowUpCircleIcon className='h-10 w-10 text-green-600' />
                  <p className='pl-2 text-green-600'>Positive</p>
                </div>
              ) : article.score < 0.5 ? (
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
              <CommentsButton id={article.id} comments={article.comments} />
            </div>
          </Link>
        </div>
      ))}
    </div>
  );
}
