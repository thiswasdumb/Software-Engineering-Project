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
      <div className='m-8 rounded-lg bg-slate-200 p-8'>
        <div className='text-2xl'>Bookmarks</div>
        <hr className='my-2 rounded-lg border-2 border-slate-400' />
        <div>
          {bookmarks.map((bookmark, index) => (
            <div
              className='m-4 overflow-scroll rounded-lg bg-slate-100 p-2'
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
