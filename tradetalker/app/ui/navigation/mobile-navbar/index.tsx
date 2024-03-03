'use client';
import React from 'react';
import MobileNavLinks from './mobile-nav-links';

export default function MobileNavbar(props: {
  isOpen: boolean;
  toggle: () => void;
  session: boolean;
  notifCount: number;
}) {
  return (
    <>
      <div
        className='fixed block w-full justify-center bg-gray-200 md:hidden'
        style={{
          display: `${props.isOpen ? 'block' : 'none'}`,
        }}
      >
        <MobileNavLinks
          toggle={props.toggle}
          session={props.session}
          notifCount={props.notifCount}
        />
      </div>
    </>
  );
}
