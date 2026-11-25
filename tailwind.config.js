/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        campus: {
          bg: '#080d19',
          surface: '#0f172a',
          surfaceElevated: '#1e293b',
          border: '#334155',
          primary: '#06b6d4',      // cyan
          primaryGlow: '#0891b2',
          accent: '#38bdf8',       // light cyan/sky
          emerald: '#10b981',      // sports/turf
          amber: '#f59e0b',        // poi/landmark
          rose: '#f43f5e',         // warning/exit
          muted: '#94a3b8'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        'glow-cyan': '0 0 20px -3px rgba(6, 182, 212, 0.45)',
        'glow-emerald': '0 0 20px -3px rgba(16, 185, 129, 0.4)',
        'card-dark': '0 10px 25px -5px rgba(0, 0, 0, 0.6), 0 8px 10px -6px rgba(0, 0, 0, 0.6)',
      }
    },
  },
  plugins: [],
}
