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
import { Poppins } from 'next/font/google';
import './style.css';

const pop = Poppins({ weight: ['600'], subsets: ['latin'] });
const pop500 = Poppins({ weight: ['500'], subsets: ['latin'] });
const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });

/**
 * Recommended articles component
 * @returns JSX.Element - Recommended articles component
 */
export default function RecommendedArticles() {
  const [articles, setArticles] = useState<any[]>([]);
  dayjs.extend(relativeTime);

  // Fetch the latest 3 articles from the past week
  useEffect(() => {
    fetch('/api/get_recommended_articles') // Replace with actual route
      .then((response) => response.json())
      .then((data) => {
        setArticles(data);
      })
      .catch((error) => {
        console.error('Error fetching articles:', error);
      });
  }, [setArticles]);

  return (
    <div className='my-2'>
      <div className={pop500.className} style={{ fontSize: '2rem' }}>
        <div className='underline-smpl'>Your suggested articles</div>
      </div>
      {articles.length === 0 && (
        <p>No new articles. Start following some companies!</p>
      )}
      {articles.map((article, index) => (
        <div
          className='my-2 overflow-scroll rounded-lg border-2 border-[#c5c5ed] bg-slate-100 p-2 transition hover:border-2 hover:border-[#706fbf] hover:bg-slate-200 hover:drop-shadow-lg'
          key={index}
        >
          <Link href={`/article/${article.id}`}>
            <div className='flex flex-row flex-wrap items-center justify-between'>
              <div className={pop500.className} style={{ fontSize: '1.2rem' }}>
                {article.title}
              </div>
              <p className='text-sm text-gray-600'>
                {dayjs(article.date).fromNow()}
              </p>
            </div>
            <hr className='my-2 rounded-lg border-2 border-[#706fbf]' />
            <div className={pop400.className}>{article.summary}</div>
            <hr className='my-2 rounded-lg border-2 border-[#706fbf]' />
            <div className='flex flex-row items-center justify-between'>
              {article.score > 0.5 ? (
                <div className='flex flex-row items-center'>
                  <ArrowUpCircleIcon className='h-10 w-10 text-green-500' />
                  <div
                    className={pop500.className}
                    style={{ color: '#4b4b9b' }}
                  >
                    Positive
                  </div>
                </div>
              ) : article.score < -0.5 ? (
                <div className='flex flex-row items-center'>
                  <ArrowDownCircleIcon className='h-12 w-12 text-red-500 ' />
                  <div
                    className={pop500.className}
                    style={{ color: '#4b4b9b' }}
                  >
                    Negative
                  </div>
                </div>
              ) : (
                <div className='flex flex-row items-center'>
                  <MinusCircleIcon className='h-12 w-12 text-slate-400' />
                  <div
                    className={pop500.className}
                    style={{ color: '#4b4b9b' }}
                  >
                    Neutral
                  </div>
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
