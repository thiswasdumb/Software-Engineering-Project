'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import FollowButton from '../company/follow-button';
import { Poppins } from 'next/font/google';
import './style.css'

const pop = Poppins({ weight: ['600'], subsets: ['latin'] });
const pop500 = Poppins({ weight: ['500'], subsets: ['latin'] });
const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });

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
    <div className='my-2 rounded-lg p-4' style={{ backgroundColor: '#7977d1' }}>
      <div className='text-white underline-white'><div className={pop.className} style={{ fontSize: '1.2rem', marginBottom: '1%' }}>News Feed</div></div>
      <div className='flex flex-col text-white' style={{ marginTop: '2%' }}><div className={pop400.className}>
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
    </div>
  );
}
