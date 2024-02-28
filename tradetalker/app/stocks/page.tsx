// Stocks.js
import React from 'react';
import { Metadata } from 'next';
import FloatingPiecesAnimation from './FloatingPiecesAnimation'; // Import the FloatingPiecesAnimation component

export const metadata: Metadata = {
  title: 'Stocks',
};

export default function Stocks() {
  return (
<<<<<<< Updated upstream
    <div className='m-8 rounded-lg bg-slate-200 p-8'>
      <div className='text-2xl'>Stocks</div>
      <hr className='mb-4 mt-2 rounded-lg border-2 border-slate-400' />
      <div className='flex flex-col content-start justify-between gap-4 md:flex-row'>
        {/* Stock trend */}
        <div className='max rounded-lg bg-slate-300 p-4'>[Stock trend]</div>
        {/* Leaderboard */}
        <div className='rounded-lg bg-slate-300 p-4'>[Leaderboard]</div>
      </div>
=======
    <div>
      <FloatingPiecesAnimation /> {/* Include the floating pieces animation */}
      <p>Stocks</p>
>>>>>>> Stashed changes
    </div>
  );
}
