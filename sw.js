/*
 * Buildora Materials — Service Worker
 * GitHub Pages can't be told to send long-lived Cache-Control headers, so
 * this fills the gap for repeat visits: images and scripts are cached on
 * the client and served instantly on the next visit, while HTML always
 * goes to the network first so content never goes stale for online users.
 */
'use strict';

var CACHE_VERSION = 'buildora-v1';
var IMAGE_CACHE = CACHE_VERSION + '-images';
var ASSET_CACHE = CACHE_VERSION + '-assets';

self.addEventListener('install', function (event) {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys
          .filter(function (key) { return key.indexOf(CACHE_VERSION) !== 0; })
          .map(function (key) { return caches.delete(key); })
      );
    }).then(function () { return self.clients.claim(); })
  );
});

function isImageRequest(url) {
  return /\/assets\/images\/.+\.(webp|svg|png|jpe?g)$/i.test(url.pathname);
}

function isScriptRequest(url) {
  return /\/js\/.+\.js$/i.test(url.pathname);
}

/* Cache-first: images rarely change and are the heaviest assets on the site. */
function cacheFirst(request, cacheName) {
  return caches.open(cacheName).then(function (cache) {
    return cache.match(request).then(function (cached) {
      if (cached) return cached;
      return fetch(request).then(function (response) {
        if (response.ok) cache.put(request, response.clone());
        return response;
      });
    });
  });
}

/* Stale-while-revalidate: serve cached JS instantly, refresh in background. */
function staleWhileRevalidate(request, cacheName) {
  return caches.open(cacheName).then(function (cache) {
    return cache.match(request).then(function (cached) {
      var networkFetch = fetch(request).then(function (response) {
        if (response.ok) cache.put(request, response.clone());
        return response;
      }).catch(function () { return cached; });
      return cached || networkFetch;
    });
  });
}

self.addEventListener('fetch', function (event) {
  var request = event.request;
  if (request.method !== 'GET') return;

  var url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (isImageRequest(url)) {
    event.respondWith(cacheFirst(request, IMAGE_CACHE));
  } else if (isScriptRequest(url)) {
    event.respondWith(staleWhileRevalidate(request, ASSET_CACHE));
  }
  /* HTML/navigation requests: no interception, always hits the network. */
});
