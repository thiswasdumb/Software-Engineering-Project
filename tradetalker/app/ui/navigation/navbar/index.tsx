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
    { menuToggled } &&
    <div>
      <div className="w-full h-20 bg-blue-600 sticky top-0">
        <div className="container mx-auto px-4 h-full">
          <div className="flex justify-between items-center h-full">
            <Logo />
            <ul className="hidden md:flex gap-x-6 text-white">
              <NavLinks session={session} />
            </ul>
            <NavbarComponent session={session} />
            <div className="text-white inline-flex items-center md:hidden gap-4">
              <SearchButton />
              <button
                type="button"
                onClick={toggleMenu}
              >
                <Bars3Icon className="w-12 h-12 text-white hover:opacity-50" />
              </button>
            </div>
          </div>
        </div>
      </div>
      <Sidebar isOpen={menuToggled} toggle={toggleMenu} />
    </div>
  );
};