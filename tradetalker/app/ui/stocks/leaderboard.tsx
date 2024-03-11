import React from 'react';
import Link from 'next/link';
import { Poppins } from 'next/font/google';

const pop = Poppins({ weight: ['600'], subsets: ['latin'] });
const pop500 = Poppins({ weight: ['500'], subsets: ['latin'] });
const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });

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
    <div className='md:w-[33%]'>
      <div className={pop.className} style={{ fontSize: '1.5rem', marginRight: '1rem', marginTop: '1.2rem' }}>
        <div className='underline-s'>
          <div className=''>Top Stocks Today</div></div></div> <br />
      <div className={pop400.className} style={{ marginRight: '1rem', marginBottom: '1rem' }}>
        <div className='mt-2 rounded-lg bg-slate-300 p-4' style={{ backgroundColor: '#9795e6' }}>
          {leaderboard.map((company, index) => (
            <Link key={index} href={`/company/${company.company_id}`}>
              <div className='leaderboard-item my-2 flex flex-row rounded-lg bg-slate-100 p-2 transition'>
                <div className='ml-2 flex flex-col items-start'>
                  <div className={pop500.className}>{company.company_name}</div>
                  <div>{company.stock_price}</div>
                </div>

              </div>
            </Link>
          ))}
        </div>
      </div>
    </div >
  );
}
