'use client'
import React, { useEffect, useState } from 'react';
import './style.css';

const SlidingRoundedRectangles = ({ count = 14, gap = 2 }) => {
    const [isVisible, setIsVisible] = useState([]);

    useEffect(() => {
        const timerIds = [];
        for (let i = count - 1; i >= 0; i--) {
            timerIds.push(setTimeout(() => setIsVisible(prev => [...prev, i]), (count - i - 1) * 300));
        }

        return () => {
            timerIds.forEach(id => clearTimeout(id));
        };
    }, [count]);

    const getRandomDarkness = () => Math.random() * 0.3 + 0.8; // Random darkness between 0.8 and 0.9

    return (
        <div className="sliding-rectangles">
            {Array.from({ length: count }).map((_, index) => {
                const darkness = getRandomDarkness();
                const backgroundColor = `rgba(93, 92, 181, ${darkness})`; // Adjust the color as needed
                return (
                    <div
                        key={index}
                        className={`rounded-rectangle ${isVisible.includes(index) ? 'visible' : ''}`}
                        style={{
                            marginLeft: index === 0 ? 0 : gap + 'vw',
                            backgroundColor: backgroundColor
                        }}
                    />
                );
            })}
        </div>
    );
};

export default SlidingRoundedRectangles;
