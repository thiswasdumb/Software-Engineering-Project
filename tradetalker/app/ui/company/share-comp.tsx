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
import jsPDF from 'jspdf';

/**
 * Share company component.
 * @param id - Company ID
 * @returns JSX.Element - Share company component
 */
export default function ShareCompany({
  id,
  company,
  diff,
  change,
  stockLastDays,
}: {
  id: string;
  company: any;
  diff: number;
  change: number;
  stockLastDays: number[];
}) {
  let diffStr = '';
  let changeStr = '';
  let max = 0;
  let min = 0;
  let mean = 0;
  let median = 0;
  let sd = 0;

  if (diff > 0) {
    diffStr = '+' + diff.toFixed(2);
  } else {
    diffStr = diff.toFixed(2);
  }

  if (change > 0) {
    changeStr = '+' + change.toFixed(2) + '%';
  } else {
    changeStr = change.toFixed(2) + '%';
  }

  if (company.description.length > 1000) {
    company.description = company.description.substring(0, 1000) + '...';
  }

  max = Math.max(...stockLastDays);
  min = Math.min(...stockLastDays);
  mean = stockLastDays.reduce((a, b) => a + b, 0) / stockLastDays.length;
  median = stockLastDays.sort((a, b) => a - b)[
    Math.floor(stockLastDays.length / 2)
  ];
  sd = Math.sqrt(
    stockLastDays.reduce((a, b) => a + Math.pow(b - mean, 2), 0) /
      stockLastDays.length
  );

  function savePdf() {
    const doc = new jsPDF('p', 'pt', 'a4');
    const canvas = document.getElementById('myChart') as HTMLCanvasElement;
    const img = canvas.toDataURL('image/png');
    console.log(img);
    doc.setFontSize(16);
    doc.text(`Company: ${company.name}`, 40, 60).setFontSize(16);
    doc.text(`Symbol: ${company.symbol}`, 40, 80).setFontSize(20);
    doc.text(`GBX ${company.stock_price}`, 40, 120).setFontSize(12);
    doc.text(`${diffStr} (${changeStr})`, 40, 140);
    doc.text(
      `Predicted stock price in 7 days: ${company.predicted_stock_price}`,
      40,
      160
    );
    doc.text('Industry: ' + company.industry, 40, 180);
    doc
      .text('Description: ' + company.description, 40, 200, { maxWidth: 500 })
      .setFontSize(16);
    doc.addImage(img, 'PNG', 40, 380, 500, 250);
    doc.text('Statistics:', 40, 660).setFontSize(12);
    doc.text(`Max: ${max}`, 40, 680).setFontSize(12);
    doc.text(`Min: ${min}`, 40, 700).setFontSize(12);
    doc.text(`Mean: ${mean}`, 40, 720).setFontSize(12);
    doc.text(`Median: ${median}`, 40, 740).setFontSize(12);
    doc.text(`Standard deviation: ${sd}`, 40, 760).setFontSize(12);
    doc.save(`${company.symbol}-summary.pdf`);
  }

  return (
    <div>
      <Popup
        trigger={
          <button
            type='button'
            className='mt-4 w-48 rounded-lg bg-blue-500 p-2 text-white transition hover:bg-blue-600 active:bg-blue-700'
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
            id='download'
            type='button'
            className='flex flex-grow items-center rounded-lg transition hover:bg-blue-100'
            onClick={() => savePdf()}
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
