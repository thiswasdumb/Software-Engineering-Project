'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Logout from 'app/ui/logout';
import clsx from 'clsx';

export default function MobileNavLinks(props: {
  toggle: () => void;
  session: boolean;
  notifCount: number;
}) {
  // Map of links to display in the navbar.
  const links = [
    ...(props.session
      ? [{ name: 'Dashboard', href: '/dashboard', onClick: props.toggle }]
      : []),
    { name: 'Stocks', href: '/stocks', onClick: props.toggle },
    { name: 'Companies', href: '/companies', onClick: props.toggle },
    { name: 'Support', href: '/support', onClick: props.toggle },
    ...(props.session
      ? [
          {
            name: `Notifications (${props.notifCount})`,
            href: '/notifications',
            onClick: props.toggle,
          },
          { name: 'Bookmarks', href: '/bookmarks', onClick: props.toggle },
          { name: 'Profile', href: '/profile', onClick: props.toggle },
        ]
      : [
          { name: 'Login', href: '/login', onClick: props.toggle },
          { name: 'Sign up', href: '/signup', onClick: props.toggle },
        ]),
  ];
  const pathname = usePathname();

  return (
    <>
      {links.map((link) => {
        return (
          <Link
            key={link.name}
            href={link.href}
            onClick={link.onClick}
            className={clsx(
              'sticky flex justify-center border-b-2 bg-white p-4 font-medium outline-gray-100 transition hover:bg-sky-100 hover:text-blue-600',
              {
                'bg-sky-200 text-blue-600': pathname === link.href,
              }
            )}
          >
            <button type='button'>
              <p className='text-xl'>{link.name}</p>
            </button>
          </Link>
        );
      })}
      {props.session && (
        <div
          onClick={() => Logout(props.session)}
          className='sticky flex justify-center border-b-2 bg-white p-4 font-medium outline-gray-100 transition hover:bg-sky-100 hover:text-blue-600'
        >
          <button type='button'>
            <p className='text-xl'>Log out</p>
          </button>
        </div>
      )}
    </>
  );
}
