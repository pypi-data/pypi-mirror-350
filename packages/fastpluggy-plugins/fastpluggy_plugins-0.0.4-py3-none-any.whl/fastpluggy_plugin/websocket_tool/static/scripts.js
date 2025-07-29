// ------------------------------------------------------
// 🔁 Fetch Service Worker version and initialize it
// ------------------------------------------------------
fetch("/sw_info.json")
    .then(res => res.json())
    .then(data => {
        window.SW_VERSION = data.version;
        console.log("[SW] Loaded version:", window.SW_VERSION);
        initServiceWorker();
    })
    .catch(err => {
        console.warn("[SW] Failed to fetch version:", err);
        initServiceWorker(); // fallback with no version
    });

// ------------------------------------------------------
// 🚀 Register the Service Worker + Init WebSocket
// ------------------------------------------------------
function initServiceWorker() {
    if (!('serviceWorker' in navigator)) {
        console.error("[SW] Not supported in this browser.");
        return;
    }

    const versionSuffix = window.SW_VERSION ? `?v=${window.SW_VERSION}` : "";
    const swPath = `/service-worker.js${versionSuffix}`;

    navigator.serviceWorker.register(swPath, { scope: '/' })
        .then(reg => {
            console.log("[SW] Registered:", reg.scope);
            return navigator.serviceWorker.ready;
        })
        .then(() => {
            const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
            const wsHost = window.location.host;
            const wsUrl = `${wsProtocol}//${wsHost}/ws`;

            if (navigator.serviceWorker.controller) {
                navigator.serviceWorker.controller.postMessage({
                    type: 'INIT_WEBSOCKET',
                    wsUrl: wsUrl
                });
                console.log("[SW] Init WebSocket message sent");
            } else {
                console.warn("[SW] Controller not ready — reload may be needed.");
            }
        })
        .catch(error => {
            console.error("[SW] Registration failed:", error);
        });
}

// ------------------------------------------------------
// 📬 Listen to Service Worker WebSocket messages
// ------------------------------------------------------
navigator.serviceWorker.addEventListener('message', event => {
    if (event.data.type === 'WEBSOCKET_MESSAGE') {
        const data = event.data.data;

        if (window.WebSocketRegistry && typeof window.WebSocketRegistry.emit === 'function') {
            window.WebSocketRegistry.emit(data);
        } else {
            console.warn("[WebSocket] WebSocketRegistry not ready or invalid:", data);
        }
    }
});

// ------------------------------------------------------
// 💬 Default toast handler for "message" type
// ------------------------------------------------------
safeRegisterHandler("message", (data) => {
    showNotification(data.content, data.meta?.level, data.meta?.link);
});

// ------------------------------------------------------
// 🧠 Safe registration using deferred queue
// ------------------------------------------------------
function safeRegisterHandler(type, callback) {
    if (window.WebSocketRegistry) {
        window.WebSocketRegistry.registerHandler(type, callback);
    } else {
        if (!window.__WebSocketRegistryQueue) {
            window.__WebSocketRegistryQueue = [];
        }
        window.__WebSocketRegistryQueue.push({ type, callback });
    }
}

// ------------------------------------------------------
// 📢 Toast Notification (Tabler-compatible)
// ------------------------------------------------------
function showNotification(message, level = "info", link = null) {
    const container = document.getElementById("notifications");

    const levelClasses = {
        info: "bg-primary text-white",
        warning: "bg-warning text-dark",
        error: "bg-danger text-white",
        success: "bg-success text-white"
    };
    const colorClass = levelClasses[level] || "bg-primary text-white";

    const textNode = document.createElement("div");
    textNode.appendChild(document.createTextNode(message));
    const escapedMessage = textNode.innerHTML;

    const notification = document.createElement("div");
    notification.className = `toast show mb-3 ${colorClass}`;
    notification.role = "alert";

    let toastContent = `
        <div class="toast-header">
            <strong class="me-auto">Task Update</strong>
            <button type="button" class="btn-close ms-2 mb-1" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">${escapedMessage}
    `;

    if (link) {
        toastContent += `
            <div class="mt-2">
                <a href="${link}" target="_blank" class="text-white text-decoration-underline">View details</a>
            </div>
        `;
    }

    toastContent += `</div>`;
    notification.innerHTML = toastContent;

    container.appendChild(notification);

    setTimeout(() => {
        if (container.contains(notification)) {
            container.removeChild(notification);
        }
    }, 5000);
}
