import React, { Suspense } from 'react';
import { Metadata } from 'next';
import Loading from '@/app/ui/loading';
import StockTrends from '@/app/ui/stocks/stock-trends';
import StockPriceLeaderboard from '@/app/ui/stocks/stock-price-leaderboard';
import PositiveArticleLeaderboard from '../ui/stocks/positive-article-leaderboard';

export const metadata: Metadata = {
  title: 'Stocks',
};

/**
 * Stocks page.
 * @returns JSX.Element - Stocks page component
 */
export default function Stocks() {
  return (
    <Suspense fallback={<Loading message={'Loading stocks...'} />}>
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='text-2xl'>Stocks</div>
        <hr className='mt-2 rounded-lg border-2 border-slate-400' />
        <div className='flex flex-col gap-2 md:flex-row'>
          <StockTrends />
          <StockPriceLeaderboard />
          <PositiveArticleLeaderboard />
        </div>
      </div>
    </Suspense>
  );
}
