import React from 'react';
import { redirect } from 'next/navigation';
import LineChart from '@/app/ui/company/linechart';
import FollowButton from '@/app/ui/company/follow-button';
import ScrollUp from '../scroll-up';
import Description from './description';
import {
  ArrowUpIcon,
  ArrowDownIcon,
  ArrowUpCircleIcon,
  ArrowDownCircleIcon,
  MinusCircleIcon,
} from '@heroicons/react/24/solid';
import ShareCompany from '../company/share-comp';
import dayjs from 'dayjs';
import RelativeTime from 'dayjs/plugin/relativeTime';
import Link from 'next/link';

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

async function getArticleData(id: string) {
  const response = await fetch(
    `http:/localhost:8080/api/get_company_articles/${id}`,
    {
      cache: 'no-store',
    }
  );
  if (!response.ok) {
    throw new Error('Error fetching articles');
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

  const articleData: any[] = await getArticleData(id);
  dayjs.extend(RelativeTime);

  return (
    <>
      <ScrollUp />
      <div className='rounded-lg bg-slate-200 p-8 md:m-8'>
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
                  <h2 className='text-2xl'>GBX</h2>
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
                  Predicted stock price in 7 days:&nbsp;
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
          </div>
          <div className='mt-2 flex w-full flex-col lg:w-[40%] lg:rounded-lg lg:bg-slate-300 lg:p-4'>
            <h2 className='text-xl'>Description</h2>
            <hr className='border-1 my-2 rounded-lg border-slate-400' />
            <Description description={companyData.description} />
          </div>
        </div>
        <div className='flex flex-col items-start justify-between'>
          <div className='mt-4 rounded-lg bg-slate-300 p-4'>
            {articleData.length === 0 ? (
              <p>No articles mentioning this company.</p>
            ) : (
              <h2 className='text-xl'>Recent articles</h2>
            )}
            {articleData.map((article, index) => (
              <div
                className='my-2 rounded-lg bg-slate-100 p-2 transition hover:bg-blue-100 hover:drop-shadow-lg'
                key={index}
              >
                <Link href={`/article/${article.id}`}>
                  <div className='flex flex-row flex-wrap items-center justify-between'>
                    <h3 className='mr-2 text-lg'>{article.title}</h3>
                    <span className='text-sm text-gray-600'>
                      {dayjs(article.date).fromNow()}
                    </span>
                  </div>
                  <hr className='border-1 my-2 rounded-lg border-slate-300' />
                  <p>{article.summary}</p>
                  <hr className='border-1 my-2 rounded-lg border-slate-300' />
                  <div className='flex flex-row items-center justify-between'>
                    {article.score > 0.33 ? (
                      <div className='flex flex-row items-center'>
                        <ArrowUpCircleIcon className='h-10 w-10 text-green-500' />
                        <p className='pl-2 text-green-600'>Positive</p>
                      </div>
                    ) : article.score < -0.33 ? (
                      <div className='flex flex-row items-center'>
                        <ArrowDownCircleIcon className='h-10 w-10 text-red-600 ' />
                        <p className='pl-2 text-red-600'>Negative</p>
                      </div>
                    ) : (
                      <div className='flex flex-row items-center'>
                        <MinusCircleIcon className='h-10 w-10 text-slate-400' />
                        <p className='pl-2 text-slate-500'>Neutral</p>
                      </div>
                    )}
                  </div>
                </Link>
              </div>
            ))}
          </div>
          <ShareCompany
            id={id}
            company={companyData}
            diff={diff}
            change={perc_change}
            stockLastDays={stockLastDays}
            articles={articleData}
          />
        </div>
      </div>
    </>
  );
}
