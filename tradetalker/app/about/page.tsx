/**
 * About page.
 * @returns JSX.Element - About page
 */
export default function AboutPage() {
  return (
    <div className='m-8 flex flex-col rounded-lg bg-slate-200 p-8'>
      <h1 className='text-2xl'>About</h1>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <p>
        TradeTalk is a news platform for traders and investors. We provide
        high-quality analysis of the latest financial news. Let&apos;s talk
        trade.
      </p>
      <p className='mt-4'>TradeTalk was created by:</p>
      <ul className='list-inside list-disc'>
        <li>Serene Alrawi</li>
        <li>Shayan Borhani Yazdi</li>
        <li>Louis Hudson</li>
        <li>Gabriel Hughes</li>
        <li>Xun Khang Tan</li>
        <li>Hao-Yen Tang</li>
        <li>Alara Tindall</li>
      </ul>
      <p className='mt-4'>
        Visit the{' '}
        <a
          href='https://github.com/thiswasdumb/SoftEngProject'
          target='_blank'
          className='mt-4 text-blue-500 hover:text-blue-600 active:text-orange-500'
        >
          GitHub repository
        </a>{' '}
        to find the website&apos;s code.
      </p>
    </div>
  );
}
