// Service Worker pour BENJ INSIDE PWA
const CACHE_NAME = 'benj-inside-v1.0.0';
const urlsToCache = [
  '/',
  '/static/css/styles.css',
  '/static/css/pwa-styles.css',
  '/static/js/theme.js',
  '/static/js/main.js',
  '/static/js/language-switcher.js',
  '/static/js/persistent-audio-player.js',
  '/static/js/pwa.js',
  '/static/images/benj_logo.jpeg',
  '/static/images/kadosh_logo.png',
  '/static/images/icon-72x72.svg',
  '/static/images/icon-192x192.svg',
  '/static/images/icon-512x512.svg',
  '/static/manifest.json',
  'https://cdn.tailwindcss.com',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
];

// Installation du Service Worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Cache ouvert');
        return cache.addAll(urlsToCache);
      })
  );
});

// Activation du Service Worker
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('Suppression ancien cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Stratégie de cache: Network First avec fallback sur cache
self.addEventListener('fetch', function(event) {
  event.respondWith(
    fetch(event.request)
      .then(function(response) {
        // Si la requête réussit, mettre en cache la réponse
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME)
            .then(function(cache) {
              cache.put(event.request, responseClone);
            });
        }
        return response;
      })
      .catch(function() {
        // Si le réseau échoue, essayer le cache
        return caches.match(event.request)
          .then(function(response) {
            if (response) {
              return response;
            }
            // Page offline par défaut pour les routes non mises en cache
            if (event.request.destination === 'document') {
              return caches.match('/');
            }
          });
      })
  );
});

// Gestion des notifications push (pour future implémentation)
self.addEventListener('push', function(event) {
  const options = {
    body: event.data ? event.data.text() : 'Nouvelle notification BENJ INSIDE',
    icon: '/static/images/icon-192x192.png',
    badge: '/static/images/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Voir',
        icon: '/static/images/icon-192x192.png'
      },
      {
        action: 'close',
        title: 'Fermer',
        icon: '/static/images/icon-192x192.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('BENJ INSIDE', options)
  );
});

// Gestion des clics sur notifications
self.addEventListener('notificationclick', function(event) {
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});