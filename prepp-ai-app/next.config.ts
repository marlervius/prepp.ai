import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  // Standalone output — produces a self-contained folder for Docker / Render
  output: "standalone",
};

export default nextConfig;
