'use client';
import Image from 'next/image';
import logo from '/public/images/logo.png';
import Link from 'next/link';

export default function Logo(props: { isOpen: boolean; toggle: () => void }) {
  return (
    <>
      <Link
        className='hover:opacity-70'
        href='/'
        onClick={props.isOpen ? props.toggle : undefined}
      >
        <div className='logo-container'>
          <Image
            src={logo}
            alt='TradeTalker Logo'
            width={210}
            className='relative'
            priority={true}
          />
        </div>
      </Link>
    </>
  );
}
