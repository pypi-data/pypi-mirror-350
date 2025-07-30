/*! Copyright 2025 (c)
    @license GPL
    Aurora {{project.version}}
*/
var _ = "{% load static %}";
var version = "{{project.version}}";
var staticCacheName = "aurora-pwa";
var min = "{{ min }}"
var filesToCache = [
    "{% static 'pwa/pwa.js' %}",
    "{% static 'pwa/icons/icon-128x128.png' %}",
];

// Cache on install
self.addEventListener("install", event => {
    console.log("SW: install")
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// // Serve from Cache
// self.addEventListener("fetch", event => {
//     event.respondWith(
//         caches.match(event.request)
//             .then(response => {
//                 return response || fetch(event.request);
//             })
//             .catch(() => {
//                 return caches.match('/pwa/offline/');
//             })
//     )
// });
self.addEventListener('fetch', async (event) => {
    // // Is this a request for an image?
    // if (event.request.destination === 'image') {
    //     // Open the cache
        event.respondWith(caches.open(staticCacheName).then((cache) => {
            // Respond with the image from the cache or from the network
            return cache.match(event.request).then((cachedResponse) => {
                console.log("Getting: ",cachedResponse)
                return cachedResponse || fetch(event.request.url).then((fetchedResponse) => {
                    // Add the network response to the cache for future visits.
                    // Note: we need to make a copy of the response to save it in
                    // the cache and use the original as the request response.
                    console.log("Storing: ", event.request.url)
                    cache.put(event.request, fetchedResponse.clone());

                    // Return the network response
                    return fetchedResponse;
                });
            });
        }));
    // } else {
    //     return;
    // }
});
self.addEventListener('activate', event => {
    console.log("SW: activate")
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      return keys.map(async (cache) => {
        if(cache !== cacheName) {
          console.log('Service Worker: Removing old cache: '+cache);
          return await caches.delete(cache);
        }
      })
    })()
  )
})
// self.addEventListener('install', function (event) {
//     console.log("SW: install")
//     event.waitUntil(self.skipWaiting()); // iivate worker immediately
// });

// self.addEventListener('activate', event => {
//     console.log("SW: activate")
//     notifyClient({version: version});
//
//     event.waitUntil(
//         caches.keys().then(cacheNames => {
//             return Promise.all(
//                 cacheNames
//                     .filter(cacheName => (cacheName.startsWith("aurora-pwa-")))
//                     .filter(cacheName => (cacheName !== staticCacheName))
//                     .map(cacheName => caches.delete(cacheName))
//             );
//         })
//     )
//     event.waitUntil(self.clients.claim());
// });
