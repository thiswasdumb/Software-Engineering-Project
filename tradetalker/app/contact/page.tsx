export default function ContactPage() {
  return (
    <div className='m-8 flex flex-col rounded-lg bg-slate-200 p-8'>
      <div className='text-2xl'>Contact</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <p>
        For general concerns about the site, please contact us at{' '}
        <a
          href='mailto:support@tradetalker.co.uk'
          className='text-blue-600 hover:text-blue-500'
        >
          support@tradetalker.co.uk
        </a>
        . Otherwise, please DM us on Twitter at{' '}
        <a
          href='https://twitter.com/tradetalk'
          className='text-blue-600 hover:text-blue-500'
        >
          @tradetalk
        </a>
        .
      </p>
    </div>
  );
}
