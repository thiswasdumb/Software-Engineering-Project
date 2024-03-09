import React from 'react';
import { Metadata } from 'next';
import ForgotPasswordComponent from '../ui/forgot-password';

export const metadata: Metadata = {
  title: 'Forgot Password',
};

/**
 * Forgot password page.
 * @returns JSX.Element - Forgot password page component
 */
export default function ForgotPassword() {
  return <ForgotPasswordComponent />;
}
