'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';

// Map of links to display in the navbar.
const links = [
  { name: 'Log in', href: '/login' },
  { name: 'Sign up', href: '/signup' },
];

export default function WhiteButtons() {
  const pathname = usePathname();
  return (
    <>
      {links.map((link) => {
        return (
          <Link
            key={link.name}
            href={link.href}
            className={clsx(
              'bg-gray-50 hover:bg-sky-100 hover:text-blue-600 focus:text-blue-800 items-center justify-center gap-2 rounded-md p-3 text-base font-medium',
              {
                'bg-sky-100 text-blue-800': pathname === link.href,
              }
            )}
          >
            {link.name}
          </Link>
        );
      })}
    </>
  );
}
