import React, { Suspense } from 'react';
import { Metadata } from 'next';
import Loading from '@/app/ui/loading';
import StockTrends from '@/app/ui/stocks/stock-trends';
import Leaderboard from '@/app/ui/stocks/leaderboard';
import Rectangles from './Rectangles';
import { Poppins } from 'next/font/google'
import './style.css'

const pop = Poppins({ weight: ['600'], subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Stocks',
};

export default function Stocks() {
  return (
    <Suspense fallback={<Loading message={'Loading stocks...'} />}>
      <div style={{ marginTop: '26%' }}>
        <div className='dark-filter'>
          <Rectangles /></div> <div className='dark-o'></div>
      </div>
      <div className='dark-r'>
        <div className={pop.className}><span className="text-white" style={{ fontSize: '7rem' }}>Stocks</span></div></div>
      <hr className='mb-4 mt-3' style={{ backgroundColor: '#4C4B9B', height: '10px' }} />
      <div className='flex flex-col content-start justify-between gap-4 md:flex-row'>
        <StockTrends />
        <Leaderboard />
      </div>
    </Suspense >
  );
}
