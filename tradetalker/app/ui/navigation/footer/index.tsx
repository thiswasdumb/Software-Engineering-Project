import Image from 'next/image';
import Link from 'next/link';
import logo from '/public/images/logo.png';

/**
 * Footer component
 * @returns JSX.Element - Footer component
 */
export default function Footer() {
  return (
    <>
      <footer>
        <div className='min-h-100 relative flex h-40 w-full flex-grow bg-blue-600'>
          <div className='m-auto flex h-full flex-col justify-center px-4'>
            <div className='flex items-center justify-between'>
              <div className='flex h-full items-center justify-between gap-x-8'>
                <Link href='/'>
                  <Image
                    src={logo}
                    alt='TradeTalk Logo'
                    width={100}
                    className='relative hover:opacity-90'
                    priority={true}
                  />
                </Link>
              </div>
              <div className='m-4 flex gap-4'>
                <Link href='/about' className='text-white hover:opacity-90'>
                  About
                </Link>
                <Link href='/contact' className='text-white hover:opacity-90'>
                  Contact
                </Link>
                <Link href='/terms' className='text-white hover:opacity-90'>
                  Terms
                </Link>
                <Link href='/privacy' className='text-white hover:opacity-90'>
                  Privacy
                </Link>
              </div>
              <div className='flex flex-col'>
                <Link href='/support' className='text-white hover:opacity-90'>
                  Support
                </Link>
                <Link href='/search' className='text-white hover:opacity-90'>
                  Search
                </Link>
                <Link href='/stocks' className='text-white hover:opacity-90'>
                  Stocks
                </Link>
                <Link href='/companies' className='text-white hover:opacity-90'>
                  Companies
                </Link>
              </div>
            </div>
            <div className='text-center text-sm text-white'>
              &copy; 2024 TradeTalk Inc.
            </div>
          </div>
        </div>
      </footer>
    </>
  );
}
