/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#006d77',
        secondary: '#83c5be',
        background: '#ffffff',
        foreground: '#333333',
        'muted-foreground': '#666666',
      },
    },
  },
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}