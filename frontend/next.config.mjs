/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
            {
            source: '/appointments/:path*',
            destination: 'http://localhost:8000/appointments/:path*',
            },
            {
            source: '/auth/:path*',
            destination: 'http://localhost:8000/auth/:path*',
            },
        ];
    },
};

export default nextConfig;
