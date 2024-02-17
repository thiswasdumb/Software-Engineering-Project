'use client';
import React, { useState } from 'react';
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

  return (
    { menuToggled } && (
      <div>
        <div className='sticky top-0 h-20 w-full bg-blue-600'>
          <div className='container mx-auto h-full px-4'>
            <div className='flex h-full items-center justify-between'>
              <Logo />
              <ul className='hidden gap-x-6 text-white md:flex'>
                <NavLinks session={session} />
              </ul>
              <NavbarComponent session={session} />
              <div className='inline-flex items-center gap-4 text-white md:hidden'>
                <SearchButton />
                <button type='button' onClick={toggleMenu}>
                  <Bars3Icon className='h-12 w-12 text-white hover:opacity-50' />
                </button>
              </div>
            </div>
          </div>
        </div>
        <Sidebar isOpen={menuToggled} toggle={toggleMenu} />
      </div>
    )
  );
}
