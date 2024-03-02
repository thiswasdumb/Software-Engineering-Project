'use client';
import { toast } from 'react-hot-toast';

export default function Logout(isLoggedIn: boolean) {
  try {
    if (isLoggedIn) {
      fetch('/api/logout', { credentials: 'include' })
        .then((response) => response.json())
        .then(() => {
          window.location.href = '/home';
          toast.success('Logged out successfully.');
        })
        .catch(() => {
          toast.error('Error logging out.');
        });
    } else {
      window.location.href = '/login';
      toast.error('You must be logged in.');
    }
  } catch (error) {
    console.error('Error during logout:', error);
    toast.error('Error during logout.');
  }
}
