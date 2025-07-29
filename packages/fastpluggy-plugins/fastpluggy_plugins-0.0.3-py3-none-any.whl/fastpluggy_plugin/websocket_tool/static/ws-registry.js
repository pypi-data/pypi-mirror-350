(function () {
    if (!window.__WebSocketRegistryQueue) {
        window.__WebSocketRegistryQueue = [];
    }

    function flushQueue(registry) {
        while (window.__WebSocketRegistryQueue.length > 0) {
            const { type, callback } = window.__WebSocketRegistryQueue.shift();
            registry.registerHandler(type, callback);
        }
    }

    const WebSocketRegistry = {
        handlers: {},

        registerHandler(type, callback) {
            if (!this.handlers[type]) {
                this.handlers[type] = [];
            }
            console.log(`[WebSocket] Handler registered for "${type}"`);
            this.handlers[type].push(callback);
        },

        emit(message) {
            const type = message.type || message.meta?.event;
            if (this.handlers[type]) {
                this.handlers[type].forEach(cb => cb(message));
            }
        },

        clearHandlers(type = null) {
            if (type) {
                delete this.handlers[type];
            } else {
                this.handlers = {};
            }
        },

        getRegisteredTypes() {
            return Object.keys(this.handlers);
        }
    };

    // Register globally
    window.WebSocketRegistry = WebSocketRegistry;

    // Flush any early registrations
    flushQueue(WebSocketRegistry);
})();
