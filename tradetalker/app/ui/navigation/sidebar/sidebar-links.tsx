'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';

export default function SidebarLinks(props: {
  toggle: () => void;
  session: boolean;
  notifCount: number;
}) {
  // Map of links to display in the navbar.
  const links = [
    ...(props.session ? [{ name: 'Dashboard', href: '/dashboard' }] : []),
    { name: 'Stocks', href: '/stocks' },
    { name: 'Companies', href: '/companies' },
    { name: 'Support', href: '/support' },
    ...(props.session
      ? [
          {
            name: `Notifications (${props.notifCount})`,
            href: '/notifications',
          },
          { name: 'Profile', href: '/profile' },
          { name: 'Log out', href: '/logout' },
        ]
      : [
          { name: 'Login', href: '/login' },
          { name: 'Sign up', href: '/signup' },
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
            onClick={props.toggle}
            className={clsx(
              'sticky flex justify-center border-b-2 bg-white p-4 font-medium outline-gray-100 hover:bg-sky-100 hover:text-blue-600',
              {
                'bg-sky-200 text-blue-600': pathname === link.href,
              }
            )}
          >
            <p className='text-xl'>{link.name}</p>
          </Link>
        );
      })}
    </>
  );
}
