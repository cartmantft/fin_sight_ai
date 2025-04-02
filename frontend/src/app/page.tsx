"use client";

import { useState, useEffect } from 'react';

async function fetchData() {
  const response = await fetch('http://localhost:8000/');
  const data = await response.json();
  return data.message;
}

export default function Home() {
  const [message, setMessage] = useState('');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    async function loadData() {
      const fetchedMessage = await fetchData();
      setMessage(fetchedMessage);
    }

    loadData();
  }, []);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    const response = await fetch('http://localhost:8000/items/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, description }),
    });
    const data = await response.json();
  };

  return (
    <div>
      <h1>FinSight AI</h1>
      <p>{message}</p>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <input type="text" placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
        <button type="submit">Create Item</button>
      </form>
    </div>
  );
}
