import React from 'react';
import { Metadata } from 'next';
import { cookies } from 'next/headers';
import DashboardComponent from '../ui/dashboard/dashboard';

export const metadata: Metadata = {
  title: 'Dashboard',
};

export default function Dashboard() {
  const session = cookies().get('session') !== undefined;
  return <DashboardComponent isLoggedIn={session} />;
}
