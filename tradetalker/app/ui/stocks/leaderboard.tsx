import React from 'react';
import Link from 'next/link';

async function getLeaderboard() {
  const response = await fetch('http://localhost:8080/api/get_leaderboard', {
    cache: 'no-store',
  });
  if (!response.ok) {
    throw new Error('Error fetching leaderboard');
  }
  return response.json();
}

export default async function StockTrends() {
  const leaderboard: any[] = await getLeaderboard();

  return (
    <div className='md:w-[30%]'>
      <div className='text-lg'>Top stocks today</div>
      <div className='mt-2 rounded-lg bg-slate-300 p-4'>
        {leaderboard.map((company, index) => (
          <Link key={index} href={`/company/${company.company_id}`}>
            <div className='my-2 flex flex-row rounded-lg bg-slate-100 p-2 transition hover:bg-blue-100 hover:drop-shadow-lg'>
              <div className='text-lg font-bold'>{index + 1}</div>
              <div className='ml-2 flex flex-col'>
                <div className='font-bold'>{company.company_symbol}</div>
                <div className='text-sm'>{company.company_name}</div>
                <p>{company.stock_price}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
