import React from 'react';
import SidebarLinks from './sidebar-links';
import { XMarkIcon } from '@heroicons/react/24/outline';

const Sidebar = ({
  isOpen,
  toggle,
}: {
  isOpen: boolean;
  toggle: () => void;
}): JSX.Element => {
  const session = false; // TODO: replace with actual session
  return (
    <>
      <div
        className='h-100 fixed left-0 z-10 grid w-full justify-center overflow-hidden bg-white pt-[120px] md:hidden'
        style={{
          opacity: `${isOpen ? '1' : '0'}`,
          top: ` ${isOpen ? '0' : '-100%'}`,
        }}
      >
        <button className='absolute right-0 p-5' onClick={toggle}>
          <XMarkIcon className='h-12 w-12' />
        </button>
        <SidebarLinks toggle={toggle} session={session} />
      </div>
    </>
  );
};

export default Sidebar;
