import { defineConfig } from "vite";

export default defineConfig({
	server: {
		host: "0.0.0.0",
	},
	build: {
		// Omite la copia de videos pesados en dist; se sirven desde public/ en dev
		// y en producción se copian manualmente o se usan desde CDN
		copyPublicDir: true,
		rollupOptions: {
			output: {
				chunkSizeWarningLimit: 1000,
			},
		},
	},
});
