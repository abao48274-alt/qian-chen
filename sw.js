const CACHE_NAME = 'anime-studio-v1';
const ASSETS_TO_CACHE = [
    './',
    './index.html',
    './manifest.json',
    './icon-192.png',
    './icon-512.png'
];

// Install Service Worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Caching assets');
                return cache.addAll(ASSETS_TO_CACHE);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate Service Worker
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch Strategy: Network First, Cache Fallback
self.addEventListener('fetch', (event) => {
    event.respondWith(
        fetch(event.request)
            .then((response) => {
                // Clone the response
                const responseClone = response.clone();
                
                // Cache the fetched response
                caches.open(CACHE_NAME)
                    .then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                
                return response;
            })
            .catch(() => {
                // If network fails, try cache
                return caches.match(event.request);
            })
    );
});

// Background Sync for offline actions
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-scenes') {
        event.waitUntil(syncScenes());
    }
});

async function syncScenes() {
    // Sync local changes when back online
    console.log('Syncing scenes...');
}

// Push notifications
self.addEventListener('push', (event) => {
    const options = {
        body: event.data ? event.data.text() : 'New update available!',
        icon: './icon-192.png',
        badge: './icon-192.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            { action: 'explore', title: '查看' },
            { action: 'close', title: '关闭' }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('千尘AI动漫工厂', options)
    );
});