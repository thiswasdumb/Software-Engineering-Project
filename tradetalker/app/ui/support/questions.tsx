import React from 'react';
import QuestionForm from '@/app/ui/support/question-form';

async function getQuestions() {
  const response = await fetch('http://localhost:8080/api/get_questions');
  if (!response.ok) {
    throw new Error('Error fetching questions');
  }
  return response.json();
}

export default async function Questions({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const questions: any[] = await getQuestions();

  return (
    <div className='m-8 rounded-lg bg-slate-200 p-8'>
      <div className='bold text-2xl'>Support</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <div className='text-xl'>FAQ</div>
      <hr className='my-2 w-[50%] rounded-lg border border-slate-400' />
      <div className='mt-2 w-[30%] rounded-lg bg-slate-200'>
        {questions.map((question, index) => (
          <div key={index} className='my-2'>
            <div className='text-lg'>{question.question}</div>
            <div className='text-lg'>{question.answer}</div>
            <hr className='my-2 rounded-lg border border-slate-400' />
          </div>
        ))}
      </div>
      <div className='mt-8 text-xl'>
        Send us a question and we&apos;ll get back to you!
      </div>
      <hr className='my-2 w-full rounded-lg border border-slate-400 md:w-[50%]' />
      {isLoggedIn ? (
        <QuestionForm />
      ) : (
        <p>
          You must&nbsp;
          <a
            href='/login'
            className='text-blue-600 underline hover:text-blue-700 active:text-orange-400'
          >
            login
          </a>{' '}
          before you can submit a question.
        </p>
      )}
    </div>
  );
}
