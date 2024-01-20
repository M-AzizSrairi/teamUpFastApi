import React, { useState } from 'react';

const TermsOfUse = ({ onAccept }) => {
  const [accepted, setAccepted] = useState(false);

  const handleAccept = () => {
    setAccepted(true);
    onAccept();
  };

  return (
    <div className="fixed top-0 left-0 right-0 bottom-0 flex items-center justify-center bg-gray bg-opacity-75 z-50">
      <div className="bg-neutral p-8 max-w-md rounded shadow-md">
        <h2 className="text-2xl font-bold mb-4">Terms of Use</h2>
        <div className="mb-4 h-40 overflow-y-auto text-justify">
        <p>
        Welcome to Team Up! These terms of use outline the rules and regulations for the use of our website. By accessing this website, we assume you accept these terms and conditions. Do not continue to use Team Up if you do not agree to take all of the terms and conditions stated on this page.
      </p>
      <p>
        The following terminology applies to these Terms and Conditions, Privacy Statement, and Disclaimer Notice and all Agreements: "Client," "You," and "Your" refers to you, the person log in this website and compliant to the Company’s terms and conditions. "The Company," "Ourselves," "We," "Our," and "Us," refers to our Company. "Party," "Parties," or "Us," refers to both the Client and ourselves. All terms refer to the offer, acceptance, and consideration of payment necessary to undertake the process of our assistance to the Client in the most appropriate manner for the express purpose of meeting the Client’s needs in respect of provision of the Company’s stated services, in accordance with and subject to, prevailing law of Tunisia.
      </p>
      <p>
        <b>Cookies:</b> We employ the use of cookies. By accessing Team Up, you agreed to use cookies in agreement with Team Up's Privacy Policy.
      </p>
        </div>
        <div className="flex items-center">
          <input type="checkbox" className="mr-2" checked={accepted} onChange={() => setAccepted(!accepted)} />
          <label htmlFor="accept">I accept the terms of use</label>
        </div>
        <button
          className="mt-4 bg-emerald text-white px-4 py-2 rounded hover:bg-orange transition duration-300 ease-in-out"
          onClick={handleAccept}
          disabled={!accepted}
        >
          Continue
        </button>
      </div>
    </div>
  );
};

export default TermsOfUse;
