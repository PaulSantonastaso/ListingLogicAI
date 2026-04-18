import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
      fontSize: {
        "2xs": ["0.75rem", { lineHeight: "1rem" }],   // 12px
        xs:   ["0.875rem", { lineHeight: "1.25rem" }], // 14px
        sm:   ["1rem",     { lineHeight: "1.5rem" }],  // 16px
        base: ["1.125rem", { lineHeight: "1.75rem" }], // 18px
        lg:   ["1.5rem",   { lineHeight: "2rem" }],    // 24px
        xl:   ["2rem",     { lineHeight: "2.5rem" }],  // 32px
      },
      colors: {
        border:      "hsl(var(--border))",
        input:       "hsl(var(--input))",
        ring:        "hsl(var(--ring))",
        background:  "hsl(var(--background))",
        foreground:  "hsl(var(--foreground))",
        primary: {
          DEFAULT:    "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT:    "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        muted: {
          DEFAULT:    "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT:    "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        card: {
          DEFAULT:    "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",          // 8px — cards
        md: "calc(var(--radius) - 2px)", // 6px — inputs, buttons
        sm: "calc(var(--radius) - 4px)", // 4px — misc
      },
      keyframes: {
        // shadcn defaults
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        // Skeleton shimmer
        shimmer: {
          "0%":   { backgroundPosition: "200% 0" },
          "100%": { backgroundPosition: "-200% 0" },
        },
        // Generating pulse dot
        pulse: {
          "0%, 100%": { opacity: "1" },
          "50%":       { opacity: "0.3" },
        },
        // Photo zone expand
        "collapsible-down": {
          from: { height: "0", opacity: "0" },
          to:   { height: "var(--radix-collapsible-content-height)", opacity: "1" },
        },
        "collapsible-up": {
          from: { height: "var(--radix-collapsible-content-height)", opacity: "1" },
          to:   { height: "0", opacity: "0" },
        },
      },
      animation: {
        "accordion-down":   "accordion-down 0.2s ease-out",
        "accordion-up":     "accordion-up 0.2s ease-out",
        shimmer:            "shimmer 1.5s infinite linear",
        pulse:              "pulse 1s ease-in-out infinite",
        "collapsible-down": "collapsible-down 0.2s ease-out",
        "collapsible-up":   "collapsible-up 0.2s ease-out",
      },
    },
  },
  plugins: [animate],
};

export default config;
