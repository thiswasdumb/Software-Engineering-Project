'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import FollowButton from '../company/follow-button';
import { Poppins } from 'next/font/google';
import './style.css';

const pop = Poppins({ weight: ['600'], subsets: ['latin'] });
const pop500 = Poppins({ weight: ['500'], subsets: ['latin'] });
const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });

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
    <div className='my-2 rounded-lg p-4' style={{ backgroundColor: '#7977d1' }}>
      <div className='underline-white text-white'>
        <div
          className={pop.className}
          style={{ fontSize: '1.2rem', marginBottom: '1%' }}
        >
          News Feed
        </div>
      </div>
      <div className='flex flex-col text-white' style={{ marginTop: '2%' }}>
        <div className={pop400.className}>
          <div className='flex flex-col text-black rounded-lg max-h-[40vh] overflow-scroll'>
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
    </div>
  );
}
