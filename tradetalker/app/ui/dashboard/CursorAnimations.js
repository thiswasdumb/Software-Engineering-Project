'use client'
import React, { useState, useEffect, useRef } from 'react';
import './style.css'; // Import the CSS file for styling

const CursorAnimation = () => {
    const [circles, setCircles] = useState([]);
    const containerRef = useRef(null); // Reference to the container element

    useEffect(() => {
        const handleMouseMove = (event) => {
            const container = containerRef.current;
            if (!container) return;

            const containerRect = container.getBoundingClientRect();
            const mouseX = event.pageX - containerRect.left;
            const mouseY = event.pageY - containerRect.top;

            // Check if the mouse coordinates are within the container boundaries
            if (mouseX >= 0 && mouseX <= containerRect.width && mouseY >= 0 && mouseY <= containerRect.height) {
                const newCircle = {
                    id: Date.now(),
                    x: mouseX,
                    y: mouseY,
                    opacity: Math.random(),
                    speedX: Math.random() * 2 - 1, // Random speed between -1 and 1
                    speedY: Math.random() * 2 - 1, // Random speed between -1 and 1
                };
                setCircles((prevCircles) => [...prevCircles, newCircle]);
            }
        };


        document.addEventListener('mousemove', handleMouseMove);

        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    useEffect(() => {
        const animationFrame = requestAnimationFrame(animateCircles);
        return () => cancelAnimationFrame(animationFrame);
    }, [circles]);

    const animateCircles = () => {
        setCircles((prevCircles) =>
            prevCircles.map((circle) => {
                const container = containerRef.current;
                if (!container) return circle;

                const containerRect = container.getBoundingClientRect();
                let newX = circle.x + circle.speedX;
                let newY = circle.y + circle.speedY;

                // Ensure the circle stays within the container
                newX = Math.max(0, Math.min(containerRect.width, newX));
                newY = Math.max(0, Math.min(containerRect.height, newY));

                return {
                    ...circle,
                    x: newX,
                    y: newY,
                };
            })
        );
    };

    return (
        <div ref={containerRef} className="cursor-containerz">
            {circles.map((circle) => (
                <div
                    key={circle.id}
                    className="circlez"
                    style={{
                        left: circle.x + 'px',
                        top: circle.y + 'px',
                        opacity: circle.opacity,
                    }}
                />
            ))}
        </div>
    );
};

export default CursorAnimation;
