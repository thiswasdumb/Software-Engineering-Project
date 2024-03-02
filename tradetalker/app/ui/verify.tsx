'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';

export default function VerifyUser() {
  const router = useRouter();
  useEffect(() => {
    fetch('/api/verify')
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          router.push('/dashboard');
          toast.success(data.success);
        } else {
          router.push('/signup');
          toast.error('You must have an account to verify your email.');
        }
      })
      .catch(() => {
        toast.error('Error verifying user.');
      });
  }, [router]);
  return null;
}
