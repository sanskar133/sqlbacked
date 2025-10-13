"""
This file contains the logic of the main application.
"""

import services
from flask import Flask, request  # type: ignore
from flask_socketio import Namespace, SocketIO  # type: ignore
from interface import WebsocketRequest
from settings import env
from utils.logger import logger_config

logger = logger_config(env.LOGGING_LEVEL)
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


class ChatNamespace(Namespace):
    """Chat space"""

    def on_connect(self):
        """On connect"""
        print("Client Connected to the socket")

    def on_message(self, data):
        """Handle incoming socket messages"""
        websocket_request = None
        try:
            websocket_request = WebsocketRequest(**data)
        except Exception as exc:
            # FIXED: send error back to the correct client session
            self.emit(
                "message",
                {
                    "status_code": 400,
                    "message": "Invalid request format",
                    "error_message": str(exc),
                },
                room=request.sid,
            )
            return

        print("Incoming:", data)

        try:
            if data.get("message") == "CONNECTED":
                services.handle_chat_connected(self, request.sid, websocket_request)

            elif data.get("message") == "DISCONNECTED":
                services.handle_chat_disconnected(self, request.sid, websocket_request)

            else:
                services.handle_incoming_message(self, request.sid, websocket_request)

        except Exception as exc:
            logger.error("Error while processing message", exc_info=True)
            self.emit(
                "message",
                {
                    "status_code": 500,
                    "message": "Internal server error",
                    "error_message": str(exc),
                },
                room=request.sid,
            )

    def on_disconnect(self):
        """Handle client disconnect"""
        print("Client Disconnected")


# Register namespace
socketio.on_namespace(ChatNamespace("/chat"))

if __name__ == "__main__":
    # import eventlet
    # import eventlet.wsgi
    socketio.run(app, port=5000, host="0.0.0.0", debug=False)
