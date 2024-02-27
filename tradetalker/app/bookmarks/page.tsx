import React from 'react';
import { Metadata } from 'next';
import { cookies } from 'next/headers';
import BookmarkComponent from '../ui/bookmarks';

export const metadata: Metadata = {
  title: 'Bookmarks',
};

export default function Bookmarks() {
  const session = cookies().get('session') !== undefined;
  return <BookmarkComponent isLoggedIn={session} />;
}
