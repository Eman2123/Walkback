// 16-bit Mars theme. Colours are named for what they are, not where they are used.
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0d0814", // outlines and hard shadows
        night: "#1b1226", // page background
        panel: "#2e2140", // raised boxes
        panel2: "#3a2a52", // boxes inside boxes
        edge: "#5b4580", // light edge of a box
        cream: "#f5e6c8", // main text
        mute: "#b7a6c9", // secondary text
        mars: "#ff7b3a", // primary accent
        rust: "#a63a22", // pressed / shadow of the accent
        aqua: "#4cc9f0", // deterministic, derived
        neon: "#5eea8a", // calibrated, measured
        sun: "#ffd23f", // truth, focus
        blush: "#ff5d8f", // assumed, failure
      },
      fontFamily: {
        pixel: ['"Press Start 2P"', "monospace"],
        body: ["VT323", "ui-monospace", "monospace"],
      },
      // VT323 is small for its size, so the scale is larger than Tailwind's default.
      fontSize: {
        xs: ["16px", "1.2"],
        sm: ["18px", "1.25"],
        base: ["20px", "1.3"],
        lg: ["24px", "1.2"],
        xl: ["28px", "1.15"],
        "2xl": ["36px", "1.1"],
      },
    },
  },
  plugins: [],
};
