import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import FollowButton from '../company/follow-button';
import { Poppins } from 'next/font/google';
import './style.css'

const pop = Poppins({ weight: ['600'], subsets: ['latin'] });
const pop500 = Poppins({ weight: ['500'], subsets: ['latin'] });
const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });

export default function RecommendedCompanies({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [companies, setCompanies] = useState<any[]>([]);
  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const data = await fetch('/api/get_recommended_companies').then((res) =>
          res.json()
        );
        setCompanies(data);
      } catch (error) {
        console.error('Error fetching recommended companies:', error);
      }
    };
    fetchCompanies();
  }, [setCompanies]);

  return (
    <div className='my-2 rounded-lg p-4' style={{ backgroundColor: '#5252a3' }}>
      <div className={pop500.className} style={{ fontSize: '1.5rem', color: 'white' }}><div className='underline-white'>Companies we think you&apos;ll like</div></div>
      <div className='mt-2 flex flex-col gap-2 md:justify-between lg:flex-row'>
        {companies.length === 0 && <p>No recommended companies.</p>}
        {companies.map((company, index) => (
          <div
            className='flex flex-1 flex-row items-center justify-between rounded-lg bg-slate-100 p-2'
            key={index}
          >
            <Link href={`/company/${company.id}`}>
              <button
                type='button'
                className='flex flex-col items-start hover:drop-shadow-lg'
              >
                <div className='text-start'>{company.name}</div>
                <div>{company.symbol}</div>
              </button>
            </Link>
            <FollowButton companyId={company.id} isLoggedIn={isLoggedIn} />
          </div>
        ))}
      </div>
    </div>
  );
}
