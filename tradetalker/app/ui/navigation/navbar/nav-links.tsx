import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';
import { Poppins } from 'next/font/google';

const pop700 = Poppins({ weight: '500', subsets: ['latin'] });

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
              'text-lg text-white text-bold px-4 py-2 ml-32 relative transition-colors duration-300',
              {
                'border-b-4 border-white': pathname === link.href,
              }
            )}
          >
            <p className={pop700.className + ' hidden md:block'}>
              {link.name}
              <span className="underline-animation"></span>
            </p>
          </Link>
        );
      })}
      <style jsx>{`
        .underline-animation {
          position: absolute;
          bottom: 0;
          left: 0;
          height: 3px;
          width: 0%;
          background-color: #4C4B9B;
          transition: width 0.3s ease-in-out;
        }

        p:hover .underline-animation {
          width: 100%;
        }
      `}</style>
    </>
  );
}
