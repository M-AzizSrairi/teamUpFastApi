import React from 'react';
import '../../tailwind.css';

const AboutCard = (props) => {
  return (
    <div className='flex flex-col items-center bg-gray-900 border border-neutral-200 text-left rounded-2xl py-12 px-8'>
      <div className='bg-emerald flex items-center justify-center p-2 rounded-full mb-4'>
        {props.icon}
      </div>
      <h3 className='text-xl font-bold mb-4'>{props.heading}</h3>
      <p className='text-justify leading-relaxed'>{props.text}</p>
    </div>
  );
};

export default AboutCard;