import React from 'react';
import { AiOutlineRise } from "react-icons/ai";
import { MdConnectWithoutContact } from "react-icons/md";
import { FaArrowsDownToPeople } from "react-icons/fa6";
import { TiWeatherPartlySunny } from "react-icons/ti";

import AboutCard from './AboutCard';
import '../../tailwind.css';

const About = () => {
  return (
    <div id='services' className='w-full py-8 bg-gray text-neutral text-center'>
      <div className='max-w-[1240px] mx-auto mb-8 px-4 pt-8 '>
        <div>
          <h1 className='text-4xl font-bold mb-4'>Services, We Provide You With</h1>
          <p className='py-4 text-xl mb-4'>
            Team Up API focuses on providing three major functionalities spanning Football pitches renting, Teams Making, and Weather Forecast to ensure a comprehensive experience for both venue owners and sports enthusiasts
          </p>

          {/* Card Container */}
          <div className='grid sm:grid-cols-3 lg:grid-cols-3 gap-12'>

            {/* Card */}
            <AboutCard icon={<MdConnectWithoutContact size={40} />} heading='People-Venues Bridge' text='Specifically cater to the sports enthusiasts and event organizers seeking football pitch rentals. This feature simplifies the process of finding and booking football pitches for various events, including matches, tournaments, or friendly games. Users can explore a diverse range of available football venues, view detailed information, check availability, and secure bookings seamlessly. ' />
            <AboutCard icon={<FaArrowsDownToPeople size={40} />} heading='Teams Matching' text='Redefine the dynamics of team creation and player collaboration within the sports community. Seamlessly blending innovation with functionality, our endpoints empower users to effortlessly form and manage teams, extending invitations to fellow players and streamlining the process of joining teams' />
            <AboutCard icon={<TiWeatherPartlySunny size={40} />} heading='Weather Forecast' text=' Offer a comprehensive 5-day ahead glimpse into the atmospheric conditions that can influence your sports activities. With a granular 3-hour step, our endpoints provide a wealth of meteorological insights, including temperature variations, "feels like" conditions, maximum and minimum temperatures, humidity levels, and even sea levels.' />
          </div>
        </div>
      </div>
      <div
        className='my-16 rounded-2xl relative flex items-center justify-center mx-16 h-96 bg-fixed bg-parallax bg-cover rounded'
      >
        <div className=" rounded-2xl w-full h-full absolute top-0 left-0 bg-black opacity-80 z-20"></div>
      </div>
    </div>
  );
};

export default About;