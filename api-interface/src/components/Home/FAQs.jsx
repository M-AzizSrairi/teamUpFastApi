import React, { useState } from 'react';
import { IoIosArrowDown } from 'react-icons/io';

const FAQItem = ({ question, answer, isOpen, toggle }) => {
  return (
    <div className='mb-4 border-b pb-4'>
      <div className='flex items-center justify-between cursor-pointer' onClick={toggle}>
        <div className='text-justify md:text-l lg:text-xl xl:text-2xl'>{question}</div>
        {isOpen ? (
          <IoIosArrowDown className='transform rotate-180 text-lg md:text-xl lg:text-2xl xl:text-3xl' />
        ) : (
          <IoIosArrowDown className='transform rotate-0 text-lg md:text-xl lg:text-2xl xl:text-3xl' />
        )}
      </div>
      {isOpen && <div className='mt-2 text-justify text-gray-600 text-sm md:text-base lg:text-lg xl:text-xl'>{answer}</div>}
    </div>
  );
};

const FAQs = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isOpen, setIsOpen] = useState(Array(5).fill(false)); 

  const toggleFAQ = (index) => {
    const newOpenState = [...isOpen];
    newOpenState[index] = !newOpenState[index];
    setIsOpen(newOpenState);
  };

  return (
    <div id='FAQs' className='bg-gray text-neutral py-8'>
      <div className='max-w-full md:max-w-2xl mx-auto px-4'>
        <h2 className='text-3xl lg:text-4xl xl:text-5xl font-bold text-center mb-8'>
          Our Most Asked Questions
        </h2>
        <div className='mb-8'>
          <input
            type='text'
            placeholder='Didn’t find an answer? Ask us!'
            className='w-full px-4 py-2 rounded-full bg-gray-900 text-gray focus:outline-none'
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <FAQItem
          question='How do I authenticate requests to the Team Up API?'
          answer='To authenticate requests, include the generated access token in the Authorization header of your API calls. You can obtain the access token by logging in through the /login endpoint and using the provided token for subsequent requests. Ensure the token is prefixed with "Bearer"'
          isOpen={isOpen[0]}
          toggle={() => toggleFAQ(0)}
        />
        <FAQItem
          question='What data formats does the Team Up API support?'
          answer='The Team Up API primarily uses JSON for both request and response data. Make sure your requests include the appropriate Content-Type header (application/json). Responses from the API are also in JSON format, providing structured and easily parsable data.'
          isOpen={isOpen[1]}
          toggle={() => toggleFAQ(1)}
        />
        <FAQItem
          question='Can I test the API before integrating it?'
          answer='Certainly! We encourage developers to explore and test the API. Utilize tools like Postman or Swagger UI for easy testing. Additionally, refer to our API documentation at /docs for a detailed overview of available endpoints, request parameters, and expected responses.'
          isOpen={isOpen[2]}
          toggle={() => toggleFAQ(2)}
        />
        <FAQItem
          question='How does the Team Matching feature work?'
          answer='The Team Matching feature allows you to create and manage teams, invite players, and facilitate team-joining processes. Refer to the related endpoints in the documentation for details on creating teams, handling invitations, and joining teams. These endpoints empower you to seamlessly manage sports teams through the API.'
          isOpen={isOpen[3]}
          toggle={() => toggleFAQ(3)}
        />
        <FAQItem
          question='What kind of weather data can I access?'
          answer='The Weather Forecast endpoints provide a 5-day forecast with a 3-hour step, delivering data on temperature, "feels like" conditions, maximum and minimum temperatures, humidity levels, and sea levels. Developers can leverage this detailed weather information to enhance the planning and execution of sports activities based on atmospheric conditions.'
          isOpen={isOpen[4]}
          toggle={() => toggleFAQ(4)}
        />
      </div>
    </div>
  );
};

export default FAQs;