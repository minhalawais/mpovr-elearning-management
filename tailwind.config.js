/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        benzin: ['Benzin', 'sans-serif'],
        roboto: ['Roboto', 'sans-serif'],
        // Add this line
        benzinTtf: 'local("Benzin"), url("../fonts/Benzin-Bold.ttf") format("truetype")',
      }
    }
  },
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}