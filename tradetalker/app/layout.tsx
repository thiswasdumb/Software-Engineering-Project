import React, { Suspense, ReactNode } from 'react';
import Navbar from './ui/navigation/navbar/navbar';
import Footer from './ui/navigation/footer';
import './globals.css';
import { Inter } from 'next/font/google';
import { Metadata } from 'next';
import { cookies } from 'next/headers';
import { Toaster } from 'react-hot-toast';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: {
    template: '%s | TradeTalker',
    default: 'TradeTalker',
  },
  description:
    'The TradeTalker website for sentiment-based financial news reports.',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  // Check if the user is logged in
  const session = cookies().get('session') !== undefined;
  return (
    <>
      <html lang='en'>
        <body className={inter.className}>
          <Suspense>
            <Navbar isLoggedIn={session} />
          </Suspense>
          <main className='min-h-screen pb-40 pt-20'>
            <Toaster position='bottom-left' reverseOrder={false} />
            {children}
          </main>
          <Footer />
        </body>
      </html>
    </>
  );
}
