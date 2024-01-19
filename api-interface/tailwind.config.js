/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
    './public/index.html',
  ],
  theme: {
    extend: {},
    colors: {
      'blue': '#082f49',    /* Royal Blue */
      'emerald': '#10b981',        /* Emerald Green*/
      'orange': '#d97706',       /* Orange-Red */
      'neutral': '#d4d4d4',      /* Neutral */
      'gray' : '#111827',
      'black' : '#0c0a09',
    },
    backgroundImage : {
           'parallax' : 'url("./assets/team.jpg")',
           'parallax2' : 'url("./assets/pitch.jpg")',
    }
  },
  plugins: [],
};