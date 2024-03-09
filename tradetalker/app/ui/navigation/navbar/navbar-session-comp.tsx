import React from 'react';
import NotifButton from './notif-button';
import ProfileButton from './profile-button';
import SearchButton from './search-button';
import WhiteButtons from './white-buttons';
import BookmarkButton from './bookmark-button';

/**
 * Navbar session component.
 * @param props.notifCount - Number of notifications
 * @param props.isOpen - Whether the mobile navbar is open
 * @param props.toggle - Function to toggle the mobile navbar
 * @param props.session - Whether the user is logged in
 * @returns JSX.Element - Navbar session component
 */
export default function NavbarSessionComponent(props: {
  notifCount: number;
  isOpen: boolean;
  toggle: () => void;
  session: boolean;
}) {
  if (props.session) {
    return (
      <>
        <ul className='hidden gap-x-4 text-white md:flex'>
          <SearchButton isOpen={props.isOpen} toggle={props.toggle} />
          <BookmarkButton isOpen={props.isOpen} toggle={props.toggle} />
          <NotifButton notifCount={props.notifCount} />
          <ProfileButton />
        </ul>
      </>
    );
  }
  return (
    <>
      <ul className='hidden items-center gap-x-6 md:flex'>
        <div className='text-white'>
          <SearchButton isOpen={props.isOpen} toggle={props.toggle} />
        </div>
        <WhiteButtons />
      </ul>
    </>
  );
}
