export default function PrivacyPage() {
  return (
    <div className='m-8 flex flex-col rounded-lg bg-slate-200 p-8'>
      <h1 className='text-2xl'>Privacy Policy</h1>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <p className='mt-2'>
        This is the privacy policy for our website. It explains how we collect,
        use, and protect your personal information.
      </p>
      <h2 className='mt-4 text-xl'>Information we collect</h2>
      <hr className='border-1 my-2 rounded-lg border-slate-400' />
      <p>
        We may collect certain personal information, such as your name and email
        address when you interact with our website.
      </p>
      <h2 className='mt-4 text-xl'>How we use your information</h2>
      <hr className='border-1 my-2 rounded-lg border-slate-400' />
      <p>
        We use the information we collect to provide and improve our services,
        communicate with you, and personalize your experience on our website.
      </p>
      <h2 className='mt-4 text-xl'>Information sharing</h2>
      <hr className='border-1 my-2 rounded-lg border-slate-400' />
      <p>
        We do not sell, trade, or otherwise transfer your personal information
        to outside parties without your consent.
      </p>
      <h2 className='mt-4 text-xl'>Security</h2>
      <hr className='border-1 my-2 rounded-lg border-slate-400' />
      <p>
        We take reasonable measures to protect your personal information from
        unauthorized access, use, or disclosure.
      </p>
      <h2 className='mt-4 text-xl'>Changes to this privacy policy</h2>
      <hr className='border-1 my-2 rounded-lg border-slate-400' />
      <p>
        We may update this privacy policy from time to time. Any changes will be
        posted on this page.
      </p>
      <h2 className='mt-4 text-xl'>Contact us</h2>
      <hr className='border-1 my-2 rounded-lg border-slate-400' />
      <p>
        If you have any questions or concerns about our privacy policy, please
        contact us at{' '}
        <a
          href='mailto:support@tradetalk.co.uk'
          className='text-blue-600 hover:text-blue-500'
        >
          support@tradetalk.co.uk
        </a>
        .
      </p>
    </div>
  );
}
