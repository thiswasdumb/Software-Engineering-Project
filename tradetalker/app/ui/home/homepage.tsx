import React from 'react';
import Link from 'next/link';
import {
  ArrowUpCircleIcon,
  ArrowDownCircleIcon,
  MinusCircleIcon,
} from '@heroicons/react/20/solid';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import ReadParams from '@/app/ui/read-params';
import RectangleLoopAnimation from './RectangleLoopAnimation';
import RectangleLoopAnimation2 from './RectangleLoopAnimation2';
import GraphWithArrowAnimation from './GraphWithArrowAnimation';
import './styles.css';
import { Poppins } from 'next/font/google';

const pop = Poppins({ weight: ['400'], subsets: ['latin'] });
const pop700 = Poppins({ weight: '700', subsets: ['latin'] });
const pop500 = Poppins({ weight: '600', subsets: ['latin'], style: 'italic' });

/**
 * Fetch the latest articles from the server
 * @returns Promise - The latest articles
 */
async function fetchArticles() {
  const response = await fetch('http://localhost:8080/api/home_articles', {
    cache: 'no-store',
  });
  if (!response.ok) {
    throw new Error('An error occurred while fetching the users.');
  }
  return response.json();
}

/**
 * Home page component
 * @returns Promise - Home page component
 */
export default async function HomeComponent() {
  const articles: any[] = await fetchArticles(); // Wait for the promise to resolve
  dayjs.extend(relativeTime);

  return (
    <>
      <div className='animation-container dark-filter'>
        <RectangleLoopAnimation />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation2 />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation2 />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation2 />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation2 />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation2 />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation2 />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation />
        <div className='my-custom-gap'></div>
        <RectangleLoopAnimation2 />
        <div className='my-custom-gap'></div>
      </div>
      <div className='dark-overlay'></div>

      <div className='dark-rectangle'>
        <div className={pop.className}>
          <div className='font-fancy mb-2 text-3xl text-white'>Let's Talk</div>
          <div className='reduce-gap'>
            <span
              className='font-bold text-white underline'
              style={{ fontSize: '12rem' }}
            >
              Trade
            </span>
            <span style={{ fontSize: '12rem' }}>.</span>
          </div>
        </div>
      </div>
      <div className='company-info'>
        <div className={pop.className}>
          <div className='text-margin'>
            <div
              className='font-bold'
              className={pop700.className}
              style={{ fontSize: '3rem', fontWeight: '700' }}
            >
              <span className='custom-underline'>What we do</span>
            </div>
            <br />
            <div style={{ fontSize: '1.3rem' }}>
              TradeTalk is dedicated to transforming the way people interact
              with the financial landscape. Our platform offers a transparent
              and insightful approach, allowing users to track public
              perceptions of companies and their impact on financial markets.
              <br />
              <br /> Through{' '}
              <span className={pop500.className}>
                personalized updates
              </span>,{' '}
              <span className={pop500.className}>real-time stock trends</span>,
              and{' '}
              <span className={pop500.className}>
                comprehensive analyses of news stories
              </span>
              , we keep users informed and equipped to make{' '}
              <span className='underline-simple'>informed decisions</span>. With
              curated links to trusted sources and advanced text analysis,
              TradeTalk provides clear insights without offering financial
              advice.
              <br />
              <br />
              Our predictive analyses on stock prices are grounded in{' '}
              <span className='underline-simple'>
                rigorous research
              </span> and{' '}
              <span className='underline-simple'>verifiable methodologies</span>
              , ensuring credibility and reliability.
              <br />
              <br /> At TradeTalk, we're committed to empowering users with the
              tools they need to navigate the complexities of the financial
              world confidently.
            </div>
            <div
              className='font-bold'
              className={pop700.className}
              style={{ fontSize: '3rem', fontWeight: '700' }}
            >
              <span className='custom-underline'>Who we are</span>
            </div>{' '}
            <br />
            <div style={{ fontSize: '1.3rem' }}>
              TradeTalk formed from a group of university students wanting to
              address ongoing issues in the financial world. From this, the
              model has grown into a{' '}
              <span className='underline-simple'>critical web platform</span>{' '}
              addressing{' '}
              <span className={pop500.className}>ongoing perspectives</span> and
              their <span className={pop500.className}>short-term effects</span>{' '}
              regarding stocks for influential companies.
              <br />
              <br />
              We have worked consistently to ensure we can produce an
              environment which allows for users to take and apply the
              information condensed and provided in order to be used for the{' '}
              <span className='underline-simple'>
                benefit of the financial world
              </span>
              . We’re committed to developing a platform that communicates{' '}
              <span className={pop500.className}>responsible usage</span>,{' '}
              <span className={pop500.className}>proper application</span> and{' '}
              <span className={pop500.className}>proactive action</span> within
              the rapidly changing financial atmosphere.
            </div>
            <br />
          </div>
        </div>
      </div>
      <div className='separator'> </div>
    </>
  );
}

/*        <div className='text-2xl'>Welcome to TradeTalk.</div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <p>
          Stay informed about the latest news sentiment in the financial
          markets.
        </p> 
        
        
                <br></br>
        <div className='rounded-lg bg-slate-300 p-4'>
          <h2 className='text-xl'>Recent articles</h2>
          {articles.map((article, index) => (
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
                  {article.score > 0.5 ? (
                    <div className='flex flex-row items-center'>
                      <ArrowUpCircleIcon className='h-10 w-10 text-green-500' />
                      <p className='pl-2 text-green-600'>Positive</p>
                    </div>
                  ) : article.score < -0.5 ? (
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
        </div>*/
