'use client';
import React, { useState, useEffect } from 'react';

export default function Description({ description }: { description: string }) {
  const [showMore, setShowMore] = useState(false);
  const [descriptionText, setDescriptionText] = useState('');

  useEffect(() => {
    if (description.length > 500) {
      setDescriptionText(description.slice(0, 500).concat('...'));
    } else {
      setDescriptionText(description);
    }
  }, [description]);

  const handleShowMore = () => {
    setShowMore(!showMore);
    if (showMore) {
      setDescriptionText(description.slice(0, 500).concat('...'));
    } else {
      setDescriptionText(description);
    }
  };

  return (
    <div className=''>
      <p>{descriptionText}</p>
      {description.length > 500 && (
        <button
          type='button'
          onClick={handleShowMore}
          className='text-blue-600 transition hover:text-blue-500'
        >
          {showMore ? 'Show less' : 'Show more'}
        </button>
      )}
    </div>
  );
}
