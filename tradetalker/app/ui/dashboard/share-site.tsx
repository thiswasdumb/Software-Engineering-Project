'use client';
import { ShareIcon } from '@heroicons/react/20/solid';
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
 * Share site component.
 * @returns JSX.Element - Share site component
 */
export default function ShareSite() {
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
              title='Check out this cool new site!'
              url='https://tradetalk.com'
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
              url='https://tradetalk.co.uk'
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
              url='https://tradetalk.co.uk'
              title='Check out this awesome site!'
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
              url='https://tradetalk.co.uk'
              title='Check out this site!'
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
              url='https://tradetalk.co.uk'
              subject='Hi, check out this site!'
            >
              <div className='my-1 flex flex-row items-center hover:drop-shadow-lg'>
                <EmailIcon size={32} round={true} />
                <p className='ml-2'>Email</p>
              </div>
            </EmailShareButton>
          </div>
        </div>
      </Popup>
    </div>
  );
}
