const CACHE_NAME = "xe-calculator-v1";
const urlsToCache = [
  "/",
  "https://cdn-icons-png.flaticon.com/512/1046/1046784.png"
];

// Устанавливаем Service Worker и кэшируем ресурсы
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

// Обслуживаем запросы из кэша
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});
