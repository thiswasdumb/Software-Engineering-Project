import React from 'react';
import Link from 'next/link';

async function getLeaderboard() {
  const response = await fetch('http://localhost:8080/api/get_leaderboard');
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
            <div className='my-2 flex flex-row rounded-lg bg-slate-100 p-2 transition hover:bg-slate-200 hover:drop-shadow-lg'>
              <div className='text-lg font-bold'>{index + 1}</div>
              <div className='ml-2 flex flex-col items-start'>
                <div>{company.company_name}</div>
                <div>{company.stock_price}</div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
