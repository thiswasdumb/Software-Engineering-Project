import React from 'react';
import { Metadata } from 'next';
import ProfileComponent from '../ui/profile';
import { cookies } from 'next/headers';

export const metadata: Metadata = {
  title: 'Profile',
};

export default function Profile() {
  const session = cookies().get('session') !== undefined;
  return <ProfileComponent isLoggedIn={session} />;
}
