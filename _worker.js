export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Try to serve static assets
    const response = await env.ASSETS.fetch(request);
    if (response.status !== 404) {
      return response;
    }
    
    // Fallback to index.html for SPA-like behavior
    const indexPath = url.pathname.endsWith('/') 
      ? url.pathname + 'index.html' 
      : url.pathname;
    
    const indexResponse = await env.ASSETS.fetch(new Request(
      new URL(indexPath, request.url),
      request
    ));
    
    if (indexResponse.status !== 404) {
      return indexResponse;
    }
    
    // Ultimate fallback
    return new Response('Not Found', { status: 404 });
  }
};
