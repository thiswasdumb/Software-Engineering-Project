'use client';
import React, { useState, useEffect } from 'react';
import Logo from './logo';
import NavLinks from './nav-links';
import NavbarSessionComponent from './navbar-session-comp';
import { Bars3Icon } from '@heroicons/react/24/outline';
import MobileNavbar from '../mobile-navbar';
import SearchButton from './search-button';
import NotifButton from './notif-button';
import BookmarkButton from './bookmark-button';
import { toast } from 'react-hot-toast';

/**
 * Navbar component.
 * @param props.isLoggedIn - Whether the user is logged in
 * @returns JSX.Element - Navbar component
 */
export default function Navbar(props: { isLoggedIn: boolean }) {
  const [notifs, setNotifs] = useState(0);
  const [menuToggled, setMenuToggled] = useState(false);
  const [prevScrollPos, setPrevScrollPos] = useState(0);
  const [isNavVisible, setIsNavVisible] = useState(true);

  const toggleMenu = () => setMenuToggled(!menuToggled);

  useEffect(() => {
    if (props.isLoggedIn) {
      localStorage.clear();
      fetch('/api/get_notification_count', { credentials: 'include' })
        .then((response) => response.json())
        .then((data) => {
          setNotifs(data.count);
        })
        .catch(() => {
          toast.error('Error fetching notifications.');
        });
    }
  }, [notifs, props.isLoggedIn]);

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const handleScroll = () => {
    const currentScrollPos = window.pageYOffset;
    const isVisible = prevScrollPos > currentScrollPos || currentScrollPos === 0;

    // Hide/show navbar based on scroll direction or if at the top of the page
    setIsNavVisible(isVisible);

    // Update prevScrollPos for next scroll event
    setPrevScrollPos(currentScrollPos);
  };

  return (
    <div>
      <div className={`fixed top-0 z-10 h-20 w-full bg-bg-[#4C4B9B] transition-all duration-300 ${isNavVisible ? '' : '-translate-y-full'}`}>
        <div className='h-full px-4'>
          <div className='flex h-full items-center justify-between'>
            <div className='flex h-full items-center justify-between gap-x-8'>
              <Logo isOpen={menuToggled} toggle={toggleMenu} />
              <ul className='hidden gap-x-6 text-white md:flex'>
                <NavLinks session={props.isLoggedIn} />
              </ul>
            </div>
            <NavbarSessionComponent
              notifCount={notifs}
              isOpen={menuToggled}
              toggle={toggleMenu}
              session={props.isLoggedIn}
            />
            <div className='inline-flex items-center gap-4 text-white md:hidden'>
              <SearchButton isOpen={menuToggled} toggle={toggleMenu} />
              {props.isLoggedIn && <NotifButton notifCount={notifs} />}
              {props.isLoggedIn && (
                <BookmarkButton isOpen={menuToggled} toggle={toggleMenu} />
              )}
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
              session={props.isLoggedIn}
              notifCount={notifs}
            />
          </div>
        </>
      )}
    </div>
  );
}



/*
import React, { useState, useEffect } from 'react';
import Logo from './logo';
import NavLinks from './nav-links';
import NavbarSessionComponent from './navbar-session-comp';
import { Bars3Icon } from '@heroicons/react/24/outline';
import Sidebar from '../mobile-navbar';
import SearchButton from './search-button';
import NotifButton from './notif-button';
import BookmarkButton from './bookmark-button';
import { toast } from 'react-hot-toast';

export default function Navbar(props: { isLoggedIn: boolean }) {
  const [notifs, setNotifs] = useState(0);
  const [menuToggled, setMenuToggled] = useState(false);
  const toggleMenu = () => setMenuToggled(!menuToggled);

  // Fetch notification count on login
  useEffect(() => {
    if (props.isLoggedIn) {
      localStorage.clear();
      fetch('/api/get_notification_count', { credentials: 'include' })
        .then((response) => response.json())
        .then((data) => {
          setNotifs(data.count);
        })
        .catch(() => {
          toast.error('Error fetching notifications.');
        });
    }
  }, [notifs, props.isLoggedIn]);

  // Close mobile navbar on window resize
  useEffect(() => {
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768 && menuToggled) {
        setMenuToggled(false);
      }
    });
  }, [menuToggled]);

  return (
    <div>
      <div className='fixed top-0 z-10 h-20 w-full'>
        <div className='h-full px-4'>
          <div className='flex h-full items-center justify-between'>
            <div className='flex h-full items-center justify-between gap-x-8'>
              <Logo isOpen={menuToggled} toggle={toggleMenu} />
              <ul className='hidden gap-x-6 text-white md:flex'>
                <NavLinks session={props.isLoggedIn} />
              </ul>
            </div>
            <NavbarSessionComponent
              notifCount={notifs}
              isOpen={menuToggled}
              toggle={toggleMenu}
              session={props.isLoggedIn}
            />
            <div className='inline-flex items-center gap-4 text-white md:hidden'>
              <SearchButton isOpen={menuToggled} toggle={toggleMenu} />
              {props.isLoggedIn && <NotifButton notifCount={notifs} />}
              {props.isLoggedIn && (
                <BookmarkButton isOpen={menuToggled} toggle={toggleMenu} />
              )}
              <button type='button' onClick={toggleMenu} title='Menu'>
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
            <MobileNavbar
              isOpen={menuToggled}
              toggle={toggleMenu}
              session={props.isLoggedIn}
              notifCount={notifs}
            />
          </div>
        </>
      )}
    </div>
  );
}*/
