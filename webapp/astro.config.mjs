// @ts-check
import tailwindcss from "@tailwindcss/vite";
import { defineConfig, fontProviders } from "astro/config";

import react from "@astrojs/react";

// https://astro.build/config
export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
  },

  integrations: [react()],
  fonts: [
    {
      provider: fontProviders.fontsource(),
      name: "Anton",
      cssVariable: "--font-anton",
    },
    {
      provider: fontProviders.fontsource(),
      name: "Montserrat",
      cssVariable: "--font-montserrat",
    },
    {
      provider: fontProviders.fontsource(),
      name: "Libre Baskerville",
      cssVariable: "--font-libre-baskerville",
    }
  ]
});
