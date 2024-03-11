import React from 'react';
import Link from 'next/link';
import { Poppins } from 'next/font/google';

const pop = Poppins({ weight: ['600'], subsets: ['latin'] });
const pop500 = Poppins({ weight: ['500'], subsets: ['latin'] });
const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });

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
    <div className='md:w-[62%] mx-auto'>
      <div className={pop.className} style={{ fontSize: '2rem', marginLeft: '1rem' }}>
        <div className='underline-s'>Top Rising Stocks</div>
      </div>
      <br />
      <div className="grid gap-4">
        <div className={pop400.className} style={{ marginLeft: '0.8rem', marginTop: '1rem' }}>
          {stockTrends.map((stock, index) => (
            <Link key={index} href={`/company/${stock.company_id}`}>
              <div className={`stock-item rounded-lg p-4 transition text-white hover:bg-slate-400 hover:bg-opacity-40 hover:drop-shadow-lg`} style={{ backgroundColor: getBackgroundColor(stock.predicted_stock_price, index, 25) }}>
                <div className={pop.className}>{stock.symbol}</div>
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
              <div style={{ marginTop: '0.7rem' }}> </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

function getBackgroundColor(predictedStockPrice, index, totalStocks) {
  // Base color
  const baseColor = [76, 75, 155];

  // Maximum brightness adjustment (brighter colors) for higher predicted prices
  const maxBrightness = 250;

  // Calculate brightness adjustment based on predicted stock price
  const brightness = (1 - predictedStockPrice / 1000) * maxBrightness;

  // Generate the new color with adjusted brightness
  const newColor = baseColor.map(component => Math.min(255, Math.max(0, component + brightness)));

  // Convert the color components to CSS format
  return `rgb(${newColor.join(', ')})`;
}



