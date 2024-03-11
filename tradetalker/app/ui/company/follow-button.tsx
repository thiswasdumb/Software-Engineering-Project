'use client';
import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { usePathname } from 'next/navigation';
import { Poppins } from 'next/font/google';

const pop400 = Poppins({ weight: ['400'], subsets: ['latin'] });


/**
 * Follow button component.
 * @param companyId - Company ID
 * @param isLoggedIn - Flag to check if the user is logged in
 * @returns JSX.Element - Follow button component
 */
export default function FollowButton({
  companyId,
  isLoggedIn,
}: {
  companyId: string;
  isLoggedIn: boolean;
}) {
  const [isFollowing, setIsFollowing] = useState(false);
  const pathname = usePathname();

  // Set the following state accordingly on page load
  useEffect(() => {
    if (isLoggedIn) {
      const fetchFollowStatus = async () => {
        try {
          const response = await fetch(
            `/api/get_company_follow_status/${companyId}`
          );
          const data = await response.json();
          setIsFollowing(data.follow_status);
        } catch (error) {
          console.error('Error fetching follow status:', error);
        }
      };
      fetchFollowStatus();
    }
  }, [isLoggedIn, companyId]);

  // Handle the follow button click
  const handleFollowClick = async () => {
    if (!isFollowing) {
      try {
        const response = await fetch(`/api/follow_company/${companyId}`, {
          credentials: 'include',
        });
        const data = await response.json();
        if (data.success) {
          setIsFollowing(!isFollowing);
          if (pathname === '/dashboard') {
            window.location.reload();
          } else {
            toast.success('Followed company.');
          }
        }
      } catch (error) {
        console.error('Error toggling follow status:', error);
      }
    } else {
      try {
        const response = await fetch(`/api/unfollow_company/${companyId}`, {
          credentials: 'include',
        });
        const data = await response.json();
        if (data.success) {
          setIsFollowing(!isFollowing);
          if (pathname === '/dashboard') {
            window.location.reload();
          } else {
            toast.success('Unfollowed company.');
          }
        }
      } catch (error) {
        console.error('Error toggling follow status:', error);
      }
    }
  };

  return (
    isLoggedIn && (
      <button
        type='button'
        onClick={handleFollowClick}
        className={`rounded-lg px-4 py-2 ${isFollowing
          ? 'border-2 text-slate-500 transition hover:bg-slate-300 hover:bg-opacity-40'
          : 'border-2 bg-blue-500 text-white transition hover:border-[#434191] hover:bg-blue-600'
          }`}
        style={{
          backgroundColor: isFollowing ? '#4c4b9b' : '#6261ba',
          borderColor: isFollowing ? '#4c4b9b' : '#blue-500',
        }}
      > <span className={pop400.className}>
          {isFollowing ? 'Unfollow' : 'Follow'}
        </span>
      </button>
    )
  );
}
