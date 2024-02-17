import React from 'react';
import { useSession } from 'next-auth/react';
import NotifButton from './notif-icon';
import ProfileButton from './profile-button';
import SearchButton from './search-button';
import WhiteButtons from './white-buttons';

export default function NavbarComponent(props: { session: any }) {
  if (props.session) {
    return (
      <ul className="hidden md:flex gap-x-4 text-white">
        <SearchButton />
        <NotifButton />
        <ProfileButton />
      </ul>
    );
  } else {
    return (
      <ul className="hidden md:flex items-center gap-x-6">
        <div className="text-white">
          <SearchButton />
        </div>
        <WhiteButtons />
      </ul>
    );
  }
}