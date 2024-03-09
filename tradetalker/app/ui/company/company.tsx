import React from 'react';
import { redirect } from 'next/navigation';
import LineChart from '@/app/ui/company/linechart';
import FollowButton from '@/app/ui/company/follow-button';
import ScrollUp from '../scroll-up';
import Description from './description';
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/solid';
import ShareCompany from '../company/share-comp';

/**
 *
 * @param id - Company ID
 * @returns Promise - Company data
 */
async function getCompanyData(id: string) {
  const response = await fetch(`http:/localhost:8080/api/get_company/${id}`, {
    cache: 'no-store',
  });
  if (!response.ok) {
    throw new Error('Error fetching company');
  }
  return response.json();
}

/**
 * Company page component.
 * @param id - Company ID
 * @param isLoggedIn - Flag to check if the user is logged in
 * @returns JSX.Element - Company page component
 */
export default async function CompanyPage({
  id,
  isLoggedIn,
}: {
  id: string;
  isLoggedIn: boolean;
}) {
  const companyData = await getCompanyData(id);
  if (companyData.error) {
    redirect('/not-found'); // Redirect to 404 page if company is not found
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
  ]; // Stock prices for the last 7 days
  // Calculate the difference and percentage change in stock price
  const diff = companyData.stock_price - companyData.stock_d7;
  const perc_change = (diff / companyData.stock_d7) * 100;

  return (
    <>
      <ScrollUp />
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='flex flex-row items-center justify-between'>
          <div className='flex flex-row flex-wrap items-center gap-3'>
            <h1 className='text-2xl'>{companyData.name}</h1>
            <span
              title='Company rank by stock price'
              className='select-none rounded-lg bg-green-600 px-2 text-lg text-white'
            >
              #{companyData.rank}
            </span>
          </div>
          <h1 className='text-2xl'>{companyData.symbol}</h1>
        </div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <div className='flex flex-col items-start lg:flex-row lg:justify-between'>
          <div className='w-full lg:w-[58%]'>
            <div className='flex w-full flex-row items-start justify-between'>
              <div>
                <div className='flex flex-row items-center gap-2'>
                  <h2 className='text-3xl'>{companyData.stock_price}</h2>
                  <div
                    className={`flex flex-row flex-wrap items-center gap-1 ${diff > 0 ? 'text-green-700' : 'text-red-700'}`}
                  >
                    <p className='text-lg'>
                      {diff > 0 ? '+' : ''}
                      {diff.toFixed(2)} ({perc_change > 0 ? '+' : ''}
                      {perc_change.toFixed(2)}%)
                    </p>
                    {diff > 0 ? (
                      <ArrowUpIcon className='h-4 w-4 stroke-green-700 stroke-[2] text-green-700' />
                    ) : (
                      <ArrowDownIcon className='h-4 w-4 stroke-red-700 stroke-[2] text-red-700' />
                    )}
                    <p>past 7 days</p>
                  </div>
                </div>
                <p className='text-lg'>
                  Predicted stock price:&nbsp;
                  {companyData.predicted_stock_price !== null
                    ? companyData.predicted_stock_price
                    : 'N/A'}
                </p>
                <p className='text-lg'>Industry:&nbsp;{companyData.industry}</p>
              </div>
              <div className='mt-2'>
                <FollowButton companyId={id} isLoggedIn={isLoggedIn} />
              </div>
            </div>
            <LineChart stockLastDays={stockLastDays} />
            <ShareCompany
              id={id}
              company={companyData}
              diff={diff}
              change={perc_change}
              stockLastDays={stockLastDays}
            />
          </div>
          <div className='mt-2 flex w-full flex-col lg:w-[40%] lg:rounded-lg lg:bg-slate-300 lg:p-4'>
            <h2 className='text-xl'>Description</h2>
            <hr className='border-1 my-2 rounded-lg border-slate-400' />
            <Description description={companyData.description} />
          </div>
        </div>
      </div>
    </>
  );
}
