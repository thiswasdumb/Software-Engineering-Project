'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import FollowButton from '../company/follow-button';
import { Poppins } from 'next/font/google';
import './style.css'

const pop = Poppins({ weight: ['600'], subsets: ['latin'] });
const pop500 = Poppins({ weight: ['500'], subsets: ['latin'] });
const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });

export default function FollowedCompanies({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [companies, setCompanies] = useState<any[]>([]);
  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const data = await fetch('/api/get_followed_companies').then((res) =>
          res.json()
        );
        setCompanies(data);
      } catch (error) {
        console.error('Error fetching followed companies:', error);
      }
    };
    fetchCompanies();
  }, [setCompanies]);

  return (
    <div className='my-2 rounded-lg p-4' style={{ backgroundColor: '#7977d1' }}>
      <div className='text-white underline-white'><div className={pop.className} style={{ fontSize: '1.2rem', marginBottom: '1%' }}>Followed companies</div></div>
      <div className='flex flex-col text-white' style={{ marginTop: '2%' }}><div className={pop400.className}>
        {companies.length === 0 && <p>No followed companies.</p>}
        {companies.map((company, index) => (
          <div
            key={index}
            className='my-2 flex w-full flex-row items-center justify-between rounded-lg bg-slate-100 p-2 md:flex-col lg:flex-row'
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
    </div>
  );
}
