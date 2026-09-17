/* Offline shell for the fan deck. Network first, so an online device always gets the
   newest page; the cache only answers when the network does not. Bump CACHE to drop
   old copies. Service workers need https or localhost, so this does nothing over plain
   http on a LAN address. */
const CACHE = 'fan-deck-v1';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icon.svg', 'icon-180.png', 'icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  e.respondWith(
    fetch(req).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(req, copy));
      return res;
    }).catch(() => caches.match(req, {ignoreSearch: true}).then(hit => hit || caches.match('index.html')))
  );
});
