'use client';
import Image from 'next/image';
import logo from '/public/images/logo.png';
import Link from 'next/link';

/**
 * Logo component.
 * @param props.isOpen - Whether the mobile navbar is open
 * @param props.toggle - Function to toggle the mobile navbar
 * @returns JSX.Element - Logo component
 */
export default function Logo(props: { isOpen: boolean; toggle: () => void }) {
  return (
    <>
      <Link
        className='hover:opacity-70'
        href='/'
        onClick={props.isOpen ? props.toggle : undefined}
      >
        <button type='button' className='logo-container'>
          <Image
            src={logo}
            alt='TradeTalk Logo'
            width={220}
            className='relative'
            priority={true}
          />
        </button>
      </Link>
    </>
  );
}
