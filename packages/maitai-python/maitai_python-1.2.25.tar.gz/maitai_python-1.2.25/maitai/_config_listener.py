import json
import logging
import os
import threading

import websocket

from maitai.models.application import Application

logging.getLogger("websocket").setLevel(logging.FATAL)

logger = logging.getLogger("maitai")


class ConfigListener:
    def __init__(self, config, path, type, key=None):
        self.config = config
        self.ws_url = f"{path}?type={type}"
        if key:
            self.ws_url += f"&key={key}"

        self.ws = None
        self.ws_thread = None
        self.running = False

    def on_message(self, ws, message):
        event = json.loads(message)
        if event.get("event_type") == "APPLICATION_CONFIG_CHANGE":
            application_json = json.loads(event.get("event_data"))
            if application_json:
                try:
                    application = Application.model_validate(application_json)
                    logger.info("Maitai config listener: received configuration change")
                    self.config.store_application_metadata([application])
                except Exception as e:
                    if os.environ.get("MAITAI_ENV") in [
                        "development",
                        "staging",
                        "prod",
                    ]:
                        logger.error(
                            "Maitai config listener: error refreshing applications",
                            exc_info=e,
                        )
                    self.config.refresh_applications()
            else:
                self.config.refresh_applications()

    def on_error(self, ws, error):
        if not isinstance(error, (AttributeError, ConnectionError)):
            logger.error("Maitai config listener: websocket error", exc_info=error)

    def on_close(self, ws, close_status_code, close_msg):
        logger.info(
            f"Maitai config listener: websocket connection closed: {close_status_code} {close_msg}"
        )

    def on_open(self, ws):
        logger.info("Maitai config listener: websocket connection established")

    def _websocket_thread(self):
        """Run the websocket client in a thread with automatic reconnection."""
        retry_count = 0
        max_retries = 10
        reconnect_delay = 0.1  # Start with 100ms

        while self.running and retry_count < max_retries:
            try:
                # Create new websocket connection
                self.ws = websocket.WebSocketApp(
                    self.ws_url,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close,
                    on_open=self.on_open,
                )

                # Run the websocket (this blocks until connection closes)
                self.ws.run_forever(ping_interval=30, ping_timeout=10)

                # If we get here, connection closed - retry with backoff if still running
                if self.running:
                    retry_count += 1
                    # Exponential backoff with max of 2 seconds
                    retry_delay = min(reconnect_delay * (2**retry_count), 2)
                    logger.info(
                        f"Maitai config listener: websocket reconnecting in {retry_delay} seconds..."
                    )
                    threading.Event().wait(retry_delay)
            except Exception as e:
                logger.error(
                    "Maitai config listener error in websocket thread", exc_info=e
                )
                if self.running:
                    retry_count += 1
                    # Exponential backoff with max of 2 seconds
                    retry_delay = min(reconnect_delay * (2**retry_count), 2)
                    logger.info(
                        f"Maitai config listener: websocket reconnecting in {retry_delay} seconds..."
                    )
                    threading.Event().wait(retry_delay)

    def _reconnect(self):
        """Attempt to reconnect the websocket."""
        if self.ws:
            try:
                self.ws.close()
            except:
                pass
            self.ws = None

    def start(self):
        """Start the websocket connection."""
        if self.running:
            return

        self.running = True

        # Start websocket in a separate thread with reconnection logic
        self.ws_thread = threading.Thread(
            target=self._websocket_thread,
            name="WebsocketThread",
            daemon=True,
        )
        self.ws_thread.start()

    def stop(self):
        """Stop the websocket connection."""
        if not self.running:
            return

        self.running = False

        # Close the websocket connection
        if self.ws:
            try:
                self.ws.close()
            except Exception as e:
                logger.debug(
                    "Maitai config listener: error closing websocket", exc_info=e
                )

        # Wait for the thread to finish
        if self.ws_thread and self.ws_thread.is_alive():
            self.ws_thread.join(timeout=2.0)

        self.ws = None
        self.ws_thread = None
