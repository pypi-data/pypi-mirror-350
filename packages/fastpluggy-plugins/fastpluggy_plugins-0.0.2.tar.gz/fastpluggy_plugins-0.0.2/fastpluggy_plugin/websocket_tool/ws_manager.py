# ws_manager.py
import asyncio
from typing import Optional, Dict, List, Tuple

from fastapi import WebSocket
from loguru import logger

from .schema.ws_message import WebSocketMessage


class ConnectionManager:
    def __init__(self):
        # Queue holds tuples of (message, optional target client_id)
        self.queue: asyncio.Queue[Tuple[WebSocketMessage, Optional[str]]] = asyncio.Queue()
        self._consumer_task: asyncio.Task | None = None

        self.active_connections: Dict[str, WebSocket] = {}
        self.unnamed_connections: List[WebSocket] = []

        # will be set to the running loop on first connect()
        self.loop: asyncio.AbstractEventLoop | None = None
    #
    # def get_loop(self) -> asyncio.AbstractEventLoop:
    #     try:
    #         return asyncio.get_running_loop()
    #     except RuntimeError:
    #         # No loop yet—create one (should only happen in very early imports)
    #         loop = asyncio.new_event_loop()
    #         asyncio.set_event_loop(loop)
    #         return loop

    async def connect(self, websocket: WebSocket, client_id: Optional[str] = None):
        # grab & cache the running loop once
        if self.loop is None:
            self.loop = asyncio.get_event_loop()

            # start the queue consumer exactly once
        if not self._consumer_task or self._consumer_task.done():
            self._consumer_task = self.loop.create_task(self._consumer())

        await websocket.accept()
        if client_id:
            self.active_connections[client_id] = websocket
        else:
            self.unnamed_connections.append(websocket)

    def disconnect(self, websocket_or_client_id: Optional[str] = None):
        if isinstance(websocket_or_client_id, str):
            self.active_connections.pop(websocket_or_client_id, None)
        else:
            try:
                self.unnamed_connections.remove(websocket_or_client_id)
            except ValueError:
                pass

    async def send_to_client(
        self, message: WebSocketMessage, client_id: Optional[str] = None
    ):
        payload = message.to_json()
        if client_id:
            ws = self.active_connections.get(client_id)
            if not ws:
                return
            try:
                await ws.send_json(payload)
            except Exception:
                logger.exception(f"Error sending to {client_id}, disconnecting")
                self.disconnect(client_id)
        else:
            await self.broadcast(message)

    async def broadcast(self, message: WebSocketMessage):
        payload = message.to_json()
        all_sockets = list(self.active_connections.values()) + self.unnamed_connections
        # Send in parallel, catching and handling per-connection errors
        coros = [self._safe_send(ws, payload) for ws in all_sockets]
        if coros:
            await asyncio.gather(*coros, return_exceptions=True)

    async def _safe_send(self, ws: WebSocket, payload: dict):
        try:
            await ws.send_json(payload)
        except Exception:
            logger.exception("Error during broadcast, disconnecting")
            self.disconnect(ws)

    # def _start_consumer(self):
    #     """Fire-and-forget the background task that drains the queue."""
    #     loop = self.get_loop()
    #     self._consumer_task = loop.create_task(self._consumer())

    async def _consumer(self):
        """Continuously pull (message, client_id) tuples and dispatch."""
        while True:
            message, client_id = await self.queue.get()
            try:
                await self.send_to_client(message, client_id)
            except Exception as e:
                logger.exception(f"Error in queue consumer: {e}")

    def notify(self, message: WebSocketMessage, client_id: Optional[str] = None):
        """
        Thread‐safe entry point for worker threads.
        Enqueues onto the loop’s queue without ever re-creating or re-fetching the loop.
        """
        if not self.loop:
            # no loop = no one connected yet, drop or buffer locally
            print("No event loop available; dropping WebSocketMessage")
            return

        # schedule the enqueue on the stored loop
        self.loop.call_soon_threadsafe(self.queue.put_nowait, (message, client_id))


    def list_clients(self) -> List[Dict[str, str]]:
        named = [{"client_id": cid, "type": "named"} for cid in self.active_connections]
        anonymous = [
            {"client_id": f"anon-{i+1}", "type": "anonymous"}
            for i in range(len(self.unnamed_connections))
        ]
        return named + anonymous
