"""
GAR Client Module

See GARClient documentation for more details.
"""

import asyncio
import json
import time
import threading
from typing import Dict, Any, Optional, Callable, Tuple
from decimal import Decimal
import logging
import os
import ssl
import getpass
import websockets
import __main__
from websockets.legacy.client import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosed


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
class GARClient:
    """
    A client implementation for the Generic Active Records (GAR) protocol using WebSockets.

    See trsgar.py for example usage.

    The GARClient class provides a Python interface for connecting to a GAR server
    using WebSockets as the transport layer. It handles the protocol details including
    message serialization, heartbeat management, topic and key enumeration, record
    updates, and subscription management.

    The client maintains separate mappings for server-assigned and client-assigned
    topic and key IDs, allowing for independent enumeration on both sides. It provides
    methods for subscribing to data, publishing records, and registering handlers for
    various message types.

    Key features:
    - Automatic heartbeat management to maintain connection
    - Support for topic and key int <-> string introductions
    - Record creation, updating, and deletion
    - Subscription management with filtering options
    - Customizable message handlers for all protocol message types
    - Thread-safe message sending
    - Automatic reconnection on WebSocket connection loss

    See the full documentation at https://trinityriversystems.com/docs/ for detailed
    protocol specifications and usage instructions.
    """

    def __init__(
        # pylint: disable=too-many-arguments
        self,
        ws_endpoint: str,
        working_namespace: str | None = None,
        heartbeat_interval: int = 4000,
        allow_self_signed_certificate: bool = False,
    ) -> None:
        """
        Initialize the GAR (Generic Active Records) client.

        Creates a new GAR client instance that connects to a GAR server using WebSockets.
        It sets up internal data structures for tracking topics, keys, and message handlers,
        and initializes the heartbeat mechanism for maintaining the connection.

        Args:
            ws_endpoint: WebSocket endpoint string in the format "ws://address:port"
                         (e.g., "ws://localhost:8765") where the GAR server is listening.
            user: Client username string used for identification and authentication
                  with the server. This is included in the socket identity.
            heartbeat_interval: Time in milliseconds between heartbeat messages sent
                  to the server to maintain the connection. Default is 4000ms (4 seconds).

        Returns:
            None

        Note:
            The client is not started automatically after initialization.
            Call the start() method to begin communication with the server.
            start() will run the IO loop until stop() is called.
            Use threading.Thread(target=gar_client.start) to run in the background.
        """
        self.ws_endpoint = ws_endpoint
        # pylint: disable=no-member
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.connected = False
        self.reconnect_delay = 5.0  # Seconds to wait before reconnecting

        self.pid = os.getpid()
        self.logger = logging.getLogger(__name__)

        self.user = os.getenv("GAR_USERNAME") or os.environ.get(
            "USER", getpass.getuser()
        )
        self.application = os.path.basename(getattr(__main__, "__file__", "unknown-py"))
        self.working_namespace = working_namespace
        self.heartbeat_interval = heartbeat_interval
        self.version = 650269

        self.server_topic_map: Dict[int, str] = {}
        self.server_key_map: Dict[int, str] = {}

        self.local_topic_counter = 1
        self.local_key_counter = 1
        self.local_topic_map: Dict[str, int] = {}
        self.local_key_map: Dict[str, int] = {}

        self.running = False
        self.heartbeat_thread: Optional[threading.Thread] = None

        self.message_handlers: Dict[str, Callable[[Dict[str, Any]], None]] = {}

        self.last_heartbeat_time = time.time()
        self.heartbeat_timeout = 3  # Default 3 seconds
        # for “10× grace” on the very first heartbeat
        self._initial_grace_period = False
        self._initial_grace_deadline = 0.0

        self.heartbeat_timeout_callback: Optional[Callable[[], None]] = None
        self.stopped_callback: Optional[Callable[[], None]] = None

        self.record_map: Dict[Tuple[int, int], Any] = {}

        self.allow_self_signed_certificate = allow_self_signed_certificate
        self.exit_code = 0

        logging.basicConfig(level=logging.INFO)
        self.register_default_handlers()

        # Asyncio event loop for WebSocket operations
        self.loop = asyncio.new_event_loop()

    async def connect(self) -> None:
        """Establish WebSocket connection with reconnection logic, using GAR subprotocol."""
        while self.running and not self.connected:
            try:
                connect_kwargs: Dict[str, Any] = {"subprotocols": ["gar-protocol"]}
                if self.ws_endpoint.lower().startswith("wss://"):
                    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                    if self.allow_self_signed_certificate:
                        ssl_ctx.check_hostname = False
                        ssl_ctx.verify_mode = ssl.CERT_NONE
                    connect_kwargs["ssl"] = ssl_ctx

                async with websockets.connect(
                    self.ws_endpoint, **connect_kwargs
                ) as websocket:
                    self.websocket = websocket  # type: ignore
                    self.connected = True
                    self.logger.info(
                        "Connected to WebSocket server at %s using gar-protocol",
                        self.ws_endpoint,
                    )
                    await asyncio.gather(
                        self._send_messages(), self._receive_messages()
                    )
            except (ConnectionClosed, ConnectionRefusedError) as e:
                self.logger.error(
                    "WebSocket connection failed: %s. Reconnecting in %s seconds...",
                    e,
                    self.reconnect_delay,
                )
                self.connected = False
                self.websocket = None
                await asyncio.sleep(self.reconnect_delay)

    async def _send_messages(self) -> None:
        """Send messages from the queue to the WebSocket server."""
        while self.connected and (self.running or not self.message_queue.empty()):
            try:
                message = await self.message_queue.get()
                if message is None:
                    break
                if self.websocket:
                    await self.websocket.send(json.dumps(message))
                    self.logger.debug("Sent: %s", json.dumps(message))
                self.message_queue.task_done()
            except ConnectionClosed:
                self.logger.warning("Connection closed while sending.")
                self.stop()
                break
            # pylint: disable=broad-exception-caught
        self.connected = False
        self.logger.info("Done sending messages.")

        # try to clear spurious "RuntimeWarning: coroutine 'Queue.put' was never awaited"
        self.message_queue.get_nowait()

    async def _receive_messages(self) -> None:
        """Receive and process messages from the WebSocket server."""
        while self.connected and self.running:
            try:
                if self.websocket:
                    message = await asyncio.wait_for(self.websocket.recv(), timeout=1)
                    msg = json.loads(message, parse_float=Decimal)
                    self._process_message(msg)
            except asyncio.TimeoutError:
                self.check_heartbeat()
            except ConnectionClosed:
                self.logger.warning("Connection closed while receiving.")
                self.halt()
                break
            except json.JSONDecodeError as e:
                self.logger.error("Invalid JSON received: %s", e)
                break
        self.stop()
        asyncio.run_coroutine_threadsafe(
            self.message_queue.put(None), self.loop
        )  # Put None into the queue to stop the send loop
        self.logger.info("Done receiving messages.")

    def register_handler(
        self, message_type: str, handler: Callable[[Dict[str, Any]], None]
    ) -> None:
        """Register a callback handler for a specific message type."""
        self.message_handlers[message_type] = handler

    def register_introduction_handler(
        self, handler: Callable[[int, int, str, Optional[str]], None]
    ) -> None:
        """Handler for Introduction: (version, heartbeat_timeout_interval, user, schema)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(
                value["version"],
                value["heartbeat_timeout_interval"],
                value["user"],
                value.get("schema"),
            )

        self.register_handler("Introduction", wrapper)

    def clear_introduction_handler(self) -> None:
        """Remove the registered introduction handler."""
        self.message_handlers.pop("Introduction", None)

    def register_heartbeat_handler(self, handler: Callable[[int], None]) -> None:
        """Handler for Heartbeat"""

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["u_milliseconds"])

        self.register_handler("Heartbeat", wrapper)

    def clear_heartbeat_handler(self) -> None:
        """Remove the registered heartbeat handler."""
        self.message_handlers.pop("Heartbeat", None)

    def register_logoff_handler(self, handler: Callable[[], None]) -> None:
        """Handler for Logoff: no arguments"""

        # pylint: disable=unused-argument
        def wrapper(msg: Dict[str, Any]):
            handler()

        self.register_handler("Logoff", wrapper)

    def clear_logoff_handler(self) -> None:
        """Remove the registered logoff handler."""
        self.message_handlers.pop("Logoff", None)

    def register_error_handler(self, handler: Callable[[str], None]) -> None:
        """Handler for Error: (message)"""

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["message"])

        self.register_handler("Error", wrapper)

    def clear_error_handler(self) -> None:
        """Remove the registered error handler."""
        self.message_handlers.pop("Error", None)

    def register_topic_introduction_handler(
        self, handler: Callable[[int, str], None]
    ) -> None:
        """Handler for TopicIntroduction: (topic_id, name)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["topic_id"], value["name"])

        self.register_handler("TopicIntroduction", wrapper)

    def clear_topic_introduction_handler(self) -> None:
        """Remove the registered topic introduction handler."""
        self.message_handlers.pop("TopicIntroduction", None)

    def register_key_introduction_handler(
        self, handler: Callable[[int, str, Optional[str]], None]
    ) -> None:
        """Handler for KeyIntroduction: (key_id, name, _class)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["key_id"], value["name"], value.get("_class"))

        self.register_handler("KeyIntroduction", wrapper)

    def clear_key_introduction_handler(self) -> None:
        """Remove the registered key introduction handler."""
        self.message_handlers.pop("KeyIntroduction", None)

    def register_delete_key_handler(self, handler: Callable[[int], None]) -> None:
        """Handler for DeleteKey: (key_id)"""

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["key_id"])

        self.register_handler("DeleteKey", wrapper)

    def clear_delete_key_handler(self) -> None:
        """Remove the registered delete key handler."""
        self.message_handlers.pop("DeleteKey", None)

    def register_subscription_status_handler(
        self, handler: Callable[[str, str], None]
    ) -> None:
        """
        Handler for SubscriptionStatus: (name)
        Callback args are (name, status)
        status can be "Streaming" or "Finished"
        """

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["name"], msg["value"]["status"])

        self.register_handler("SubscriptionStatus", wrapper)

    def clear_subscription_status_handler(self) -> None:
        """Remove the registered subscription status handler."""
        self.message_handlers.pop("SubscriptionStatus", None)

    def register_delete_record_handler(
        self, handler: Callable[[int, int], None]
    ) -> None:
        """Handler for DeleteRecord: (key_id, topic_id)"""

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["key_id"], msg["value"]["topic_id"])

        self.register_handler("DeleteRecord", wrapper)

    def clear_delete_record_handler(self) -> None:
        """Remove the registered delete record handler."""
        self.message_handlers.pop("DeleteRecord", None)

    def register_record_update_handler(
        self, handler: Callable[[int, int, Any], None]
    ) -> None:
        """Handler for JSONRecordUpdate: (key_id, topic_id, value)"""

        def wrapper(msg: Dict[str, Any]):
            record_id = msg["value"]["record_id"]
            handler(record_id["key_id"], record_id["topic_id"], msg["value"]["value"])

        self.register_handler("JSONRecordUpdate", wrapper)

    def clear_record_update_handler(self) -> None:
        """Remove the registered record update handler."""
        self.message_handlers.pop("JSONRecordUpdate", None)

    def register_shutdown_handler(self, handler: Callable[[], None]) -> None:
        """Handler for Shutdown: no arguments"""

        # pylint: disable=unused-argument
        def wrapper(msg: Dict[str, Any]):
            handler()

        self.register_handler("Shutdown", wrapper)

    def clear_shutdown_handler(self) -> None:
        """Remove the registered shutdown handler."""
        self.message_handlers.pop("Shutdown", None)

    def register_heartbeat_timeout_handler(self, handler: Callable[[], None]) -> None:
        """Register a callback to handle heartbeat timeout events."""
        self.heartbeat_timeout_callback = handler

    def clear_heartbeat_timeout_handler(self) -> None:
        """Remove the registered heartbeat timeout handler."""
        self.heartbeat_timeout_callback = None

    def register_stopped_handler(self, handler: Callable[[], None]) -> None:
        """Register a callback to handle client stopped events."""
        self.stopped_callback = handler

    def clear_stopped_handler(self) -> None:
        """Remove the registered stopped handler."""
        self.stopped_callback = None

    def register_default_handlers(self) -> None:
        """Register default logging handlers for all message types."""
        self.register_introduction_handler(
            lambda version, interval, user, schema: self.logger.info(
                "Connected to server: %s", user
            )
        )
        self.register_heartbeat_handler(
            lambda ms: self.logger.debug("Heartbeat received %dms", ms)
        )
        self.register_logoff_handler(lambda: self.logger.info("Logoff received"))
        self.register_topic_introduction_handler(
            lambda topic_id, name: self.logger.info(
                "New server topic: %s (Server ID: %d)", name, topic_id
            )
        )
        self.register_key_introduction_handler(
            lambda key_id, name, _class: self.logger.debug(
                "New server key: %s (Server ID: %d)", name, key_id
            )
        )
        self.register_delete_key_handler(
            lambda key_id: self.logger.debug(
                "Delete key: %s (Server ID: %d)",
                self.server_key_map.get(key_id),
                key_id,
            )
        )
        self.register_subscription_status_handler(
            self._default_subscription_status_handler
        )
        self.register_delete_record_handler(
            lambda key_id, topic_id: self.logger.debug(
                "Delete record: %s - %s",
                self.server_key_map.get(key_id),
                self.server_topic_map.get(topic_id),
            )
        )
        self.register_record_update_handler(
            lambda key_id, topic_id, value: self.logger.debug(
                "Record update: %s - %s = %s",
                self.server_key_map.get(key_id),
                self.server_topic_map.get(topic_id),
                value,
            )
        )
        self.register_shutdown_handler(lambda: self.logger.info("Shutdown received"))

    def _default_subscription_status_handler(self, name: str, status: str) -> None:
        """Default handler for subscription status messages."""
        self.logger.info("Subscription %s status: %s", name, status)
        if status == "NeedsContinue":
            self.logger.info(
                "Snapshot size limit reached, sending SubscribeContinue for %s", name
            )
            self.send_subscribe_continue(name)

    def start(self) -> None:
        """Start the client and send introduction message."""
        self.running = True
        intro_msg = {
            "message_type": "Introduction",
            "value": {
                "version": self.version,
                "pid": self.pid,
                "heartbeat_timeout_interval": self.heartbeat_interval,
                "user": self.user,
                "application": self.application,
                "working_namespace": self.working_namespace,
            },
        }
        self.send_message(intro_msg)
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop, daemon=True
        )
        self.heartbeat_thread.start()
        # Run the WebSocket connection in the asyncio event loop
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect())
        self.loop.close()
        self.stop()
        if self.stopped_callback:
            self.stopped_callback()

    def stop(self) -> None:
        """
        Stop the client and terminate all client operations.
        Note this does not block until the connection is closed.
        Register a stopped callback to be notified when the control loop has stopped.
        """
        self.running = False

    def halt(self) -> None:
        """
        Stops the client without sending any pending messages.
        """
        self.stop()
        self.connected = False

    def logoff(self) -> None:
        """Send a logoff message to the server and stop the client."""
        self.send_message({"message_type": "Logoff"})
        self.stop()

    def __del__(self) -> None:
        """Clean up resources when the object is destroyed."""
        if self.loop and not self.loop.is_closed():
            self.loop.close()

    def send_message(self, message: Dict[str, Any]) -> None:
        """Send a JSON message through the WebSocket."""
        asyncio.run_coroutine_threadsafe(self.message_queue.put(message), self.loop)

    def _heartbeat_loop(self) -> None:
        """Send periodic heartbeat messages."""
        while self.running:
            msg = {
                "message_type": "Heartbeat",
                "value": {
                    "u_milliseconds": int(time.time() * 1000),
                },
            }
            self.send_message(msg)
            time.sleep(min(10, self.heartbeat_interval / 1000 / 2))

    def check_heartbeat(self) -> None:
        """Check if the heartbeat has timed out."""
        # Enforce heartbeat timeout, with 10× grace for the very first beat
        if self._initial_grace_period:
            cutoff = self._initial_grace_deadline
        else:
            cutoff = self.last_heartbeat_time + self.heartbeat_timeout
        if time.time() > cutoff:
            self.logger.warning(
                "Heartbeat failure; previous heartbeat: %.3fs",
                self.last_heartbeat_time,
            )
            self.exit_code = 1
            self.halt()
            if self.heartbeat_timeout_callback:
                self.heartbeat_timeout_callback()

    def _process_message(self, message: Dict[str, Any]) -> None:
        """Process incoming messages by calling registered handlers."""
        msg_type = message.get("message_type")
        if msg_type == "TopicIntroduction":
            self.server_topic_map[message["value"]["topic_id"]] = message["value"][
                "name"
            ]
        elif msg_type == "KeyIntroduction":
            self.server_key_map[message["value"]["key_id"]] = message["value"]["name"]
        elif msg_type == "DeleteKey":
            # 1) drop deleted key from server map
            key_id = message["value"]["key_id"]
            self.server_key_map.pop(key_id, None)
        elif msg_type == "Heartbeat":
            # update last‐beat and clear initial grace on the very first one
            self.last_heartbeat_time = time.time()
            if self._initial_grace_period:
                self._initial_grace_period = False
        elif msg_type == "Introduction":
            value = message["value"]
            # 5) Clear out old server state on reconnect
            self.server_topic_map.clear()
            self.server_key_map.clear()
            self.record_map.clear()
            # reset heartbeat timeout (in seconds)
            self.heartbeat_timeout = max(
                self.heartbeat_timeout, value["heartbeat_timeout_interval"] / 1000
            )
            self.last_heartbeat_time = time.time()
            # 4) enable 10× grace window for the *first* heartbeat
            self._initial_grace_period = True
            self._initial_grace_deadline = (
                self.last_heartbeat_time + self.heartbeat_timeout * 10
            )
        elif msg_type == "JSONRecordUpdate":
            record_id = message["value"]["record_id"]
            key_id = record_id["key_id"]
            topic_id = record_id["topic_id"]
            record_value = message["value"]["value"]
            self.record_map[(key_id, topic_id)] = record_value
        elif msg_type == "DeleteRecord":
            value = message["value"]
            key_id = value["key_id"]
            topic_id = value["topic_id"]
            self.record_map.pop((key_id, topic_id), None)
        elif msg_type == "Logoff":
            self.logger.info("Received Logoff from server")
            self.running = False
        elif msg_type == "Error":
            self.logger.error("GAR %s", message["value"]["message"])
            self.exit_code = 1
            self.stop()

        self.check_heartbeat()

        handler = self.message_handlers.get(str(msg_type))
        if handler:
            handler(message)

    # pylint: disable=too-many-arguments
    def subscribe(
        self,
        name: str,
        mode: str = "Streaming",
        key_name: Optional[str] = None,
        topic_name: Optional[str] = None,
        class_filter: Optional[str] = None,
        key_filter: Optional[str] = None,
        topic_filter: Optional[str] = None,
        all_matching_keys: Optional[bool] = False,
        snapshot_size_limit: Optional[int] = 0,
    ) -> None:
        """Send a subscription request using local IDs."""
        key_id = self.get_and_possibly_introduce_key_id(key_name) if key_name else 0
        topic_id = (
            self.get_and_possibly_introduce_topic_id(topic_name) if topic_name else 0
        )
        sub_msg = {
            "message_type": "Subscribe",
            "value": {
                "subscription_mode": mode,
                "all_matching_keys": all_matching_keys,
                "snapshot_size_limit": snapshot_size_limit,
                "nagle_interval": 0,
                "name": name,
                "key_id": key_id,
                "topic_id": topic_id,
                "_class": class_filter,
                "key_filter": key_filter,
                "topic_filter": topic_filter,
            },
        }
        self.send_message(sub_msg)

    def send_subscribe_continue(self, name: str) -> None:
        """Send a SubscribeContinue message for a subscription name."""
        msg = {"message_type": "SubscribeContinue", "value": {"name": name}}
        self.send_message(msg)

    def get_and_possibly_introduce_key_id(
        self, name: str, class_name: Optional[str] = None
    ) -> int:
        """Introduce a new key if not already known and return local key ID."""
        if name not in self.local_key_map:
            key_id = self.local_key_counter
            self.local_key_map[name] = key_id
            self.local_key_counter += 1
            msg = {
                "message_type": "KeyIntroduction",
                "value": {"key_id": key_id, "name": name, "_class": class_name},
            }
            self.send_message(msg)
        return self.local_key_map[name]

    def get_and_possibly_introduce_topic_id(self, name: str) -> int:
        """Introduce a new topic if not already known and return local topic ID."""
        if name not in self.local_topic_map:
            topic_id = self.local_topic_counter
            self.local_topic_map[name] = topic_id
            self.local_topic_counter += 1
            msg = {
                "message_type": "TopicIntroduction",
                "value": {"topic_id": topic_id, "name": name},
            }
            self.send_message(msg)
        return self.local_topic_map[name]

    def publish_delete_key(self, key_id: int) -> None:
        """Publish a DeleteKey message using a local key ID."""
        msg = {"message_type": "DeleteKey", "value": {"key_id": key_id}}
        self.send_message(msg)

    def publish_delete_record(self, key_id: int, topic_id: int) -> None:
        """Publish a DeleteRecord message using local key and topic IDs."""
        msg = {
            "message_type": "DeleteRecord",
            "value": {"key_id": key_id, "topic_id": topic_id},
        }
        self.send_message(msg)

    def publish_unsubscribe(self, name: str) -> None:
        """Publish an Unsubscribe message for a subscription name."""
        msg = {"message_type": "Unsubscribe", "value": {"name": name}}
        self.send_message(msg)

    def publish_shutdown(self) -> None:
        """Publish a Shutdown message."""
        msg = {"message_type": "Shutdown"}
        self.send_message(msg)

    def publish_record_with_ids(self, key_id: int, topic_id: int, value: Any) -> None:
        """
        Publish a record update using explicit key and topic IDs.

        This method creates and sends a JSONRecordUpdate message to the GAR server
        using the provided key and topic IDs. Unlike publish_record(), this method
        does not perform any name-to-ID conversion or introduce new keys/topics.

        Args:
            key_id: The integer ID of the key for this record. This should be a valid
                   key ID that has already been introduced to the server.
            topic_id: The integer ID of the topic for this record. This should be a valid
                     topic ID that has already been introduced to the server.
            value: The value to publish for this record. Can be any JSON-serializable
                  data type (dict, list, string, number, boolean, or null).

        Returns:
            None
        """
        update_msg = {
            "message_type": "JSONRecordUpdate",
            "value": {
                "record_id": {"key_id": key_id, "topic_id": topic_id},
                "value": value,
            },
        }
        self.send_message(update_msg)

    def publish_record(
        self,
        key_name: str,
        topic_name: str,
        value: Any,
        class_name: Optional[str] = None,
    ) -> None:
        """Publish a record update using names, converting to local IDs."""
        key_id = self.get_and_possibly_introduce_key_id(key_name, class_name)
        topic_id = self.get_and_possibly_introduce_topic_id(topic_name)
        self.publish_record_with_ids(key_id, topic_id, value)
