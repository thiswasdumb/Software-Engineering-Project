'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function RedirectPage() {
  const router = useRouter();
  useEffect(() => {
    // Redirect to another page
    router.push('/api/redirect');
  }, [router]);

  return (
    <div className='m-8 rounded-lg bg-slate-200 p-8'>
      <div className='text-2xl'>Redirecting...</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
    </div>
  );
}

export function RedirectWithMessage(destination: string, message: string) {
  localStorage.setItem('message', message); // Store message for one session
  window.location.href = destination; // Redirect to another page
}
