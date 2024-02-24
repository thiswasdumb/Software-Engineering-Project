import Navbar from './ui/navigation/navbar';
import Footer from './ui/navigation/footer';
import './globals.css';
import { Inter } from 'next/font/google';
import { Metadata } from 'next';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: {
    template: '%s | TradeTalker',
    default: 'TradeTalker',
  },
  description:
    'The TradeTalker website for sentiment-based financial news reports.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang='en'>
      <body className={inter.className}>
        <Navbar />
        <div className='min-h-screen pb-40 pt-20'>{children}</div>
        <Footer />
      </body>
    </html>
  );
}
