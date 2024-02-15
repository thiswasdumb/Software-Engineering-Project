'use client';
import React, { useEffect, useState } from 'react';

export default function Home() {
  // Showing how to fetch data from the backend
  const [message, setMessage] = useState("Loading...");
  const [data, setData] = useState([]);
  useEffect(() => {
    fetch("http://localhost:8080/api/home")
      .then((response) => response.json())
      .then((data) => {
        setMessage(data.message);
        setData(data.data);
      });
  }, []);

  return (
    <div className="p-8 bg-slate-200 m-8 rounded-lg">
      <div className="text-xl">Welcome to TradeTalker.</div>
      <p>Stay informed about the latest news sentiment in the financial markets.</p>
      <br></br>
      <p>If you see text below then Flask is working :)</p>
      <div className="p-4 bg-slate-300 rounded-lg">
        {message}
        {data.map((item, index) => (
          <div className="p-2" key={index}>{item}</div>
        ))}
      </div>
    </div>
  );
}