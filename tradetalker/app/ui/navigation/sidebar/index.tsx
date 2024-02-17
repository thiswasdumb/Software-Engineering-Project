import React from 'react';
import Link from 'next/link';
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
        className="fixed w-full h-100 md:hidden overflow-hidden justify-center bg-white grid pt-[120px] left-0 z-10"
        style={{
          opacity: `${isOpen ? "1" : "0"}`,
          top: ` ${isOpen ? "0" : "-100%"}`,
        }}
      >
        <button className="absolute right-0 p-5" onClick={toggle}>
          <XMarkIcon className="w-12 h-12" />
        </button>
        <SidebarLinks toggle={toggle} session={session} />
      </div>
    </>
  );
};

export default Sidebar;