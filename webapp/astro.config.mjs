// @ts-check
import tailwindcss from "@tailwindcss/vite";
import { defineConfig, fontProviders } from "astro/config";

import react from "@astrojs/react";

// https://astro.build/config
export default defineConfig({
  site: "https://la-france-a-la-loupe.fr",

  vite: {
    plugins: [tailwindcss()],
  },

  integrations: [react()],

  fonts: [
    {
      provider: fontProviders.fontsource(),
      name: "Anton",
      cssVariable: "--font-family-anton",
      weights: [400],
    },
    {
      provider: fontProviders.fontsource(),
      name: "Montserrat",
      cssVariable: "--font-family-montserrat",
      weights: [300, 400, 600, 700],
    },
    {
      provider: fontProviders.fontsource(),
      name: "Libre Baskerville",
      cssVariable: "--font-family-libre-baskerville",
      weights: [400, 600, 700],
    },
  ],
});
