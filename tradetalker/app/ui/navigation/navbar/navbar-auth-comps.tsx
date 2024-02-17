import React from 'react';
import NotifButton from './notif-icon';
import ProfileButton from './profile-button';
import SearchButton from './search-button';
import WhiteButtons from './white-buttons';

export default function NavbarComponent(props: { session: boolean }) {
  if (props.session) {
    return (
      <ul className='hidden gap-x-4 text-white md:flex'>
        <SearchButton />
        <NotifButton />
        <ProfileButton />
      </ul>
    );
  } else {
    return (
      <ul className='hidden items-center gap-x-6 md:flex'>
        <div className='text-white'>
          <SearchButton />
        </div>
        <WhiteButtons />
      </ul>
    );
  }
}
