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
import Share from './share-site'
import CursorAnimation from './CursorAnimations'
import { Poppins } from 'next/font/google'
import './style.css'

const pop = Poppins({ weight: ['600'], subsets: ['latin'] })

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
      <div className=''>
        <div className='dark-olay'></div>
        <CursorAnimation />
        <div className='big-header'>
          <div className='dark-rectle'>
            <div className={pop.className}><span className="text-white" style={{ fontSize: '7rem' }}>Dashboard</span></div></div>
          <hr className='mb-4 mt-3' style={{ backgroundColor: '#4C4B9B', height: '10px', marginTop: '-3%' }} />
          <div className='margin-all-around'>
            <div className={pop.className}><span style={{ fontSize: '3rem' }}>{data}.</span></div>
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
          </div>
          <Share />
        </div>
      </div>
    )
  );
}
