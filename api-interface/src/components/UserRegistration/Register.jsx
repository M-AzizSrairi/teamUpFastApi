import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TermsOfUse from './TermsOfUse';

const Register = () => {
  const navigate = useNavigate();
  const [showTerms, setShowTerms] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirm_password: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSelectChange = (e) => {
    setFormData({ ...formData, user_type: e.target.value });
  };

  const handleLoginClick = () => {
    // Navigate to the Login page
    navigate('/login');
  };

  const handleRegisterClick = () => {
    // Show the Terms of Use pop-up
    setShowTerms(true);
  };

  const handleTermsAccept = async () => {
    // Close the Terms of Use pop-up
    setShowTerms(false);

    try {
      // Perform the registration logic here
      const response = await fetch('http://localhost:8000/registerApiUser', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          username: formData.username,
          password: formData.password,
          confirm_password : formData.confirm_password,
        }),
      });

      if (response.ok) {
        // Registration successful
        console.log('User registered successfully');
        navigate('/login');
      } else {
        // Handle errors from the server
        const data = await response.json();
        console.error('Registration failed:', data);

        // Show an alert to the user with the error message
        alert(data.detail || 'Registration failed. Please try again.');
      }
    } catch (error) {
      console.error('Error during registration:', error.message);

      alert('An unexpected error occurred. Please try again.');
    }
  };
  

  return (
    <div className="flex items-center justify-center px-4 lg:w-6/12">
      <div className="mx-16">
        <div className="text-center pt-8">
          <div className="text-emerald font-bold text-3xl">Team Up</div>
          <h4 className="mb-8 text-xl font-semibold">
            We Bring People Together and Venues Closer
          </h4>
        </div>

        <h2 className="mb-4">Create a new account</h2>
        <input
          type="email"
          name="email"
          placeholder="Email"
          className="p-3 bg-neutral text-gray w-full mb-3"
          onChange={handleChange}
        />
        <input
          type="text"
          name="username"
          placeholder="User Name"
          className="p-3 bg-neutral text-gray w-full mb-3"
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          className="p-3 bg-neutral text-gray w-full mb-3"
          onChange={handleChange}
        />
        <input
          type="password"
          name="confirm_password"
          placeholder="Confirm Password"
          className="p-3 bg-neutral text-gray w-full mb-3"
          onChange={handleChange}
        />
        <button
          className="inline-block w-full rounded mt-3 px-6 pb-2 pt-2.5 text-xs font-medium uppercase bg-gray text-neutral transition duration-300 ease-in-out hover:bg-emerald hover:text-gray"
          type="button"
          onClick={handleRegisterClick}
        >
          Register
        </button>
        <div className="flex items-center justify-center mt-2">
          <span className="text-sm">Already have an account?</span>
          <button
            type="button"
            className="ml-2 text-orange hover:text-emerald"
            onClick={handleLoginClick}
          >
            Login
          </button>
        </div>
      </div>
      {showTerms && <TermsOfUse onAccept={handleTermsAccept} />}
    </div>
  );
};

export default Register;