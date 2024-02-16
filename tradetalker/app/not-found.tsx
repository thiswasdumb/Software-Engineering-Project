import Link from "next/link";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Not Found",
};

export default function NotFound() {
  return (
    <div className="">
      <Link href="/page-not-found">Not Found</Link>
      <p>Could not find requested resource.</p>
      <Link href="/">Return Home</Link>
    </div>
  );
}