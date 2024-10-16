'use client';
import React from 'react';
import MobileNavLinks from './mobile-nav-links';

/**
 * Mobile Navbar component.
 * @param props.isOpen - Whether the mobile navbar is open
 * @param props.toggle - Function to toggle the mobile navbar
 * @param props.session - Whether the user is logged in
 * @param props.notifCount - Number of notifications
 * @returns JSX.Element - Mobile Navbar component
 */
export default function MobileNavbar(props: {
  isOpen: boolean;
  toggle: () => void;
  session: boolean;
  notifCount: number;
}) {
  const isLoggedIn = props.session;
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
          session={isLoggedIn}
          notifCount={props.notifCount}
        />
      </div>
    </>
  );
}
