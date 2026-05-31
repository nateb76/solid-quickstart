import solid from "solid-start/vite";
import node from "solid-start-node";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [solid({ adapter: node() })],
  server: {
    host: "0.0.0.0",
    port: Number(process.env.PORT) || 3000,
  },
});
