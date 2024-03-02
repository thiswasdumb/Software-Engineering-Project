'use client';
import React, { useState } from 'react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useSearchParams, usePathname, useRouter } from 'next/navigation';
import { useDebouncedCallback } from 'use-debounce';
import { toast } from 'react-hot-toast';
import Link from 'next/link';

export default function SearchBar({ placeholder }: { placeholder: string }) {
  const [articles, setArticles] = useState<any[]>([]);
  const [companies, setCompanies] = useState<any[]>([]);
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  const handleSearch = useDebouncedCallback((term: string) => {
    if (term !== '') {
      fetch(`/api/search/${term}`)
        .then((response) => response.json())
        .then((data) => {
          setArticles(data.articles);
          setCompanies(data.companies);
        })
        .catch((error) => {
          console.error('Error fetching search results', error);
          toast.error('Error fetching search results.');
        });
    }

    const params = new URLSearchParams(searchParams);
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
            className='border-gray-200 placeholder:text-gray-500 block w-full rounded-md border py-[9px] pl-10 text-lg outline-2 md:text-sm'
            placeholder={placeholder}
            onChange={(e) => {
              handleSearch(e.target.value);
            }}
            defaultValue={searchParams.get('query')?.toString()}
          />
          <MagnifyingGlassIcon className='text-gray-500 peer-focus:text-gray-900 absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2' />
        </div>
        <div className='flex justify-center pt-4 text-center'>
          <div className='text-gray-500 text-xs'>
            {searchParams.get('query') !== null &&
              `Showing results for "${searchParams.get('query')}"`}
          </div>
        </div>
        {searchParams.get('query') == null && (
          <div className='text-black flex justify-center pt-20 text-center text-xl '>
            Start typing to search for news articles or companies.
          </div>
        )}
        {searchParams.get('query') !== null && (
          <div className='flex flex-col md:flex-row'>
            <div className='bg-slate-200 m-8 rounded-lg p-8 md:w-[50%]'>
              <div className='text-2xl'>Articles</div>
              <hr className='border-slate-400 my-2 rounded-lg border-2' />
              {articles.length === 0 && (
                <div className='text-gray-600'>No matching articles found.</div>
              )}
              <div className='flex flex-col justify-between'>
                {articles.map((article, index) => (
                  <Link
                    key={index}
                    className='opacity:30 bg-slate-300 hover:bg-slate-400 my-2 w-full rounded-lg p-2 transition hover:bg-opacity-60'
                    href={`/article/${article.id}`}
                  >
                    <div>
                      {getHighlightedText(
                        article.title,
                        searchParams.get('query')
                      )}
                    </div>
                    <div>{article.summary}</div>
                  </Link>
                ))}
              </div>
            </div>
            <div className='bg-slate-200 m-8 rounded-lg p-8 md:w-[50%]'>
              <div className='text-2xl'>Companies</div>
              <hr className='border-slate-400 my-2 rounded-lg border-2' />
              <div className='md:max-[80%]'>
                {companies.length === 0 && (
                  <div className='text-gray-600'>
                    No matching companies found.
                  </div>
                )}
                <div className='flex flex-col justify-between'>
                  {companies.map((company, index) => (
                    <Link
                      key={index}
                      className='opacity:30 bg-slate-300 hover:bg-slate-400 my-2 w-full rounded-lg p-2 transition hover:bg-opacity-60'
                      href={`/company/${company.id}`}
                    >
                      <div>
                        {getHighlightedText(
                          company.name,
                          searchParams.get('query')
                        )}
                      </div>
                      <div>{company.stock_symbol}</div>
                      <div className='text-base'>{company.stock_price}</div>
                      <div className='text-sm'>{company.industry}</div>
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export function getHighlightedText(text: string, highlight: string | null) {
  // Split text on highlighted term, include term itself into parts, ignore case
  if (highlight === null) {
    return text;
  }
  const parts = text.split(new RegExp(`(${highlight})`, 'gi'));
  return (
    <span>
      {parts.map((part, key) =>
        part.toLowerCase() === highlight.toLowerCase() ? (
          <span className='bg-yellow-400' key={key}>
            {part}
          </span>
        ) : (
          part
        )
      )}
    </span>
  );
}
