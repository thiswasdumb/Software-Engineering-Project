'use client';
import React, { useEffect, useState } from 'react';
import {
  ArrowUpCircleIcon,
  ArrowDownCircleIcon,
  MinusCircleIcon,
} from '@heroicons/react/20/solid';
import Link from 'next/link';
import { Poppins } from 'next/font/google';
import './style.css'

const pop = Poppins({ weight: ['600'], subsets: ['latin'] });
const pop500 = Poppins({ weight: ['500'], subsets: ['latin'] });
const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });

export default function RecommendedArticles() {
  const [articles, setArticles] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/home_articles')
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
      <div className={pop500.className} style={{ fontSize: '2rem' }}><div className='underline-smpl'>Your suggested articles</div></div>
      {articles.length === 0 && <p>No suggested articles.</p>}
      <br />
      {articles.map((article, index) => (
        <div
          className='my-2 overflow-scroll rounded-lg bg-slate-100 p-2 transition hover:bg-slate-200 hover:drop-shadow-lg hover:border-2 hover:border-[#706fbf] border-2 border-[#c5c5ed]'
          key={index}
        >
          <Link href={`/article/${article.id}`}>
            <div className={pop500.className} style={{ fontSize: '1.2rem' }}>{article.title}</div>
            <hr className='border-2 my-2 rounded-lg border-[#706fbf]' />
            <div className={pop400.className}>{article.summary}</div>
            <div>
              {article.score > 0.5 ? (
                <div className='flex flex-row items-center'>
                  <ArrowUpCircleIcon className='h-12 w-12 text-green-500' />
                  <div className={pop500.className} style={{ color: '#4b4b9b' }}>Positive</div>
                </div>
              ) : article.score < 0.5 ? (
                <div className='flex flex-row items-center'>
                  <ArrowDownCircleIcon className='h-12 w-12 text-red-500 ' />
                  <div className={pop500.className} style={{ color: '#4b4b9b' }}>Negative</div>
                </div>
              ) : (
                <div className='flex flex-row items-center'>
                  <MinusCircleIcon className='h-12 w-12 text-slate-400' />
                  <div className={pop500.className} style={{ color: '#4b4b9b' }}>Neutral</div>
                </div>
              )}
            </div>
          </Link>
        </div>
      ))}
    </div>
  );
}
