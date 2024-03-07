import React from 'react';
import { Metadata } from 'next';
import ResetPasswordForm from 'app/ui/reset-password';

export const metadata: Metadata = {
  title: 'Reset Password',
};

export default function ResetPassword({
  params,
}: {
  params: { token: string };
}) {
  return <ResetPasswordForm token={params.token} />;
}
