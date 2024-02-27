import React from 'react';
import { Metadata } from 'next';
import NotifComponent from '../ui/notif-component';
import { cookies } from 'next/headers';

export const metadata: Metadata = {
  title: 'Notifications',
};

export default function Notifications() {
  const session = cookies().get('session') !== undefined;
  return <NotifComponent isLoggedIn={session} />;
}
