import { defineConfig } from "vite";

export default defineConfig({
	server: {
		host: "0.0.0.0",
	},
	build: {
		copyPublicDir: true,
		chunkSizeWarningLimit: 1500,
	},
});
