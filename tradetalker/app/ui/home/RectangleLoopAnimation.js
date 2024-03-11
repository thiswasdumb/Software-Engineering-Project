'use client'
import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

const RectangleLoopAnimation = () => {
    const canvasRef = useRef();

    useEffect(() => {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ canvas: canvasRef.current, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setClearColor(0x000000, 0); // Set the background color to transparent

        const rectangles = [];
        const numRectangles = 30;
        const rectangleSpacing = 1.1;
        const rectangleWidth = 1;
        const rectangleHeight = 0.5;
        const cornerRadius = 0.3; // Adjusted corner radius

        for (let i = 0; i < numRectangles; i++) {
            const shape = new THREE.Shape();
            shape.moveTo(-rectangleWidth / 2 + cornerRadius, -rectangleHeight / 2);
            shape.lineTo(rectangleWidth / 2 - cornerRadius, -rectangleHeight / 2);
            shape.quadraticCurveTo(rectangleWidth / 2, -rectangleHeight / 2, rectangleWidth / 2, -rectangleHeight / 2 + cornerRadius);
            shape.lineTo(rectangleWidth / 2, rectangleHeight / 2 - cornerRadius);
            shape.quadraticCurveTo(rectangleWidth / 2, rectangleHeight / 2, rectangleWidth / 2 - cornerRadius, rectangleHeight / 2);
            shape.lineTo(-rectangleWidth / 2 + cornerRadius, rectangleHeight / 2);
            shape.quadraticCurveTo(-rectangleWidth / 2, rectangleHeight / 2, -rectangleWidth / 2, rectangleHeight / 2 - cornerRadius);
            shape.lineTo(-rectangleWidth / 2, -rectangleHeight / 2 + cornerRadius);
            shape.quadraticCurveTo(-rectangleWidth / 2, -rectangleHeight / 2, -rectangleWidth / 2 + cornerRadius, -rectangleHeight / 2);

            const geometry = new THREE.ShapeGeometry(shape);
            const color = new THREE.Color('#4C4B9B');
            const brightness = 0.08 * Math.random() - 0.06; // Adjust brightness by a random amount
            color.addScalar(brightness);
            const material = new THREE.MeshBasicMaterial({ color, transparent: true });
            const rectangle = new THREE.Mesh(geometry, material);
            rectangle.position.x = i * rectangleSpacing;
            scene.add(rectangle);
            rectangles.push(rectangle);
        }

        camera.position.z = 5;

        const animate = () => {
            requestAnimationFrame(animate);

            rectangles.forEach(rectangle => {
                rectangle.position.x -= 0.02;
                if (rectangle.position.x < -numRectangles * rectangleSpacing / 2) {
                    rectangle.position.x = (numRectangles - 1) * rectangleSpacing / 2;
                }
            });

            renderer.render(scene, camera);
        };

        animate();

        const handleResize = () => {
            const width = window.innerWidth;
            const height = window.innerHeight;
            renderer.setSize(width, height);
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
        };

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
            renderer.dispose();
        };
    }, []);

    return <canvas ref={canvasRef} />;
};

export default RectangleLoopAnimation;