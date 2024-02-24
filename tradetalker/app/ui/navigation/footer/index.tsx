import Image from 'next/image';
import Link from 'next/link';
import logo from '/public/images/logo.png';

export default function Footer() {
  return (
    <>
      <footer>
        <div className='min-h-100 flex h-40 w-full flex-grow bg-blue-600'>
          <div className='m-auto h-full px-4'>
            <div className='flex h-full items-center justify-between'>
              <div className='flex h-full items-center justify-between gap-x-8'>
                <Link href='/'>
                  <Image
                    src={logo}
                    alt='TradeTalker Logo'
                    width={50}
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
                <Link href='/search' className='text-white'>
                  Search
                </Link>
                <Link href='/stocks' className='text-white'>
                  Stocks
                </Link>
                <Link href='/companies' className='text-white'>
                  Companies
                </Link>
                <Link href='/support' className='text-white'>
                  Support
                </Link>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
}
