// continuousLoopAnimation.js
'use client'
import React, { useRef, useEffect } from 'react';

const ContinuousLoopAnimation = ({ children, animationDuration, animationDirection }) => {
    const wrapperRef = useRef(null);

    useEffect(() => {
        const wrapper = wrapperRef.current;

        const handleAnimationEnd = () => {
            wrapper.style.transform = `translateX(${animationDirection === 'left' ? '0%' : '-100%'})`;
            wrapper.style.transition = 'none';
            void wrapper.offsetWidth; // Trigger reflow
            wrapper.style.transition = `transform ${animationDuration}s linear`;
            wrapper.style.transform = `translateX(${animationDirection === 'left' ? '-100%' : '0%'})`;
        };

        const animationInterval = setInterval(handleAnimationEnd, animationDuration * 1000);

        return () => clearInterval(animationInterval);
    }, [animationDuration, animationDirection]);

    return <div ref={wrapperRef} style={{ display: 'inline-block' }}>{children}</div>;
};

export default ContinuousLoopAnimation;