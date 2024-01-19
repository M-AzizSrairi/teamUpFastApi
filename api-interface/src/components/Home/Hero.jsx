// Hero.js

import React from 'react';
import heroVid from '../../assets/heroVid.mp4';

const Hero = () => {
  return (
    <div className="relative h-[42rem] text-neutral text-3xl">
      {/* Black overlay */}
      <div className="w-full h-full absolute top-0 left-0 bg-black opacity-70 z-20"></div>

      {/* Video with dark filter */}
      <video
        className="object-cover w-full h-full absolute -z-10"
        src={heroVid}
        autoPlay
        loop
        muted
      />

      {/* Text and content */}
      <div className="w-full h-[90%] flex flex-col justify-center items-center text-neutral px-4 text-center text-4xl relative z-40">
        <h1>Team Up</h1>
        <h1 className="py-2">
          <span className="blue">and Find</span> the Best Venue
        </h1>
        <h1 className="text-xl py-4 text-neutral-dark">
          We Bring People Together and Venues Closer
        </h1>
      </div>
    </div>
  );
};

export default Hero;