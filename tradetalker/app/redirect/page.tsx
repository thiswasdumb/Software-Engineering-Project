'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function RedirectPage() {
  const router = useRouter();
  useEffect(() => {
    // Redirect to another page
    router.push('http://localhost:8080/api/redirect');
  }, [router]);

  return <div>Redirecting...</div>;
}
