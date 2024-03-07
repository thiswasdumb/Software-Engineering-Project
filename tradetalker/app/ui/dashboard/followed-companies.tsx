'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import FollowButton from '../company/follow-button';

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
    <div className='my-2 rounded-lg bg-slate-300 p-4'>
      <div className='text-xl'>Followed companies ({companies.length})</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <div className='flex flex-col'>
        {companies.length === 0 && <p>No followed companies.</p>}
        {companies.map((company, index) => (
          <div
            key={index}
            className='my-2 flex flex-1 flex-row items-center justify-between rounded-lg bg-slate-100 p-2 md:flex-col lg:flex-row'
          >
            <Link
              href={`/company/${company.id}`}
              className='grow hover:drop-shadow-lg'
            >
              <button
                type='button'
                className='flex flex-col items-start text-start'
              >
                <p className='font-bold'>{company.symbol}</p>
                <p className='text-sm'>{company.name}</p>
              </button>
            </Link>
            <FollowButton companyId={company.id} isLoggedIn={isLoggedIn} />
          </div>
        ))}
      </div>
    </div>
  );
}
