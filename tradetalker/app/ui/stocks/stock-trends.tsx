import React from 'react';
import Link from 'next/link';
import { Poppins } from 'next/font/google';

const pop = Poppins({ weight: ['600'], subsets: ['latin'] });
const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });

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
    <div className='md:w-[62%] mx-auto'>
      <div className={pop.className} style={{ fontSize: '2rem', marginLeft: '1rem' }}>
        <div className='underline-s'>Top Rising Stocks</div> </div>
      <br />
      <div className="grid gap-4">
        <div className={pop400.className} style={{ marginLeft: '1rem' }}>
          {stockTrends.map((stock, index) => (
            <Link key={index} href={`/company/${stock.company_id}`}>
              <div className='rounded-lg bg-slate-300 p-4 transition hover:bg-slate-400 hover:bg-opacity-40 hover:drop-shadow-lg'>
                <div className='font-bold'>{stock.symbol}</div>
                <div className='text-lg'>{stock.stock_price}</div>
                <div>
                  Predicted stock price:&nbsp;
                  {stock.predicted_stock_price !== null
                    ? stock.predicted_stock_price
                    : 'N/A'}
                </div>
                <div>
                  Variance:&nbsp;
                  {stock.stock_variance !== null ? stock.stock_variance : 'N/A'}
                </div>
              </div>

            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
