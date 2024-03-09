'use client';
import { useState, useEffect } from 'react';

/**
 * Description component.
 * @param description - Company description
 * @returns JSX.Element - Description component
 */
export default function Description({ description }: { description: string }) {
  const [showMore, setShowMore] = useState(false);
  const [descriptionText, setDescriptionText] = useState('');

  // Set the description text accordingly
  useEffect(() => {
    if (description.length > 500) {
      setDescriptionText(description.slice(0, 500).concat('...'));
    } else {
      setDescriptionText(description);
    }
  }, [description]);

  // Handle the show more button click
  const handleShowMore = () => {
    setShowMore(!showMore);
    if (showMore) {
      setDescriptionText(description.slice(0, 500).concat('...'));
    } else {
      setDescriptionText(description);
    }
  };

  return (
    <div>
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
