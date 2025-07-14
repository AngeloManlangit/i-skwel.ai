// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./index.html",
      // This line tells Tailwind to scan all .vue, .js, .ts, .jsx, .tsx files in src/ and its subdirectories
      "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {},
    },
    plugins: [],
  }