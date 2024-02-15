'use client';
import React, { useEffect, useState } from 'react';
import Logo from './logo';
import NavLinks from './nav-links';
import NavbarComponent from './navbar-auth-comps';
import { Bars3Icon } from '@heroicons/react/24/outline';
import clsx from 'clsx';
import { useRouter } from 'next/navigation';

const Navbar = ({ toggle }: { toggle: () => void }) => {
  const router = useRouter();
  const [menuOpen, setMenuOpen] = useState(false);
  const toggleMenu = () => setMenuOpen(!menuOpen);
  const closeMenu = () => setMenuOpen(false);

  useEffect(() => {
    if (menuOpen) {
      document.body.style.overflow = 'auto';
    } else {
      document.body.style.overflow = 'hidden';
    }
  }, [menuOpen]);


  const session = false; // For testing logged in/out state
  return (
    <>
      <div className="w-full h-20 bg-blue-600 sticky top-0">
        <div className="container mx-auto px-4 h-full">
          <div className="flex justify-between items-center h-full">
            <Logo />
            <ul className="hidden md:flex gap-x-6 text-white">
              <NavLinks />
            </ul>
            <NavbarComponent session={session} />
            <button
              type="button"
              className="inline-flex items-center md:hidden"
              onClick={toggleMenu}
            >
              <Bars3Icon className={clsx("w-12 h-12 text-white hover:opacity-50")} />
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default Navbar;