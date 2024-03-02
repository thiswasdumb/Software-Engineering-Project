'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';

export default function NavLinks(props: { session: boolean }) {
  // Map of links to display in the navbar.
  const links = [
    ...(props.session ? [{ name: 'Dashboard', href: '/dashboard' }] : []),
    { name: 'Stocks', href: '/stocks' },
    { name: 'Companies', href: '/companies' },
    { name: 'Support', href: '/support' },
  ];
  const pathname = usePathname();

  return (
    <>
      {links.map((link) => {
        return (
          <Link
            key={link.name}
            href={link.href}
            className={clsx(
              'border-transparent bg-blue-600 hover:border-slate-300 focus:border-white border-b-4 p-2 text-base font-medium transition duration-150 md:flex-none md:justify-start',
              {
                'border-white border-b-4': pathname === link.href,
              }
            )}
          >
            <p className='hidden md:block'>{link.name}</p>
          </Link>
        );
      })}
    </>
  );
}
