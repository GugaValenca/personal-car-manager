import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig(() => ({
  server: {
    host: "::",
    port: 8080,
    hmr: {
      overlay: false,
    },
  },
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    // Emitted as dist/.vite/manifest.json. The Django templates read this
    // (via cars/templatetags/vite_assets.py) to resolve the hashed JS/CSS
    // filenames instead of hardcoding them, so a new `npm run build` no
    // longer requires manually editing 3 templates.
    manifest: true,
    rollupOptions: {
      input: path.resolve(__dirname, "index.html"),
    },
  },
}));
