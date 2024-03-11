'use client';
import React, { useState } from 'react';
import toast from 'react-hot-toast';
import { Poppins } from 'next/font/google'

const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] })

export default function QuestionForm() {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    fetch('/api/submit_question', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          toast.error(data.error);
        }
        if (data.success) {
          toast.success(data.success);
          setQuestion('');
        }
      })
      .catch((error) => console.error(error));
  };

  return (
    <div>
      <form
        onSubmit={handleSubmit}
        method='post'
        className='mt-2 flex flex-col items-end md:items-start'
      >
        <label className='hidden' htmlFor='question'>
          Question
        </label>
        <textarea
          className={`w-full resize-none rounded p-2 hover:drop-shadow-lg md:w-[70%] ${pop400.className}`}
          placeholder='Enter a question...'
          rows={4}
          cols={4}
          name='question'
          minLength={1}
          maxLength={10000}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          required
        />
        <button
          type='submit'
          className={`mt-2 rounded-lg bg-[#5f5eb5] p-2 text-white hover:bg-[#4c4b9b] hover:drop-shadow-lg focus:bg-blue-700 ${pop400.className}`}
        >
          Submit
        </button>
      </form>
    </div>
  );
}
