import React from 'react';

async function getBookmarks() {
  const response = await fetch('http://localhost:8080/api/get_bookmarks');
  if (!response.ok) {
    throw new Error('Error fetching bookmarks');
  }
  return response.json();
}

export default async function BookmarkComponent({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const bookmarks: any[] = await getBookmarks();

  return (
    isLoggedIn && (
      <div className='bg-slate-200 m-8 rounded-lg p-8'>
        <div className='text-2xl'>Bookmarks</div>
        <hr className='border-slate-400 my-2 rounded-lg border-2' />
        <div>
          {bookmarks.map((bookmark, index) => (
            <div
              className='bg-slate-100 m-4 overflow-scroll rounded-lg p-2'
              key={index}
            >
              <p>Timestamp: {bookmark.Time}</p>
              <p>Message: {bookmark.Content}</p>
            </div>
          ))}
        </div>
      </div>
    )
  );
}
