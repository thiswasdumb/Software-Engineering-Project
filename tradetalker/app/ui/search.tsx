'use client';
import React, { useState } from 'react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useSearchParams, usePathname, useRouter } from 'next/navigation';
import { useDebouncedCallback } from 'use-debounce';
import { toast } from 'react-hot-toast';
import Link from 'next/link';
import dayjs from 'dayjs';

/**
 * Search bar component.
 * @param placeholder - The placeholder text
 * @returns JSX.Element - Search bar component
 */
export default function SearchBar({ placeholder }: { placeholder: string }) {
  const [articles, setArticles] = useState<any[]>([]);
  const [keyArticles, setKeyArticles] = useState<any[]>([]);
  const [companies, setCompanies] = useState<any[]>([]);
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  // Fetch search results
  const handleSearch = useDebouncedCallback((term: string) => {
    if (term !== '') {
      fetch(`/api/search/${term}`)
        .then((response) => response.json())
        .then((data) => {
          setArticles(data.article_titles);
          setKeyArticles(data.article_keywords);
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
          <p className='flex justify-center pt-20 text-center text-xl text-black'>
            Start typing to search for news articles or companies.
          </p>
        )}
        {searchParams.get('query') !== null && (
          <div className='flex flex-col md:flex-row md:items-start'>
            <div className='m-4 rounded-lg bg-slate-200 p-8 md:w-[33%]'>
              <h1 className='text-2xl'>Articles (by title)</h1>
              <hr className='my-2 rounded-lg border-2 border-slate-400' />
              {articles.length === 0 && (
                <span className='text-gray-600'>
                  No matching articles found.
                </span>
              )}
              <div className='flex flex-col justify-between'>
                {articles.map((article, index) => (
                  <Link
                    key={index}
                    className='opacity:30 my-2 w-full rounded-lg bg-slate-300 p-2 transition hover:bg-slate-400 hover:bg-opacity-60'
                    href={`/article/${article.id}`}
                  >
                    <div className='flex flex-row flex-wrap justify-between'>
                      <div>
                        {getHighlightedText(
                          article.title,
                          searchParams.get('query')
                        )}
                      </div>
                      <span className='text-sm text-gray-600'>
                        {dayjs(article.date).format('D MMM YYYY')}
                      </span>
                    </div>
                    <div>{article.summary}</div>
                  </Link>
                ))}
              </div>
            </div>
            <div className='m-4 rounded-lg bg-slate-200 p-8 md:w-[33%]'>
              <h1 className='text-2xl'>Articles (by keyword)</h1>
              <hr className='my-2 rounded-lg border-2 border-slate-400' />
              {keyArticles.length === 0 && (
                <span className='text-gray-600'>
                  No matching articles found.
                </span>
              )}
              <div className='flex flex-col justify-between'>
                {keyArticles.map((article, index) => (
                  <Link
                    key={index}
                    className='opacity:30 my-2 w-full rounded-lg bg-slate-300 p-2 transition hover:bg-slate-400 hover:bg-opacity-60'
                    href={`/article/${article.id}`}
                  >
                    <div className='flex flex-row flex-wrap justify-between'>
                      <div>
                        {article.title}
                      </div>
                      <span className='text-sm text-gray-600'>
                        {dayjs(article.date).format('D MMM YYYY')}
                      </span>
                    </div>
                    <div>{article.summary}</div>
                  </Link>
                ))}
              </div>
            </div>
            <div className='m-4 rounded-lg bg-slate-200 p-8 md:w-[33%]'>
              <h1 className='text-2xl'>Companies</h1>
              <hr className='my-2 rounded-lg border-2 border-slate-400' />
              <div className='md:max-[80%]'>
                {companies.length === 0 && (
                  <span className='text-gray-600'>
                    No matching companies found.
                  </span>
                )}
                <div className='flex flex-col justify-between'>
                  {companies.map((company, index) => (
                    <Link
                      key={index}
                      className='opacity:30 my-2 w-full rounded-lg bg-slate-300 p-2 transition hover:bg-slate-400 hover:bg-opacity-60'
                      href={`/company/${company.id}`}
                    >
                      <div>
                        {getHighlightedText(
                          company.symbol,
                          searchParams.get('query')
                        )}
                        &nbsp;|&nbsp;
                        {getHighlightedText(
                          company.name,
                          searchParams.get('query')
                        )}
                      </div>
                      <p className='text-base'>{company.stock_price}</p>
                      <p className='text-sm'>{company.industry}</p>
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
