/** @type {import('next').NextConfig} */
const nextConfig = {
    output:'standalone',
    rewrites: async () => {
        return [
            {
                source: '/api/:path*',
                destination: process.env.NODE_ENV === 'development'
                    ? 'http://127.0.0.1:8000/api/:path*' // For local npm run dev
                    : 'http://backend:8000/api/:path*', // For Docker
            },
        ]
    },
}

module.exports = nextConfig
