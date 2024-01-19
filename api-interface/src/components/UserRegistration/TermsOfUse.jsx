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
        <div className="mb-4 h-40 overflow-y-auto">
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla facilisi. Proin vel orci non
            nisl tincidunt porta. Ut ut interdum mi, at rhoncus lorem. Pellentesque sed nunc at leo
            consectetur tristique. Fusce pharetra sagittis odio, vel venenatis risus cursus non.
            Vestibulum ut nisi eget felis efficitur rhoncus. Sed non urna vel purus hendrerit accumsan.
            Suspendisse sed urna nec nunc consectetur euismod. Nullam et lectus at tortor malesuada
            faucibus ac eu erat. Aliquam erat volutpat. Vestibulum vel metus nec quam varius
            scelerisque. Ut et elit non lectus commodo varius nec vel metus. Vivamus et neque id libero
            bibendum hendrerit. Phasellus vel efficitur dolor. Nullam ullamcorper posuere urna, eu
            consectetur purus vehicula id.
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
