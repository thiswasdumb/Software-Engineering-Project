'use client';
import React, { useState, useEffect } from 'react';
import Logo from './logo';
import NavLinks from './nav-links';
import NavbarComponent from './navbar-auth-comps';
import { Bars3Icon } from '@heroicons/react/24/outline';
import Sidebar from '../sidebar';
import SearchButton from './search-button';

export default function Navbar() {
  const [menuToggled, setMenuToggled] = useState(false);
  const toggleMenu = () => setMenuToggled(!menuToggled);

  const session = false; // TODO: replace with actual session
  const notifCount = 1; // TODO: replace with actual notification count

  useEffect(() => {
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768 && menuToggled) {
        setMenuToggled(false);
      }
    });
  }, [menuToggled]);

  return (
    <>
      <div>
        <div className='fixed top-0 z-10 h-20 w-full bg-blue-600'>
          <div className='h-full px-4'>
            <div className='flex h-full items-center justify-between'>
              <div className='flex h-full items-center justify-between gap-x-8'>
                <Logo isOpen={menuToggled} toggle={toggleMenu} />
                <ul className='hidden gap-x-6 text-white md:flex'>
                  <NavLinks session={session} />
                </ul>
              </div>
              <NavbarComponent
                notifCount={notifCount}
                isOpen={menuToggled}
                toggle={toggleMenu}
                session={session}
              />
              <div className='inline-flex items-center gap-4 text-white md:hidden'>
                <SearchButton isOpen={menuToggled} toggle={toggleMenu} />
                <button type='button' onClick={toggleMenu}>
                  <Bars3Icon className='h-12 w-12 text-white hover:opacity-50' />
                </button>
              </div>
            </div>
          </div>
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
                session={session}
                notifCount={notifCount}
              />
            </div>
          </>
        )}
      </div>
    </>
  );
}
