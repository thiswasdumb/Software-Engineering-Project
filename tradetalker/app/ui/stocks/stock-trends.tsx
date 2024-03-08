import React from 'react';
import Link from 'next/link';

async function getStockTrends() {
  const response = await fetch('http://localhost:8080/api/get_stock_trends', {
    cache: 'no-store',
  });
  if (!response.ok) {
    throw new Error('Error fetching stock trends');
  }
  return response.json();
}

export default async function StockTrends() {
  const stockTrends: any[] = await getStockTrends();

  return (
    <div className='md:w-[70%]'>
      <h2 className='text-lg'>Top rising stocks</h2>
      {stockTrends.map((stock, index) => (
        <Link key={index} href={`/company/${stock.company_id}`}>
          <div className='mt-2 rounded-lg bg-slate-300 p-4 transition hover:bg-slate-400 hover:bg-opacity-40 hover:drop-shadow-lg'>
            <p className='font-bold'>{stock.symbol}</p>
            <p className='text-lg'>{stock.stock_price}</p>
            <p>
              Predicted stock price:&nbsp;
              {stock.predicted_stock_price !== null
                ? stock.predicted_stock_price
                : 'N/A'}
            </p>
            <p>
              Variance:&nbsp;
              {stock.stock_variance !== null ? stock.stock_variance : 'N/A'}
            </p>
          </div>
        </Link>
      ))}
    </div>
  );
}
