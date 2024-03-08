'use client';
import { useEffect } from 'react';

/**
 * Scroll up component.
 * @returns null
 */
export default function ScrollUp() {
  useEffect(() => {
    // Scroll to top of page when not viewing comments
    if (window.location.hash !== '#comments') {
      window.document.scrollingElement?.scrollTo(0, 0);
    }
  }, []);

  return null;
}
