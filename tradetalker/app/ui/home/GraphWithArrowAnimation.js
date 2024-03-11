'use client'
import React, { useEffect, useState } from 'react';
import * as THREE from 'three';

const GraphWithArrowAnimation = () => {
    const [position, setPosition] = useState({ x: 0, y: 50 });
    const [points, setPoints] = useState([]);

    useEffect(() => {
        const animation = setInterval(() => {
            const deltaX = Math.random() * 3;
            const deltaY = Math.random() * 5 - 2.5; // Adjust the range for more upwards movement
            setPosition(prevPosition => ({
                x: prevPosition.x + deltaX,
                y: prevPosition.y + deltaY,
            }));
            setPoints(prevPoints => [...prevPoints.slice(-50), [position.x, position.y]]);
        }, 100);

        return () => clearInterval(animation);
    }, [position]);

    return (
        <svg width="100%" height="100%" viewBox="0 0 100 100">
            <polyline
                points={points.map(point => point.join(',')).join(' ')}
                fill="none"
                stroke="blue"
                strokeWidth="0.5" // Adjust the stroke width here
            />
            <defs>
                <marker
                    id="arrowhead"
                    markerWidth="2"
                    markerHeight="1.5"
                    refX="0"
                    refY="0.75"
                    orient="auto"
                    markerUnits="strokeWidth"
                >
                    <polygon points="0 0, 2 0.75, 0 1.5" fill="red" />
                </marker>
            </defs>
            <line
                x1={position.x - 3}
                y1={position.y}
                x2={position.x}
                y2={position.y}
                stroke="black"
                strokeWidth="1" // Adjust the stroke width here
                markerEnd="url(#arrowhead)"
            />
        </svg>
    );
};


export default GraphWithArrowAnimation;
