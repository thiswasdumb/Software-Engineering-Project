import { Metadata } from 'next';
import HomeComponent from './ui/homepage';

export const metadata: Metadata = {
  title: 'Welcome!',
};

export default function Home() {
  return (
    <div>
      <HomeComponent />
    </div>
  );
}
