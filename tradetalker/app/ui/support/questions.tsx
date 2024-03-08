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
      <h1 className='bold text-2xl'>Support</h1>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <h2 className='text-xl'>FAQ</h2>
      <hr className='my-2 w-[50%] rounded-lg border border-slate-400' />
      <div className='mt-2 rounded-lg bg-slate-200'>
        {questions.map((question, index) => (
          <div key={index} className='my-2'>
            <h3 className='text-lg'>{question.question}</h3>
            <p>{question.answer}</p>
            <hr className='my-2 rounded-lg border border-slate-400' />
          </div>
        ))}
      </div>
      <h2 className='mt-8 text-xl'>
        Send us a question and we&apos;ll get back to you!
      </h2>
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
          </a>
          &nbsp;before you can submit a question.
        </p>
      )}
    </div>
  );
}
