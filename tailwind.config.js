/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
      "./**/*.{html, js}",
      "./node_modules/flowbite/**/*.js",
      "!./static/alpinejs/*", // Exclude all alpine.js files
      "./node_modules/*",
      "./node_modules/alpinejs/**/*.js",
    ],
    safelist: [
      'access-page',
      'password-reset-page',
      'main-app',
    ],
  theme: {
    extend: {
      colors: {
        // 'black-700': '#202328',
      },
      screens: {
        'portrait': {'raw': '(max-width: 375px) and (orientation: portrait)'},
        'landscape': {'raw': '(max-width: 375px) and (orientation: landscape)'},
      },
      boxShadow: {
        'medium': '0 3px 3px 0 rgb(0 0 0 / 0.3), 0 3px 2px -1px rgb(0 0 0 / 0.3)',
      }
    },
  },
  plugins: [
    function({ addUtilities }) {
      const newUtilities = {
        ".scroll-container": {
          position: "relative",
        },
        ".scroll-shadow": {
          content: '""',
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 0,
          width: "100%",
          height: "20px",
          background: "linear-gradient(180deg, rgba(255, 255, 255, 0) 0%, #fefefe 100%)",
        }
      };
      addUtilities(newUtilities);
    },
  ],
}
