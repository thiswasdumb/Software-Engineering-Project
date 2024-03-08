/**
 * Loading component.
 * @param message - The message to display
 * @returns 
 */
export default function Loading({ message }: { message: string }) {
  return (
    <div className='absolute bottom-1/2 right-1/2 m-auto translate-x-1/2 translate-y-1/2 transform '>
      <div className='m-auto h-32 w-32 animate-spin rounded-full border-8 border-solid border-slate-500 border-t-transparent'></div>
      <span className='m-3 text-center text-2xl text-slate-500'>{message}</span>
    </div>
  );
}
