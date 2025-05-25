import { defineConfig } from 'vite';
import path, { dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  resolve: {
    alias: {
      app: path.resolve(__dirname, './src/app'),
      entities: path.resolve(__dirname, './src/entities'),
      pages: path.resolve(__dirname, './src/pages'),
      shared: path.resolve(__dirname, './src/shared'),
    },
  },
});
