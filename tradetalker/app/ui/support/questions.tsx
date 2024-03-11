import React from 'react';
import QuestionForm from '@/app/ui/support/question-form';
import CursorAnimation from './CursorAnimation';
import { Poppins } from 'next/font/google';
import './style.css';

const pop = Poppins({ weight: ['600'], subsets: ['latin'] });
const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });
const pop500 = Poppins({ weight: ['500'], subsets: ['latin'] });

async function getQuestions() {
  const response = await fetch('http://localhost:8080/api/get_questions');
  if (!response.ok) {
    throw new Error('Error fetching questions');
  }
  return response.json();
}

/**
 * Questions component
 * @param isLoggedIn - Whether the user is logged in
 * @returns Promise - Questions component
 */
export default async function Questions({
  isLoggedIn,
}: {
  isLoggedIn: boolean;
}) {
  const questions: any[] = await getQuestions();

  return (
    <div className=''>
      <div className='dark-over'>
        <div className='moveup'>
          <CursorAnimation />
        </div>
      </div>
      <div className='dark-rec'>
        <div className={pop.className}>
          <span className='text-bold text-white' style={{ fontSize: '7rem' }}>
            Support
          </span>
        </div>
      </div>
      <hr
        className='mb-4'
        style={{
          backgroundColor: '#4C4B9B',
          height: '10px',
          marginTop: '-5.45%',
        }}
      />
      <br />
      <div className='moveright'>
        <div
          className={pop.className}
          className='underlinesimple'
          style={{ fontSize: '2.4rem' }}
        >
          Frequently Asked Questions
        </div>{' '}
        <br />
        <div className='mt-4 w-[70%]'>
          {questions.map((question, index) => (
            <div key={index} className='my-2'>
              <div className={pop500.className} style={{ fontSize: '1.5rem' }}>
                {question.question}
              </div>
              <div
                className={pop400.className}
                style={{ fontSize: '1.2rem', color: '#5554ab' }}
              >
                {question.answer}
              </div>
              <hr
                className='my-2 mb-2 rounded-lg'
                style={{
                  backgroundColor: '#43428f',
                  height: '3px',
                  marginTop: '2%',
                }}
              />
            </div>
          ))}
        </div>{' '}
        <br />
        <div className={pop500.className} style={{ fontSize: '1.3rem' }}>
          Send us a question and we&apos;ll get back to you!
        </div>
        <hr
          className='my-2 w-full rounded-lg border border-slate-400 md:w-[50%]'
          style={{ backgroundColor: '#43428f', height: '3px' }}
        />
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
    </div>
  );
}
