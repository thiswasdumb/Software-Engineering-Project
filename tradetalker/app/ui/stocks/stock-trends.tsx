import React from 'react';
import Link from 'next/link';

async function getStockTrends() {
  const response = await fetch('http://localhost:8080/api/get_stock_trends');
  if (!response.ok) {
    throw new Error('Error fetching stock trends');
  }
  return response.json();
}

export default async function StockTrends() {
  const stockTrends: any[] = await getStockTrends();

  return (
    <div className='md:w-[70%]'>
      <div className='text-base'>Top rising stocks</div>
      {stockTrends.map((stock, index) => (
        <Link key={index} href={`/company/${stock.company_id}`}>
          <div className='mt-2 rounded-lg bg-slate-300 p-4 transition hover:bg-slate-400 hover:bg-opacity-40 hover:drop-shadow-lg'>
            <div className='font-bold'>{stock.symbol}</div>
            <div className='text-lg'>{stock.stock_price}</div>
            <div>Predicted stock price: {stock.predicted_stock_price}</div>
            <div>Variance: {stock.stock_variance}</div>
          </div>
        </Link>
      ))}
    </div>
  );
}
