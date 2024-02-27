/** @type {import('next').NextConfig} */
const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: '/api/:path*',
        destination:
          process.env.NODE_ENV === 'development'
            ? 'http://127.0.0.1:8080/api/:path*'
            : '/api/',
      },
      {
        source: '/home',
        destination: '/',
      },
    ];
  },
};

module.exports = {
  ...nextConfig,
  reactStrictMode: false, // Components may render twice in development mode if set to true
};
