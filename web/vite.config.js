import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// In development the page is on :5173 and the API on :8000. The proxy sends /api to the API,
// so the browser sees one origin and no CORS setup is needed. It is used only when VITE_API_URL is empty.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const target = env.VITE_DEV_API ?? "http://127.0.0.1:8000";
  return {
    plugins: [react()],
    server: { proxy: { "/api": { target, changeOrigin: true } } },
    preview: { proxy: { "/api": { target, changeOrigin: true } } },
  };
});
