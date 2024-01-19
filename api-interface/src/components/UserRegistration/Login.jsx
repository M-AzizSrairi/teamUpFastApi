import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { parseJwt } from './authUtils';

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegisterClick = () => {
    // Navigate to the Register page
    navigate('/register');
  };

  const handleLoginClick = async () => {
    try {
      const response = await fetch('http://localhost:8000/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': `Basic ${btoa(`${formData.username}:${formData.password}`)}`,
        },
        body: `grant_type=password&username=${formData.username}&password=${formData.password}`,
      });

      console.log('Access Token:', localStorage.getItem('accessToken'));

      if (response.ok) {
        const data = await response.json();

        if (data.access_token) {
          // Store the received access token in localStorage
          localStorage.setItem('accessToken', data.access_token);

          // Extract user type and username from the token payload
          const tokenPayload = parseJwt(data.access_token);
          const username = tokenPayload.sub;
          console.log("data", data.access_token);
          console.log("username", username);

          if (username) {
            // Navigate to the user's profile
            navigate('/docs');
          } else {
            console.error('User type or username not found in token payload:', tokenPayload);
            setError('An unexpected error occurred. Please try again.');
          }
        } else {
          console.error('Access token not found in response:', data);
          setError('Login failed. Please try again.');
        }
      } else {
        // Handle errors from the server
        const data = await response.json();
        console.error('Login failed:', data);
        setError(data.detail || 'Login failed. Please try again.');
      }
    } catch (error) {
      console.error('Error during login:', error);
      setError('An unexpected error occurred. Please try again.');
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

        <h2 className="mb-4">Login to your account</h2>
        <input
          type="text"
          name="username"
          placeholder="Username"
          className="mt-1 p-3 bg-neutral text-gray w-full mb-3"
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          className="mt-1 p-3 bg-neutral text-gray w-full mb-3"
          onChange={handleChange}
        />
        {error && <div className="text-red-500 mb-4">{error}</div>}
        <button
          className="inline-block w-full rounded px-6 pb-2 pt-2.5 text-xs font-medium uppercase bg-gray text-neutral transition duration-300 ease-in-out hover:bg-emerald hover:text-gray"
          type="button"
          onClick={handleLoginClick}
        >
          Log in
        </button>
        <div className="flex items-center justify-center mt-2">
          <span className="text-sm">Don't have an account?</span>
          <button
            type="button"
            className="ml-2 text-orange hover:text-emerald"
            onClick={handleRegisterClick}
          >
            Register
          </button>
        </div>
        <a href="#!" className="flex items-center justify-center hover:text-orange">
          Forgot password?
        </a>
      </div>
    </div>
  );
};

export default Login;