'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';

export default function SidebarLinks(props: {
  toggle: () => void;
  session: boolean;
}) {
  // Map of links to display in the navbar.
  const links = [
    ...(props.session ? [{ name: 'Dashboard', href: '/dashboard' }] : []),
    { name: 'Stocks', href: '/stocks' },
    { name: 'Companies', href: '/companies' },
    { name: 'Support', href: '/support' },
    { name: 'Search', href: '/search' },
    ...(props.session
      ? [
          { name: 'Login', href: '/login' },
          { name: 'Signup', href: '/signup' },
        ]
      : []),
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
              'p-3 text-base font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start',
              {
                'bg-sky-100 text-blue-600': pathname === link.href,
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
