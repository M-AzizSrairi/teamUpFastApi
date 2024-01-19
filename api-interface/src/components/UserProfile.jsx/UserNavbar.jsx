// UserNavbar.jsx
import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  TbCircleLetterA,
  TbSquareLetterB,
  TbSquareLetterC,
  TbSquareLetterD,
  TbSquareLetterE,
  TbSquareLetterF,
  TbSquareLetterG,
  TbSquareLetterH,
  TbSquareLetterI,
  TbSquareLetterJ,
  TbSquareLetterK,
  TbSquareLetterL,
  TbSquareLetterM,
  TbSquareLetterN,
  TbSquareLetterO,
  TbSquareLetterP,
  TbSquareLetterQ,
  TbSquareLetterR,
  TbSquareLetterS,
  TbSquareLetterT,
  TbSquareLetterU,
  TbSquareLetterV,
  TbSquareLetterW,
  TbSquareLetterX,
  TbSquareLetterY,
  TbSquareLetterZ,
   }
   from 'react-icons/tb'; 

import { parseJwt } from '../UserRegistration/authUtils';


const UserNavbar = () => {
    const navigate = useNavigate();
    const loggedInUsername = parseJwt(localStorage.getItem('accessToken')).sub;
    const [menuOpen, setMenuOpen] = useState(false);
    const [profileMenuOpen, setProfileMenuOpen] = useState(false);
    const menuRef = useRef();
    const profileMenuRef = useRef();

    useEffect(() => {
        const handleOutsideClick = (event) => {
          if (menuRef.current && !menuRef.current.contains(event.target)) {
            setMenuOpen(false);
          }
          if (profileMenuRef.current && !profileMenuRef.current.contains(event.target)) {
            setProfileMenuOpen(false);
          }
        };
    
        document.addEventListener('click', handleOutsideClick);
    
        return () => {
          document.removeEventListener('click', handleOutsideClick);
        };
      }, []);

  const handleMenuToggle = () => {
    setMenuOpen(!menuOpen);
  };

  const handleProfileMenuToggle = () => {
    setProfileMenuOpen(!profileMenuOpen);
  };

  const getProfileIcon = (username) => {
    const firstLetter = username.charAt(0).toUpperCase();
  
    console.log("First letter:", firstLetter);
  
    switch (firstLetter) {
      case 'A':
        return <TbCircleLetterA className="h-8 w-8" />;
      case 'B':
        return <TbSquareLetterB className="h-8 w-8" />;
      case 'C':
        return <TbSquareLetterC className="h-8 w-8" />;
      case 'D':
        return <TbSquareLetterD className="h-8 w-8" />;
      case 'E':
        return <TbSquareLetterE className="h-8 w-8" />;
      case 'F':
        return <TbSquareLetterF className="h-8 w-8" />;
      case 'G':
        return <TbSquareLetterG className="h-8 w-8" />;
      case 'H':
        return <TbSquareLetterH className="h-8 w-8" />;
      case 'I':
        return <TbSquareLetterI className="h-8 w-8" />;
      case 'J':
        return <TbSquareLetterJ className="h-8 w-8" />;
      case 'K':
        return <TbSquareLetterK className="h-8 w-8" />;
      case 'L':
        return <TbSquareLetterL className="h-8 w-8" />;
      case 'M':
        return <TbSquareLetterM className="h-8 w-8" />;
      case 'N':
        return <TbSquareLetterN className="h-8 w-8" />;
      case 'O':
        return <TbSquareLetterO className="h-8 w-8" />;
      case 'P':
        return <TbSquareLetterP className="h-8 w-8" />;
      case 'Q':
        return <TbSquareLetterQ className="h-8 w-8" />;
      case 'R':
        return <TbSquareLetterR className="h-8 w-8" />;
      case 'S':
        return <TbSquareLetterS className="h-8 w-8" />;
      case 'T':
        return <TbSquareLetterT className="h-8 w-8" />;
      case 'U':
        return <TbSquareLetterU className="h-8 w-8" />;
      case 'V':
        return <TbSquareLetterV className="h-8 w-8" />;
      case 'W':
        return <TbSquareLetterW className="h-8 w-8" />;
      case 'X':
        return <TbSquareLetterX className="h-8 w-8" />;
      case 'Y':
        return <TbSquareLetterY className="h-8 w-8" />;
      case 'Z':
        return <TbSquareLetterZ className="h-8 w-8" />;
      default:
        return <TbSquareLetterJ className="h-8 w-8" />;
    }
  };
  

  
  

  const profileIcon = getProfileIcon(loggedInUsername);
  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:8000/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
      });

      if (response.ok) {
        localStorage.removeItem('accessToken');
        navigate('/');
      } else {
        console.error('Logout failed:', response);
        // Handle logout failure (optional)
      }
    } catch (error) {
      console.error('Error during logout:', error);
      // Handle logout error (optional)
    }
  };

  return (
    <nav className="bg-gray">
      <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div className="relative flex h-16 items-center justify-between">
          <div className="flex items-center">
            <div className="text-emerald font-bold text-2xl">Team Up</div>
          </div>
          <div className="flex items-center ml-4">
            <div className="relative mt-1" ref={profileMenuRef}>
              <button
                type="button"
                className="ml-4 h-8 w-8 text-neutral rounded-full hover:text-emerald focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                onClick={handleProfileMenuToggle}
              >
                {profileIcon}
              </button>
              {profileMenuOpen && (
                <div className="absolute z-10 bg-neutral text-gray mt-2 space-y-2 py-2">
                  <a href="#" className="block px-4 py-2 text-gray text-sm hover:bg-gray hover:text-neutral">
                    Your Profile
                  </a>
                  <button
                    className="block px-4 py-2 text-gray text-sm hover:bg-gray hover:text-neutral"
                    onClick={handleLogout}
                  >
                    Log Out
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default UserNavbar;