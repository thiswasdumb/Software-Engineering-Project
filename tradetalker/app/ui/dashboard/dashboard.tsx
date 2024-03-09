'use client';
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';
import RecommendedArticles from './rec-articles';
import RecommendedCompanies from './rec-companies';
import NewsFeed from './news-feed';
import FollowedCompanies from './followed-companies';
import ShareSite from './share-site';
import ReadParams from '../read-params';

/**
 * Dashboard component
 * @param isLoggedIn - Flag to check if the user is logged in
 * @returns JSX.Element - Dashboard component
 */
export default function DashboardComponent({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const [data, setData] = useState('Loading...');
  const router = useRouter();

  // Fetch the user data on page load
  useEffect(() => {
    if (isLoggedIn) {
      fetch('/api/get_dashboard_data')
        .then((response) => response.json())
        .then((data) => {
          if (data.username) {
            setData(data.username);
          }
        })
        .catch(() => {
          toast.error('Error fetching user data.');
        });
    } else {
      router.push('/login');
      toast.error('You must be logged in.');
    }
  }, [data, isLoggedIn, router]);

  return (
    isLoggedIn && (
      <>
        <ReadParams url='dashboard' />
        <div className='rounded-lg bg-slate-200 p-8 md:m-8'>
          <h1 className='text-2xl'>Dashboard</h1>
          <hr className='my-2 rounded-lg border-2 border-slate-400' />
          <p className='text-lg'>{data}.</p>
          <div className='flex flex-col justify-between md:flex-row'>
            <div className='flex w-full flex-col md:w-[69%]'>
              <RecommendedArticles />
              <RecommendedCompanies isLoggedIn={isLoggedIn} />
            </div>
            <div className='flex w-full flex-col md:w-[30%]'>
              <NewsFeed />
              <FollowedCompanies isLoggedIn={isLoggedIn} />
            </div>
          </div>
          <ShareSite />
        </div>
      </>
    )
  );
}
