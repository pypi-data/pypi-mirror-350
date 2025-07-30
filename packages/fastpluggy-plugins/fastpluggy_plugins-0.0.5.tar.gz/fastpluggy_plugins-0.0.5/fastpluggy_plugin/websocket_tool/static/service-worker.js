const SW_VERSION = (() => {
    const url = new URL(self.location);
    return url.searchParams.get("v") || "unknown";
})();
self.addEventListener('install', event => {
    console.log(`Service Worker (v${SW_VERSION}): Installed`);
});

self.addEventListener('activate', event => {
    console.log(`Service Worker (v${SW_VERSION}): Activated`);
    event.waitUntil(self.clients.claim()); // Take control of uncontrolled clients
});

self.addEventListener('message', event => {
    // Handle messages from the main thread
    if (event.data.type === 'INIT_WEBSOCKET') {
        connectWebSocket(event.data.wsUrl);
    }
});

// WebSocket Connection (optional use for service worker messaging)
let websocket;

function connectWebSocket(wsUrl) {
    console.log('Service Worker: Connecting WebSocket to', wsUrl);
    websocket = new WebSocket(wsUrl);

    websocket.onopen = () => {
        console.log('Service Worker: WebSocket connected');
    };

    websocket.onmessage = event => {
        console.debug('Service Worker: WebSocket message received', event.data);
        const data = parseWebsocketMessage(event.data);

        if (data && data.type) {
            self.clients.matchAll().then(clients => {
                clients.forEach(client => {
                    client.postMessage({
                        type: 'WEBSOCKET_MESSAGE',
                        data
                    });
                });
            });
        } else {
            console.error("Service Worker: Invalid WebSocket message:", data);
        }
    };

    websocket.onerror = error => {
        console.error('Service Worker: WebSocket error:', error);
    };

    websocket.onclose = () => {
        console.warn('Service Worker: WebSocket closed. Reconnecting...');
        setTimeout(() => connectWebSocket(wsUrl), 5000);
    };
}

function parseWebsocketMessage(message) {
    try {
        return JSON.parse(message);
    } catch (error) {
        console.error('Service Worker: Failed to parse WebSocket message:', error);
        return {};
    }
}
