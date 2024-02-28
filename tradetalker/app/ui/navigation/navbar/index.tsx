'use client';
import React, { useState, useEffect } from 'react';
import Logo from './logo';
import NavLinks from './nav-links';
import NavbarComponent from './navbar-auth-comps';
import { Bars3Icon } from '@heroicons/react/24/outline';
import Sidebar from '../sidebar';
import SearchButton from './search-button';
import { toast } from 'react-hot-toast';

export default function Navbar({ isLoggedIn }: { isLoggedIn: boolean }) {
  const [menuToggled, setMenuToggled] = useState(false);
  const [notifCount, setNotifCount] = useState(0);
  const toggleMenu = () => setMenuToggled(!menuToggled);

  useEffect(() => {
    if (isLoggedIn) {
      fetch('/api/get_notification_count')
        .then((response) => response.json())
        .then((data) => {
          setNotifCount(data);
        })
        .catch(() => {
          toast.error('Error fetching notifications.');
        });
    }
  }, [notifCount, isLoggedIn]);

  useEffect(() => {
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768 && menuToggled) {
        setMenuToggled(false);
      }
    });
  }, [menuToggled]);

  return (
    <>
<<<<<<< Updated upstream
      <div>
        <div className='fixed top-0 z-10 h-20 w-full bg-blue-600'>
          <div className='h-full px-4'>
            <div className='flex h-full items-center justify-between'>
              <div className='flex h-full items-center justify-between gap-x-8'>
                <Logo isOpen={menuToggled} toggle={toggleMenu} />
                <ul className='hidden gap-x-6 text-white md:flex'>
                  <NavLinks session={isLoggedIn} />
                </ul>
              </div>
              <NavbarComponent
                notifCount={notifCount}
                isOpen={menuToggled}
                toggle={toggleMenu}
                session={isLoggedIn}
              />
              <div className='inline-flex items-center gap-4 text-white md:hidden'>
                <SearchButton isOpen={menuToggled} toggle={toggleMenu} />
                <button type='button' onClick={toggleMenu}>
                  <Bars3Icon className='h-12 w-12 text-white hover:opacity-50' />
                </button>
              </div>
            </div>
          </div>
=======
      <div className="container mx-auto px-4 h-full">
        <div className="flex justify-between items-center h-full">
          <Logo isOpen={false} toggle={function (): void {
            throw new Error('Function not implemented.');
          }} />
          <ul className="hidden md:flex gap-x-20 text-white">
            <NavLinks session={session} />
          </ul>
          <NavbarComponent session={session} notifCount={0} isOpen={false} toggle={function (): void {
            throw new Error('Function not implemented.');
          }} />
          <button
            type="button"
            className="inline-flex items-center md:hidden"
            onClick={toggleMenu}
          >
            <Bars3Icon className={clsx("w-12 h-12 text-white hover:opacity-50")} />
          </button>
>>>>>>> Stashed changes
        </div>
        {menuToggled && (
          <>
            <div className='fixed z-10 mt-20'>
              <div
                className='fixed h-full w-full bg-black opacity-30'
                onClick={toggleMenu}
              />
              <Sidebar
                isOpen={menuToggled}
                toggle={toggleMenu}
                session={isLoggedIn}
                notifCount={notifCount}
              />
            </div>
          </>
        )}
      </div>
    </>
  );
}
