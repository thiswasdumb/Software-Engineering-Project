import React from 'react';
import Link from 'next/link';

async function getCompanies() {
  const response = await fetch('http://localhost:8080/api/get_companies');
  if (!response.ok) {
    throw new Error('Error fetching companies');
  }
  return response.json();
}

export default async function CompaniesComponent() {
  const companies: any[] = await getCompanies();

  return (
    <div className='m-8 rounded-lg bg-slate-200 p-8'>
      <div className='text-2xl'>Companies</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <div className='flex justify-center'>
        <div className='flex flex-row flex-wrap justify-center'>
          {companies.map((company, index) => (
            <Link
              href={`/company/${company.id}`}
              key={index}
              className='max-w-4 opacity:30 my-2 w-full rounded-lg bg-slate-300 p-2 transition hover:bg-slate-400 hover:bg-opacity-40 hover:drop-shadow-lg md:m-2 md:w-[30%]'
            >
              <div>
                {company.symbol}&nbsp;|&nbsp;
                {company.name}
              </div>
              {company.stock_price}
              <div className='text-sm'>{company.industry}</div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
