import React from 'react';
import Link from 'next/link';
import {
  ArrowUpCircleIcon,
  ArrowDownCircleIcon,
  MinusCircleIcon,
} from '@heroicons/react/20/solid';

async function fetchArticles() {
  const response = await fetch('http://localhost:8080/api/home_articles', {
    next: { revalidate: 0 },
  });
  if (!response.ok) {
    throw new Error('An error occurred while fetching the users.');
  }
  return response.json();
}

export default async function HomeComponent() {
  const articles: any[] = await fetchArticles(); // Wait for the promise to resolve

  return (
    <>
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='text-2xl'>Welcome to TradeTalker.</div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <p>
          Stay informed about the latest news sentiment in the financial
          markets.
        </p>
        <br></br>
        <div className='rounded-lg bg-slate-300 p-4'>
          <div className='text-xl'>Recent articles</div>
          {articles.map((article, index) => (
            <div
              className='my-2 overflow-scroll rounded-lg bg-slate-100 p-2 transition hover:bg-slate-200 hover:drop-shadow-lg'
              key={index}
            >
              <Link href={`/article/${article.id}`}>
                <div>{article.title}</div>
                <hr className='border-1 my-2 rounded-lg border-slate-300' />
                <div>{article.summary}</div>
                <div>
                  {article.score > 0.5 ? (
                    <div className='flex flex-row items-center'>
                      <ArrowUpCircleIcon className='h-12 w-12 text-green-500' />
                      <div className='pl-2'>Positive</div>
                    </div>
                  ) : article.score < 0.5 ? (
                    <div className='flex flex-row items-center'>
                      <ArrowDownCircleIcon className='h-12 w-12 text-red-500 ' />
                      <div className='pl-2'>Negative</div>
                    </div>
                  ) : (
                    <div className='flex flex-row items-center'>
                      <MinusCircleIcon className='h-12 w-12 text-slate-400' />
                      <div className='pl-2'>Neutral</div>
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
