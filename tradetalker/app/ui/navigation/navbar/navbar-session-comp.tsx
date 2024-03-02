import React from 'react';
import NotifButton from './notif-button';
import ProfileButton from './profile-button';
import SearchButton from './search-button';
import WhiteButtons from './white-buttons';

export default function NavbarSessionComponent(props: {
  notifCount: number;
  isOpen: boolean;
  toggle: () => void;
  session: boolean;
}) {
  if (props.session) {
    return (
      <>
        <ul className='text-white hidden gap-x-4 md:flex'>
          <SearchButton isOpen={props.isOpen} toggle={props.toggle} />
          <NotifButton notifCount={props.notifCount} />{' '}
          {/* Will update from db */}
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
