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
              'border-b-4 border-transparent bg-blue-600 p-2 text-base font-medium transition duration-150 hover:border-slate-300 focus:border-white md:flex-none md:justify-start',
              {
                'border-b-4 border-white': pathname === link.href,
              }
            )}
          >
            <button type='button'>
              <p className='hidden md:block'>{link.name}</p>
            </button>
          </Link>
        );
      })}
    </>
  );
}
