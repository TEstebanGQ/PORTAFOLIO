import { defineConfig } from "vite";

export default defineConfig({
	plugins: [],
	server: {
		host: "0.0.0.0",
	},
	build: {
		copyPublicDir: true,
		chunkSizeWarningLimit: 1500,
	},
});
