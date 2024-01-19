// AuthForm.jsx
import React, { useState } from 'react';
import Login from './Login';
import AuthFormRight from './AuthFormRight';
import '../../tailwind.css';

const LoginPage = ({ userType, onUserTypeChange }) => {
  return (
    <section className="min-h-screen w-full flex items-center justify-center">
      <div className="container h-screen mx-auto">
        <div className="g-6 flex flex-wrap items-center h-screen justify-center text-neutral-800 dark:text-neutral-200">
          <div className="w-full">
            <div className="block bg-white shadow-lg dark:bg-neutral-800">
              <div className="g-0 lg:flex lg:flex-wrap">
                {/* Left column container */}
                <Login />

                {/* Right column container with background and description */}
                <AuthFormRight />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default LoginPage;