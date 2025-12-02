/**
 * Cloudflare Workers entry point for gellax API
 * Handles routing and proxying requests to the backend
 */

const BACKEND_URL = 'http://localhost:8000';
const API_PREFIX = '/api';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    // CORS headers for API requests
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: corsHeaders,
      });
    }

    try {
      // Proxy API requests to backend
      if (pathname.startsWith(API_PREFIX)) {
        const backendPath = pathname.replace(API_PREFIX, '');
        const backendUrl = new URL(BACKEND_URL + backendPath + url.search);

        const backendRequest = new Request(backendUrl, {
          method: request.method,
          headers: request.headers,
          body: request.method !== 'GET' && request.method !== 'HEAD' ? await request.text() : undefined,
        });

        let response = await fetch(backendRequest);

        // Add CORS headers to response
        response = new Response(response.body, response);
        Object.entries(corsHeaders).forEach(([key, value]) => {
          response.headers.set(key, value);
        });

        return response;
      }

      // Serve frontend assets
      const frontendPath = pathname === '/' ? '/index.html' : pathname;
      const assetUrl = new URL(frontendPath, env.ASSETS || 'http://localhost:3000');

      let response = await fetch(assetUrl);

      if (!response.ok && pathname !== '/index.html') {
        // Fallback to index.html for SPA routing
        response = await fetch(new URL('/index.html', env.ASSETS || 'http://localhost:3000'));
      }

      // Add cache headers for static assets
      if (pathname.match(/\.(js|css|png|jpg|gif|svg|woff|woff2)$/)) {
        response = new Response(response.body, response);
        response.headers.set('Cache-Control', 'public, max-age=31536000');
      }

      return response;
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders,
        },
      });
    }
  },

  async scheduled(event, env, ctx) {
    // Scheduled event handler for periodic tasks
    // Example: cleanup, cache invalidation, etc.
    console.log('Scheduled event triggered', event.cron);
  },
};
