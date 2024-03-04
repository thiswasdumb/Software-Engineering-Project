import { ShareIcon } from '@heroicons/react/20/solid';

export default function Share() {
  return (
    <div>
      <button
        type='button'
        className='mt-2 rounded-lg bg-blue-500 p-2 text-white hover:bg-blue-600 active:bg-blue-700'
      >
        Share
        <ShareIcon className='ml-2 inline-block h-6 w-6' />
      </button>
    </div>
  );
}
