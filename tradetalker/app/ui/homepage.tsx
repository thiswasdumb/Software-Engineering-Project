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
      <div className='bg-slate-200 m-8 rounded-lg p-8'>
        <div className='text-2xl'>Welcome to TradeTalker.</div>
        <hr className='border-slate-400 my-2 rounded-lg border-2' />
        <p>
          Stay informed about the latest news sentiment in the financial
          markets.
        </p>
        <br></br>
        <div className='bg-slate-300 rounded-lg p-4'>
          <div className='text-xl'>Recent articles</div>
          {articles.map((article, index) => (
            <div
              className='bg-slate-100 hover:bg-slate-200 my-2 overflow-scroll rounded-lg p-2 transition hover:drop-shadow-lg'
              key={index}
            >
              <Link href={`/article/${article.id}`}>
                <div>{article.title}</div>
                <hr className='border-1 border-slate-300 my-2 rounded-lg' />
                <div>{article.summary}</div>
                <div>
                  {article.score > 0.5 ? (
                    <div className='flex flex-row items-center'>
                      <ArrowUpCircleIcon className='text-green-500 h-12 w-12' />
                      <div className='pl-2'>Positive</div>
                    </div>
                  ) : article.score < 0.5 ? (
                    <div className='flex flex-row items-center'>
                      <ArrowDownCircleIcon className='text-red-500 h-12 w-12 ' />
                      <div className='pl-2'>Negative</div>
                    </div>
                  ) : (
                    <div className='flex flex-row items-center'>
                      <MinusCircleIcon className='text-slate-400 h-12 w-12' />
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
