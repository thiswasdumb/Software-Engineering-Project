'use client';

import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useSearchParams, usePathname, useRouter } from 'next/navigation';
import { useDebouncedCallback } from 'use-debounce';

export default function SearchBar({ placeholder }: { placeholder: string }) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  const handleSearch = useDebouncedCallback((term: string) => {
    const result = fetch(`/api/search/${term}`);
    console.log(result); // Placeholder for the actual search functionality
    const params = new URLSearchParams(searchParams);
    params.set('page', '1');
    if (term) {
      params.set('query', term);
    } else {
      params.delete('query');
    }
    replace(`${pathname}?${params.toString()}`);
  }, 300);

  return (
    <>
      <div>
        <div className='relative'>
          <label htmlFor='search' className='sr-only'>
            Search
          </label>
          <input
            name='search'
            className='block w-full rounded-md border border-gray-200 py-[9px] pl-10 text-lg outline-2 placeholder:text-gray-500 md:text-sm'
            placeholder={placeholder}
            onChange={(e) => {
              handleSearch(e.target.value);
            }}
            defaultValue={searchParams.get('query')?.toString()}
          />
          <MagnifyingGlassIcon className='absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900' />
        </div>
        <div className='flex justify-center pt-4 text-center'>
          <div className='text-xs text-gray-500'>
            {searchParams.get('query') !== null &&
              `Showing results for "${searchParams.get('query')}"`}
          </div>
        </div>
        {searchParams.get('query') == null && (
          <div className='flex justify-center pt-20 text-center text-xl text-black '>
            Start typing to search for news articles or companies.
          </div>
        )}
      </div>
    </>
  );
}
