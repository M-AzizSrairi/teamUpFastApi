import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Home/Navbar";
import Hero from './components/Home/Hero';
import About from './components/Home/About';
import AboutUs from './components/Home/AboutUs';
import FAQs from './components/Home/FAQs';
import Footer from './components/Home/Footer';
import LoginPage from './components/UserRegistration/LoginPage';
import RegisterPage from './components/UserRegistration/RegisterPage';
import Documentation from './components/UserProfile.jsx/Documentation';


function App() {
  return (
    
    <div className="App">
      <Router>
        <Routes>
          <Route 
            path="/"
            element = {
              <div className='Home'>
                <Navbar/>
                <Hero />
                <AboutUs />
                <About />
                <FAQs />
                <Footer />
              </div>
            }
          />

        {/* User authentication route */}
        <Route
          path="/login"
          element={
            <div className="UserAuth">
              <LoginPage />
            </div>
          }
        />

        {/* User registration route*/}
        <Route
          path="/register"
          element={
            <div className="UserReg">
              <RegisterPage />
            </div>
          }
        />

        {/* User Profile Route */}
        <Route
          path="/docs"
          element={
            <div className="userProfile">
              <Documentation />
            </div>
          }
        />

        </Routes>
      </Router>
    </div>
  );
}

export default App;
