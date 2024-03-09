'use client';
import { useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { toast } from 'react-hot-toast';
import { useRouter } from 'next/navigation';

/**
 * Read URL parameters.
 * @param url - The URL to redirect to
 * @returns null
 */
export default function ReadParams({ url }: { url: string }) {
  const params = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    if (params.get('error')) {
      toast.error(params.get('error'));
    }
    if (params.get('success')) {
      toast.success(params.get('success'));
    }
    router.replace(`/${url}`, undefined);
  }, [params, router, url]);
  return null;
}
