'use client';
import { Metadata } from 'next';
import { useRouter } from 'next/navigation';

export const metadata: Metadata = {
  title: 'Not Found',
};

export default function NotFound() {
  const router = useRouter();
  return (
    <div className='flex flex-col justify-center rounded-lg bg-slate-200 p-4'>
      <p>Could not find requested resource.</p>
      <button
        type='button'
        onClick={() => router.back()}
        className='rounded-lg bg-blue-500 p-4 text-white transition hover:bg-blue-600'
      >
        Back
      </button>
    </div>
  );
}
