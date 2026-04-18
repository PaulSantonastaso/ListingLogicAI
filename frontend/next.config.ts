import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    // Allow images proxied from the FastAPI backend
    remotePatterns: [
      {
        protocol: "http",
        hostname: "localhost",
        port: "8000",
        pathname: "/api/images/**",
      },
      {
        // Railway production — hostname filled in at deploy time
        protocol: "https",
        hostname: "*.up.railway.app",
        pathname: "/api/images/**",
      },
    ],
  },
};

export default nextConfig;
