import React from 'react';
import { Metadata } from 'next';
import ResetPasswordForm from 'app/ui/reset-password';

export const metadata: Metadata = {
  title: 'Reset Password',
};

/**
 * Reset password page.
 * @param {string} token - Reset password token from the URL
 * @returns JSX.Element - Reset password page component
 */
export default function ResetPassword({ params }: {
  params: { token: string };
}) {
  return <ResetPasswordForm token={params.token} />;
}
