import React from 'react';
import './style.css'; // Import the CSS file for styling

const CursorAnimation = () => {
    const numLines = 10; // Number of lines
    const circlesPerLine = 26; // Number of circles per line
    const circleSize = 50; // Size of each circle
    const horizontalSpacing = 160; // Increased horizontal spacing between circles
    const verticalSpacing = 0; // Decreased vertical spacing between lines

    return (
        <div className="cursor-container">
            {[...Array(numLines)].map((_, lineIndex) => (
                <div key={lineIndex} className="line">
                    {[...Array(circlesPerLine)].map((_, circleIndex) => {
                        const brightness = Math.random() * 0.2 + 0.6; // Random brightness between 0.3 and 0.6
                        return (
                            <div
                                key={circleIndex}
                                className="circle"
                                style={{
                                    left: `${circleIndex * (circleSize + horizontalSpacing)}px`,
                                    top: `${lineIndex * (circleSize + verticalSpacing)}px`,
                                    backgroundColor: `rgba(36, 35, 99, ${brightness})`,
                                }}
                            />
                        );
                    })}
                </div>
            ))}
        </div>
    );
};

export default CursorAnimation;
