// AboutUs.js

import React from 'react';
import '../../tailwind.css';

const AboutUs = () => {
  return (
    <div id='about' className="max-w-full px-4 pt-8 bg-gray text-neutral">
      {/* Centered Text Section */}
      <div className="text-center mx-12  mb-8 ">
        <h1 className="text-4xl font-bold mb-4">Your Premier Sports Solutions Provider</h1>
        <p className="text-lg mt-8 text-justify leading-relaxed">
        At Team Up API, we take pride in delivering cutting-edge backend services designed to address a myriad of challenges within the sports community, with a particular focus on enhancing the experiences of football enthusiasts. Our commitment lies in creating a seamless and robust platform that caters to the unique needs of sports aficionados, providing tailored solutions to make the football community happier. From facilitating effortless football pitch rentals to optimizing team matching processes and offering</p>
        <span className="text-lg text-center">
        accurate weather forecasts, our comprehensive suite of services is meticulously crafted to elevate your sports-related endeavors.
        </span>
      </div>

      {/* Scrolling Background with Simple Scroll Effect */}
      <div
        className='rounded-2xl relative flex items-center justify-center mx-16 h-96 bg-fixed bg-parallax2 bg-cover rounded'
      >
        <div className=" rounded-2xl w-full h-full absolute top-0 left-0 bg-black opacity-80 z-20"></div>
      </div>
    </div>
  );
};

export default AboutUs;