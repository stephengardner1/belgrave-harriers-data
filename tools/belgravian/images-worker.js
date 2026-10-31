// Cloudflare Worker "belgravian-images": serves The Belgravian archive's page scans and photos from the
// R2 bucket "belgravian-archive" (binding name BUCKET), read-only. Replaces the rate-limited r2.dev address.
// Paths match the bucket: /belgravian/pages/B171/B171-p18.webp, /belgravian/crops/B171/...
export default {
  async fetch(request, env) {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method not allowed', { status: 405, headers: { Allow: 'GET, HEAD' } });
    }
    const url = new URL(request.url);
    const key = decodeURIComponent(url.pathname.slice(1));
    if (!key.startsWith('belgravian/') || key.includes('..')) {
      return new Response('Not found', { status: 404 });
    }
    const object = await env.BUCKET.get(key, { onlyIf: request.headers, range: request.headers });
    if (object === null) return new Response('Not found', { status: 404 });
    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set('etag', object.httpEtag);
    headers.set('Cache-Control', 'public, max-age=604800'); // a week: lets corrected images replace old ones
    headers.set('Access-Control-Allow-Origin', '*');
    if (!('body' in object)) return new Response(null, { status: 304, headers });
    return new Response(request.method === 'HEAD' ? null : object.body, { headers });
  },
};
