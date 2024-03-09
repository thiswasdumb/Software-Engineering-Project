import React from 'react';
import Link from 'next/link';

/**
 * Fetch the stock price leaderboard.
 * @returns Promise - Leaderboard data
 */
async function getArticlesLeaderboard() {
  const response = await fetch(
    'http://localhost:8080/api/get_most_positive_leaderboard',
    {
      cache: 'no-store',
    }
  );
  if (!response.ok) {
    throw new Error('Error fetching leaderboard');
  }
  return response.json();
}

/**
 * Stock price leaderboard component.
 * @returns Promise - Stock price leaderboard component
 */
export default async function PositiveArticleLeaderboard() {
  const leaderboard: any[] = await getArticlesLeaderboard(); // Wait for the promise to resolve

  return (
    <div className='md:w-[30%]'>
      <div className='mt-2 rounded-lg bg-slate-300 p-4'>
        <h2 className='mb-2 text-lg'>Most positive companies</h2>
        <div className='max-h-[60vh] overflow-scroll rounded-lg'>
          {leaderboard.map((company, index) => (
            <Link key={index} href={`/company/${company.company_id}`}>
              <div className='mb-2 flex flex-row rounded-lg bg-slate-100 p-2 transition hover:bg-blue-100 hover:drop-shadow-lg'>
                <span className='text-lg font-bold'>{index + 1}</span>
                <div className='ml-2 flex flex-col'>
                  <p className='font-bold'>{company.company_symbol}</p>
                  <p className='text-sm'>{company.company_name}</p>
                  <p>{company.stock_price}</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
