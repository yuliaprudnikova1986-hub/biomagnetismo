// Service Worker — Par Biomagnético
// Кэширует приложение для офлайн-работы.
// При обновлении сайта увеличь номер версии (v1 → v2), чтобы кэш обновился.
const CACHE = 'biomag-v2';

const SHELL = [
  './',
  './index.html',
  './disease_data.js',
  './rastreo_data.js',
  './manifest.json',
  './img/icon-192.png',
  './img/icon-512.png'
];

// Установка: кэшируем оболочку приложения
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

// Активация: удаляем старые кэши и фоном докачиваем все 325 картинок пар
self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)));
    await self.clients.claim();
    // Фоновая предзагрузка картинок пар (партиями, ошибки игнорируем)
    const cache = await caches.open(CACHE);
    const urls = [];
    for (let n = 1; n <= 325; n++) {
      urls.push(`./img/pbs/pb_${String(n).padStart(3, '0')}.jpg`);
    }
    const BATCH = 10;
    for (let i = 0; i < urls.length; i += BATCH) {
      const batch = urls.slice(i, i + BATCH).map(async (u) => {
        const hit = await cache.match(u);
        if (hit) return;
        try {
          const res = await fetch(u);
          if (res.ok) await cache.put(u, res);
        } catch (e) { /* офлайн или ошибка — докачается при просмотре */ }
      });
      await Promise.all(batch);
    }
  })());
});

// Запросы: сначала кэш, потом сеть (и кладём в кэш то, что скачали)
self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith((async () => {
    const cached = await caches.match(req, { ignoreSearch: true });
    if (cached) return cached;
    try {
      const res = await fetch(req);
      if (res.ok) {
        const cache = await caches.open(CACHE);
        cache.put(req, res.clone());
      }
      return res;
    } catch (e) {
      // Офлайн: для навигации отдаём index.html
      if (req.mode === 'navigate') {
        const fallback = await caches.match('./index.html');
        if (fallback) return fallback;
      }
      return new Response('Sin conexión', { status: 503, statusText: 'Offline' });
    }
  })());
});
