'use client';
import React, { useEffect, useState } from 'react';

export default function Home() {
  // Showing how to fetch data from the backend
  const [data, setData] = useState<any[]>([]);
  useEffect(() => {
    fetch('http://localhost:8080/api/example')
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setData(data);
      });
  }, []);

  return (
    <div className='m-8 rounded-lg bg-slate-200 p-8'>
      <div className='text-xl'>Welcome to TradeTalker.</div>
      <p>
        Stay informed about the latest news sentiment in the financial markets.
      </p>
      <br></br>
      <p>Below should show all users in the database.</p>
      <div className='rounded-lg bg-slate-300 p-4'>
        {data.map((user, index) => (
          <div className='m-4 rounded-lg bg-slate-100 p-2' key={index}>
            <p>User ID: {user.UserID}</p>
            <p>Username: {user.Username}</p>
            <p>Email: {user.Email}</p>
            <p>Password: {user.Password}</p>
            <p>Preferences: {user.Preferences}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
