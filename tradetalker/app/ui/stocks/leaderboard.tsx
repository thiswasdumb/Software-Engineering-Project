import React from 'react';
import Link from 'next/link';

/**
 * Fetch the leaderboard.
 * @returns Promise - Leaderboard data
 */
async function getLeaderboard() {
  const response = await fetch('http://localhost:8080/api/get_leaderboard', {
    cache: 'no-store',
  });
  if (!response.ok) {
    throw new Error('Error fetching leaderboard');
  }
  return response.json();
}

/**
 * Stock trends component.
 * @returns Promise - StockTrends component
 */
export default async function Leaderboard() {
  const leaderboard: any[] = await getLeaderboard(); // Wait for the promise to resolve

  return (
    <div className='md:w-[30%]'>
      <h2 className='text-lg'>Top stocks today</h2>
      <div className='mt-2 rounded-lg bg-slate-300 p-4'>
        {leaderboard.map((company, index) => (
          <Link key={index} href={`/company/${company.company_id}`}>
            <div className='my-2 flex flex-row rounded-lg bg-slate-100 p-2 transition hover:bg-blue-100 hover:drop-shadow-lg'>
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
  );
}
