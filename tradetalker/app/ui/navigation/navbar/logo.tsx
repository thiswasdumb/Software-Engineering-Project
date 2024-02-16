'use client';

import Image from 'next/image';
import logo from '/public/images/logo.png';
import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function Logo() {
  return (
    <>
      <Link className="hover:opacity-70" href="/">
        <Image
          src={logo}
          alt="TradeTalker Logo"
          width={80}
          height={45}
          className="relative"
        />
      </Link>
    </>
  );
}