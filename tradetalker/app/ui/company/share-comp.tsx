'use client';
import { ShareIcon, ArrowDownTrayIcon } from '@heroicons/react/20/solid';
import {
  EmailShareButton,
  RedditIcon,
  RedditShareButton,
  FacebookShareButton,
  TwitterShareButton,
  FacebookIcon,
  XIcon,
  EmailIcon,
  WhatsappShareButton,
  WhatsappIcon,
} from 'react-share';
import React from 'react';
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';

/**
 * Share company component.
 * @param id - Company ID
 * @returns JSX.Element - Share company component
 */
export default function ShareCompany({ id }: { id: string }) {
  return (
    <div>
      <Popup
        trigger={
          <button
            type='button'
            className='mt-2 w-48 rounded-lg bg-blue-500 p-2 text-white transition hover:bg-blue-600 active:bg-blue-700'
          >
            Share
            <ShareIcon className='ml-2 inline-block h-6 w-6' />
          </button>
        }
      >
        <div className='flex flex-col '>
          <div className='flex flex-grow rounded-lg transition hover:bg-blue-100'>
            <TwitterShareButton
              className='flex flex-grow hover:bg-blue-500 hover:drop-shadow-lg'
              title="Check out how this company's doing!"
              url={`http://localhost:3000/company/${id}`}
            >
              <div className='my-1 flex flex-row items-center hover:drop-shadow-lg'>
                <XIcon size={32} round={true} />
                <p className='ml-2'>X</p>
              </div>
            </TwitterShareButton>
          </div>
          <div className='flex flex-grow rounded-lg transition hover:bg-blue-100'>
            <FacebookShareButton
              className='flex flex-grow hover:bg-blue-500 hover:drop-shadow-lg'
              url={`http://localhost:3000/company/${id}`}
              hashtag='#TradeTalk #LetsTalkTrade #Finance'
            >
              <div className='my-1 flex flex-row items-center hover:drop-shadow-lg'>
                <FacebookIcon size={32} round={true} />
                <p className='ml-2'>Facebook</p>
              </div>
            </FacebookShareButton>
          </div>
          <div className='flex flex-grow rounded-lg transition hover:bg-blue-100'>
            <RedditShareButton
              className='flex flex-grow hover:bg-blue-500 hover:drop-shadow-lg'
              url={`http://localhost:3000/company/${id}`}
              title="Check out this company's status!"
            >
              <div className='my-1 flex flex-row items-center hover:drop-shadow-lg'>
                <RedditIcon size={32} round={true} />
                <p className='ml-2'>Reddit</p>
              </div>
            </RedditShareButton>
          </div>
          <div className='flex flex-grow rounded-lg transition hover:bg-blue-100'>
            <WhatsappShareButton
              className='flex flex-grow hover:bg-blue-500 hover:drop-shadow-lg'
              url={`http://localhost:3000/company/${id}`}
              title="Check out this company's status!"
            >
              <div className='my-1 flex flex-row items-center hover:drop-shadow-lg'>
                <WhatsappIcon size={32} round={true} />
                <p className='ml-2'>WhatsApp</p>
              </div>
            </WhatsappShareButton>
          </div>
          <div className='flex flex-grow rounded-lg transition hover:bg-blue-100'>
            <EmailShareButton
              className='flex flex-grow hover:bg-blue-500 hover:drop-shadow-lg'
              url={`http://localhost:3000/company/${id}`}
              subject="Hi, check out this company's status!"
            >
              <div className='my-1 flex flex-row items-center hover:drop-shadow-lg'>
                <EmailIcon size={32} round={true} />
                <p className='ml-2'>Email</p>
              </div>
            </EmailShareButton>
          </div>
          <button
            type='button'
            className='flex flex-grow items-center rounded-lg transition hover:bg-blue-100'
          >
            <div className='my-1 rounded-full bg-gray-400 p-1 hover:drop-shadow-lg'>
              <ArrowDownTrayIcon className='h-6 w-6 bg-gray-400 text-white' />
            </div>
            <p className='ml-2'>Save as PDF</p>
          </button>
        </div>
      </Popup>
    </div>
  );
}
