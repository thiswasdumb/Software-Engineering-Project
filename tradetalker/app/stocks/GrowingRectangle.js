'use client'
import React, { useState, useEffect } from 'react';
import './style.css'; // Import the CSS file for styling


const GrowingRectangle = ({ width, finalHeight, duration }) => {
    const [height, setHeight] = useState(0);
    const [color, setColor] = useState(getRandomColor());

    useEffect(() => {
        const interval = setInterval(() => {
            if (height < finalHeight) {
                setHeight((prevHeight) => Math.min(prevHeight + 1, finalHeight));
            } else {
                clearInterval(interval);
            }
        }, duration / finalHeight);

        return () => clearInterval(interval);
    }, [height, finalHeight, duration]);

    // Function to generate a random color
    function getRandomColor() {
        const baseColor = [76, 75, 155];
        const variation = 5; // Adjust this value to control the amount of variation

        // Generate random variations for each RGB component
        const randomVariations = baseColor.map(component => component + Math.floor(Math.random() * variation) * (Math.random() < 0.5 ? -1 : 1));

        // Ensure the color components are within the valid range (0-255)
        const correctedComponents = randomVariations.map(component => Math.max(0, Math.min(255, component)));

        return `rgb(${correctedComponents.join(', ')})`;
    }


    return <div className="growing-rectangle" style={{ width, height, backgroundColor: color }} />;
};

export default GrowingRectangle;



