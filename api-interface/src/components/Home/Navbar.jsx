// Navbar.js

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {Link as ScrollLink} from 'react-scroll'
import '../../tailwind.css';

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);

  const handleScroll = () => {
    const offset = window.scrollY;
    setScrolled(offset > 96);
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 p-4 flex justify-between items-center px-16 z-50 ${
        scrolled ? 'bg-gray shadow-md' : ''
      }`}
    >
      <div className="text-emerald font-bold text-3xl">TeamUp</div>

      <div className="flex text-xl space-x-16">
        <ScrollLink to="about" smooth={true} duration={500} className="text-neutral hover:text-emerald hover:cursor-pointer">
          About Us
        </ScrollLink>
        <ScrollLink to="services" smooth={true} duration={500} className="text-neutral hover:text-emerald hover:cursor-pointer">
          Services
        </ScrollLink>
        <ScrollLink to="FAQs" smooth={true} duration={500} className="text-neutral hover:text-emerald hover:cursor-pointer">
          FAQs
        </ScrollLink>
      </div>

      <Link to="/Login">
        <button
          className="rounded-full px-4 py-2 text-neutral bg-orange transition duration-300 ease-in-out hover:bg-emerald"
        >
          Get Started
        </button>
      </Link>
    </nav>
  );
};

export default Navbar;