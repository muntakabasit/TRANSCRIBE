import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        dawt: {
          background: '#F9F7F4',        // Warm off-white
          card: '#FFFFFF',              // Pure white
          accent: '#E8B44C',            // Warm gold
          text: {
            primary: '#1A1A1A',         // Near black
            secondary: '#666666',       // Medium gray
            timestamp: '#888888',       // Timestamp gray
          },
          divider: '#E0E0E0',           // Hairline divider
        }
      },
      letterSpacing: {
        wider: '0.015em',    // +1.5pt equivalent
        wide: '0.012em',     // +1.2pt equivalent
        widest: '0.02em',    // +2pt equivalent
      },
    },
  },
  plugins: [],
};
export default config;
