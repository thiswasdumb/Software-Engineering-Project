export default function Loading({ message }: { message: string }) {
  return (
    <div className='absolute bottom-1/2 right-1/2 m-auto translate-x-1/2 translate-y-1/2 transform '>
      <div className='border-slate-500 border-t-transparent m-auto h-32 w-32 animate-spin rounded-full border-8 border-solid'></div>
      <div className='text-slate-500 m-3 text-center text-2xl'>{message}</div>
    </div>
  );
}
