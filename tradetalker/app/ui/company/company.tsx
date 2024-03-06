import React from 'react';
import { redirect } from 'next/navigation';
import LineChart from '@/app/ui/company/linechart';
import FollowButton from '@/app/ui/company/follow-button';
import ScrollUp from '../scroll-up';
import Description from './description';

async function getCompanyData(id: string) {
  const response = await fetch(`http:/localhost:8080/api/get_company/${id}`);
  if (!response.ok) {
    throw new Error('Error fetching company');
  }
  return response.json();
}

export default async function CompanyPage({
  id,
  isLoggedIn,
}: {
  id: string;
  isLoggedIn: boolean;
}) {
  const companyData = await getCompanyData(id);
  if (companyData.error) {
    redirect('/not-found');
  }
  const stockLastDays = [
    companyData.stock_d7,
    companyData.stock_d6,
    companyData.stock_d5,
    companyData.stock_d4,
    companyData.stock_d3,
    companyData.stock_d2,
    companyData.stock_d1,
    companyData.stock_price,
  ];

  return (
    <>
      <ScrollUp />
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='flex flex-row items-center justify-between'>
          <div className='text-2xl'>{companyData.name}</div>
          <div className='text-2xl'>{companyData.symbol}</div>
        </div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <div className='flex flex-col items-start lg:flex-row lg:justify-between'>
          <div className='w-full lg:w-[58%]'>
            <div className='flex w-full flex-row items-start justify-between'>
              <div>
                <div className='text-3xl'>{companyData.stock_price}</div>
                <div className='text-lg'>
                  Predicted stock price:&nbsp;
                  {companyData.predicted_stock_price !== null
                    ? companyData.predicted_stock_price
                    : 'N/A'}
                </div>
                <div className='text-lg'>
                  Stock variance:&nbsp;
                  {companyData.stock_variance !== null
                    ? companyData.stock_variance
                    : 'N/A'}
                </div>
                <div className='text-lg'>
                  Industry:&nbsp;{companyData.industry}
                </div>
              </div>
              <div className='mt-2'>
                <FollowButton companyId={id} isLoggedIn={isLoggedIn} />
              </div>
            </div>
            <LineChart stockLastDays={stockLastDays} />
          </div>
          <div className='mt-2 flex flex-col lg:w-[40%] lg:rounded-lg lg:bg-slate-300 lg:p-4'>
            <div className='text-xl'>Description</div>
            <hr className='border-1 my-2 rounded-lg border-slate-400' />
            <Description description={companyData.description} />
          </div>
        </div>
      </div>
    </>
  );
}
