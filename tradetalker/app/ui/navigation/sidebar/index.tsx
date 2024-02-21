import React from 'react';
import SidebarLinks from './sidebar-links';

export default function Sidebar(props: {
  isOpen: boolean;
  toggle: () => void;
  session: boolean;
  notifCount: number;
}) {
  return (
    <>
      <div
        className='sticky block w-full justify-center bg-gray-200 md:hidden'
        style={{
          display: `${props.isOpen ? 'block' : 'none'}`,
        }}
      >
        <SidebarLinks
          toggle={props.toggle}
          session={props.session}
          notifCount={props.notifCount}
        />
      </div>
    </>
  );
}
