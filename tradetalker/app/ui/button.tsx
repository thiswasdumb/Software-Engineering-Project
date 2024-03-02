import React, { ButtonHTMLAttributes, ReactNode } from 'react';
import clsx from 'clsx';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
}

export function Button({ children, className, ...rest }: ButtonProps) {
  return (
    <button
      {...rest}
      className={clsx(
        'bg-blue-500 text-white hover:bg-blue-400 focus-visible:outline-blue-500 active:bg-blue-600 flex h-10 items-center rounded-lg px-4 text-sm font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 aria-disabled:cursor-not-allowed aria-disabled:opacity-50',
        className
      )}
    >
      {children}
    </button>
  );
}
