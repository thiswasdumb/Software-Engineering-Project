import React from 'react';
import { redirect } from 'next/navigation';

async function getCompanyData(id: string) {
  const response = await fetch(`http:/localhost:8080/api/get_company/${id}`);
  if (!response.ok) {
    throw new Error('Error fetching company');
  }
  return response.json();
}

export default async function CompanyPage({ id }: { id: string }) {
  const companyData = await getCompanyData(id);
  if (companyData.error) {
    redirect('/not-found');
  }

  return (
    <div className='m-8 rounded-lg bg-slate-200 p-8'>
      <div className='flex flex-row items-center justify-between'>
        <div className='text-2xl'>{companyData.company_name}</div>
        <div className='text-xl'>{companyData.stock_symbol}</div>
      </div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <div className='text-lg'>Stock price: {companyData.stock_price}</div>
      <div className='text-lg'>
        Predicted stock price: {companyData.predicted_stock_price}
      </div>
      <div className='text-lg'>
        Stock variance: {companyData.stock_variance}
      </div>
      <div className='text-lg'>Industry: {companyData.industry}</div>
      <div className='mt-2 rounded-lg bg-slate-200'>
        <div className='text-xl'>Description</div>
        <hr className='border-1 my-2 rounded-lg border-slate-400' />
        <div className='text-lg'>{companyData.description}</div>
      </div>
    </div>
  );
}
