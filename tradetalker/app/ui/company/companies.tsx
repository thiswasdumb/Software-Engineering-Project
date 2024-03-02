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
    <div className='bg-slate-200 m-8 rounded-lg p-8'>
      <div className='text-2xl'>Companies</div>
      <hr className='border-slate-400 my-2 rounded-lg border-2' />
      <div className='flex flex-row flex-wrap justify-between'>
        {companies.map((company, index) => (
          <Link
            href={`/company/${company.id}`}
            key={index}
            className='max-w-4 opacity:30 bg-slate-300 hover:bg-slate-400 my-2 w-full rounded-lg p-2 transition hover:bg-opacity-40 hover:drop-shadow-lg md:m-2 md:w-[30%]'
          >
            {company.name}
            <br></br>
            {company.symbol}
            <br></br>
            {company.stock_price}
            <br></br>
            {company.industry}
          </Link>
        ))}
      </div>
    </div>
  );
}
