import { useRouter } from 'next/navigation';

export default async function Logout() {
  const router = useRouter();
  try {
    const response = await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include', // Include cookies in the request
    });
    if (response.ok) {
      const success = await response.json().then((data) => data.success);
      router.refresh();
      router.push(`/login?success=${success}`);
    } else {
      console.error('Logout failed');
    }
  } catch (error) {
    console.error('Error during logout:', error);
  }
}
