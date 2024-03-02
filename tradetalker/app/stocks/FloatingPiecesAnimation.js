// FloatingPiecesAnimation.js
import React from 'react';
import styles from './FloatingPiecesAnimation.module.css'; // Import CSS module for styling
import ContinuousLoopAnimation from './continuousLoopAnimation'; // Import ContinuousLoopAnimation component

const numRectangles = 10; // Number of rectangles to generate in each set
const animationDuration = 10; // Animation duration in seconds

const FloatingPiecesAnimation = () => {
    const rectangles = Array.from({ length: numRectangles }).map((_, index) => (
        <div key={`rectangle-${index}`} className={styles.rectangle}></div>
    ));

    return (
        <ContinuousLoopAnimation animationDuration={animationDuration} animationDirection="right">
            {/* Floating rectangles */}
            <div className={styles.rectangles}>{rectangles}</div>
        </ContinuousLoopAnimation>
    );
};

export default FloatingPiecesAnimation;
