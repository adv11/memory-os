import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17202a",
        paper: "#fbfcf8",
        moss: "#4b6f44",
        clay: "#a85f3d",
        marine: "#315f72",
        line: "#d9ded3",
      },
      boxShadow: {
        soft: "0 12px 32px rgba(23, 32, 42, 0.08)",
      },
    },
  },
  plugins: [],
};

export default config;

