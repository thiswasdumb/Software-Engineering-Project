import React from 'react';
import Link from 'next/link';
import SlidingRoundedRectangle from './SlidingRoundedRectangle';
import { Poppins } from 'next/font/google';
import './style.css';

const pop = Poppins({ weight: ['600'], subsets: ['latin'] });
const pop500 = Poppins({ weight: ['500'], subsets: ['latin'] });
const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });

async function getCompanies() {
  const response = await fetch('http://localhost:8080/api/get_companies');
  if (!response.ok) {
    throw new Error('Error fetching companies');
  }
  return response.json();
}

export default async function CompaniesComponent() {
  const companies: any[] = await getCompanies();

  // Base number to adjust brightness
  const baseBrightnessMultiplier = 0.00001;

  // Function to calculate brightness based on stock price
  const calculateBrightness = (stockPrice: number) => {
    // Adjust brightness based on stock price
    const brightness = 0.7 - stockPrice * baseBrightnessMultiplier * 2.5;
    return Math.max(0, brightness); // Ensure brightness is between 0 and 1
  };

  return (
    <div className="">
      <SlidingRoundedRectangle />
      <SlidingRoundedRectangle />
      <SlidingRoundedRectangle />
      <SlidingRoundedRectangle />
      <SlidingRoundedRectangle />
      <SlidingRoundedRectangle />
      <SlidingRoundedRectangle />
      <div className="overdark"></div>
      <div className="recdark">
        <div className={pop.className} style={{ fontSize: '7rem' }}>
          Companies
        </div>
      </div>
      <hr
        className="mb-4 mt-3"
        style={{ backgroundColor: '#4C4B9B', height: '10px', marginTop: '-0.17%' }}
      />
      <div className="flex justify-center">
        <div className="flex flex-row flex-wrap justify-center">
          {companies.map((company, index) => (
            <Link
              href={`/company/${company.id}`}
              key={index}
              className="linkcontainer max-w-4 opacity:30 my-2 w-full rounded-lg p-2 transition hover:bg-opacity-40 hover:drop-shadow-lg md:m-2 md:w-[30%]"
              style={{
                backgroundColor: `rgba(113, 112, 196, ${calculateBrightness(company.stock_price)})`,
              }}
            >
              <div>
                <span className={pop.className}>{company.symbol}&nbsp;|&nbsp;</span>
                <span className={pop500.className}>{company.name}</span>
              </div>
              <span className={pop400.className}>{company.stock_price}</span>
              <div className={pop400.className}>{company.industry}</div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
