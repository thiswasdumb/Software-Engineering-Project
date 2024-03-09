import React from 'react';
import Link from 'next/link';
import {
  ArrowUpCircleIcon,
  ArrowDownCircleIcon,
  MinusCircleIcon,
} from '@heroicons/react/20/solid';
import RectangleLoopAnimation from './RectangleLoopAnimation';
import RectangleLoopAnimation2 from './RectangleLoopAnimation2';
import './styles.css';
import { Poppins } from 'next/font/google'

const pop = Poppins({ weight: ['400'], subsets: ['latin'] })
const pop700 = Poppins({ weight: '700', subsets: ['latin'] })
const pop500 = Poppins({ weight: '600', subsets: ['latin'], style: 'italic' })

async function fetchArticles() {
  const response = await fetch('http://localhost:8080/api/home_articles', {
    next: { revalidate: 0 },
  });
  if (!response.ok) {
    throw new Error('An error occurred while fetching the users.');
  }
  return response.json();
}

export default async function HomeComponent() {
  const articles: any[] = await fetchArticles(); // Wait for the promise to resolve

  return (
    <>
      <div className='animation-container dark-filter'>
        <RectangleLoopAnimation />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation2 />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation2 />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation2 />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation2 />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation2 />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation2 />
        <div className="my-custom-gap"></div>
        <RectangleLoopAnimation />
        <div className="my-custom-gap"></div>
      </div>
      <div className="dark-overlay"></div>

      <div className="dark-rectangle">
        <div className={pop.className}>
          <div className="text-white text-3xl font-fancy mb-2">Let's Talk</div>
          <div className="reduce-gap"><span className="text-white font-bold underline" style={{ fontSize: '12rem' }}>Trade</span><span style={{ fontSize: '12rem' }}>.</span></div></div>
      </div>
      <div className="company-info">
        <div className={pop.className}>
          <div className="text-margin">
            <div className="font-bold" className={pop700.className} style={{ fontSize: '3rem', fontWeight: '700' }}>
              <span className="custom-underline">What we do</span>
            </div><br />
            <div style={{ fontSize: '1.3rem' }}>TradeTalk is dedicated to transforming the way people interact with the financial landscape. Our platform offers a transparent and insightful approach, allowing users to track public perceptions of companies and their impact on financial markets.<br /><br /> Through <span className={pop500.className}>personalized updates</span>, <span className={pop500.className}>real-time stock trends</span>, and <span className={pop500.className}>comprehensive analyses of news stories</span>, we keep users informed and equipped to make <span className="underline-simple">informed decisions</span>. With curated links to trusted sources and advanced text analysis, TradeTalk provides clear insights without offering financial advice.<br /><br />Our predictive analyses on stock prices are grounded in <span className="underline-simple">rigorous research</span> and <span className="underline-simple">verifiable methodologies</span>, ensuring credibility and reliability.<br /><br /> At TradeTalk, we're committed to empowering users with the tools they need to navigate the complexities of the financial world confidently.</div>
          </div>
        </div></div >
      <div className="separator"> </div>

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
          <div className='text-xl'>Recent articles</div>
          {articles.map((article, index) => (
            <div
              className='my-2 overflow-scroll rounded-lg bg-slate-100 p-2 transition hover:bg-slate-200 hover:drop-shadow-lg'
              key={index}
            >
              <Link href={`/article/${article.id}`}>
                <div>{article.title}</div>
                <hr className='border-1 my-2 rounded-lg border-slate-300' />
                <div>{article.summary}</div>
                <div>
                  {article.score > 0.5 ? (
                    <div className='flex flex-row items-center'>
                      <ArrowUpCircleIcon className='h-12 w-12 text-green-500' />
                      <div className='pl-2'>Positive</div>
                    </div>
                  ) : article.score < 0.5 ? (
                    <div className='flex flex-row items-center'>
                      <ArrowDownCircleIcon className='h-12 w-12 text-red-500 ' />
                      <div className='pl-2'>Negative</div>
                    </div>
                  ) : (
                    <div className='flex flex-row items-center'>
                      <MinusCircleIcon className='h-12 w-12 text-slate-400' />
                      <div className='pl-2'>Neutral</div>
                    </div>
                  )}
                </div>
              </Link>
            </div>
          ))}
        </div>*/