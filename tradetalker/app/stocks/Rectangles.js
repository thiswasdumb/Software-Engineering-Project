import React from 'react';
import GrowingRectangle from './GrowingRectangle';

const generateRandomHeight = () => {
    return Math.floor(Math.random() * (400 - 100) + 100); // Generate a random height between 100 and 400
};

const Rectangles = () => {
    const numRectangles = 13; // Number of rectangles

    return (
        <div className="flex">
            {Array.from({ length: numRectangles }, (_, index) => (
                <div key={index} style={{ width: '100px', marginRight: '10px' }}>
                    <GrowingRectangle width={100} finalHeight={generateRandomHeight()} duration={100} />
                </div>
            ))}
        </div>
    );
};

export default Rectangles;
