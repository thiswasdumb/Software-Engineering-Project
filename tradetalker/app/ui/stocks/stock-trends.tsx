import React from 'react';
import Link from 'next/link';

/**
 * Get stock trends
 * @returns Promise - Stock trends
 */
async function getStockTrends() {
  const response = await fetch('http://localhost:8080/api/get_stock_trends', {
    cache: 'no-store',
  });
  if (!response.ok) {
    throw new Error('Error fetching stock trends');
  }
  return response.json();
}

/**
 * Stock trends component
 * @returns Promise - StockTrends component
 */
export default async function StockTrends() {
  const stockTrends: any[] = await getStockTrends();

  return (
    <div className='md:w-[40%]'>
      <div className='mt-2 rounded-lg bg-slate-300 p-4'>
        <h2 className='mb-2 text-lg'>Top 25 predicted rising stocks</h2>
        <div className='max-h-[60vh] overflow-scroll rounded-lg'>
          {stockTrends.map((stock, index) => (
            <Link key={index} href={`/company/${stock.company_id}`}>
              <div className='mb-2 flex flex-row gap-2 rounded-lg bg-slate-100 p-2 transition hover:bg-blue-100 hover:drop-shadow-lg'>
                <span className='text-lg font-bold'>{index + 1}</span>
                <div>
                  <span className='flex flex-row items-center gap-2'>
                    <p className='font-bold'>{stock.symbol}</p>|
                    <p className='text-sm'>{stock.company_name}</p>
                  </span>
                  <p className='text-lg'>{stock.stock_price}</p>
                  <p>
                    Predicted stock price in 7 days:&nbsp;
                    {stock.predicted_stock_price !== null
                      ? stock.predicted_stock_price
                      : 'N/A'}
                  </p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
