import React from 'react';

async function getQuestions() {
  const response = await fetch('http://localhost:8080/api/get_questions');
  if (!response.ok) {
    throw new Error('Error fetching questions');
  }
  return response.json();
}

export default async function Questions() {
  const questions: any[] = await getQuestions();

  return (
    <div className='m-8 rounded-lg bg-slate-200 p-8'>
      <div className='bold text-2xl'>Support</div>
      <hr className='my-2 rounded-lg border-2 border-slate-400' />
      <div className='text-xl'>Questions</div>
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
    </div>
  );
}
