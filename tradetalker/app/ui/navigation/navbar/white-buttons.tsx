'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';

/**
 * White buttons component.
 * @returns JSX.Element - White buttons component
 */
export default function WhiteButtons() {
  const pathname = usePathname();
  // Map of links to display in the navbar.
  const links = [
    { name: 'Log in', href: '/login' },
    { name: 'Sign up', href: '/signup' },
  ];
  return (
    <>
      {links.map((link) => {
        return (
          <Link
            key={link.name}
            href={link.href}
            className={clsx(
              'items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-base font-medium hover:bg-sky-100 hover:text-blue-600 focus:text-blue-800',
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
