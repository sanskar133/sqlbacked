import logging
import time
from typing import Dict

from chat_manager import ChatManagerV5 as ChatManager
from databases import utils as database_connection_management_utils
from interface import WebsocketRequest, WebsocketResponse
from settings import env
from utils.commons import authenticate


# TODO Later to be moved to a db or cache
CHAT_ID_TO_MANAGER_MAPPING: Dict[str, ChatManager] = {}

logger = logging.getLogger(__name__)


def handle_chat_connected(
    socket_object, socket_id, websocket_request: WebsocketRequest
):
    """Handle Chat Connected
    TODO:
        1. Add validation to check if all ids and relations are valid
        2. Move creating response entry to rabbitmq
    """

    try:
        print("Handling Chat Connected Message", socket_id, websocket_request)

        start_time = time.time()

        # Get connection metadata
        connection_metadata = env.CONNECTION_META_DATA[websocket_request.user_id]
        connection_type = "STANDARD"

        print("CREATInG DB OBJ!")

        # Cache The Chat Id and Connection
        database_object = database_connection_management_utils.get_database_object(
            connection_metadata["database_type"],
            connection_metadata["database_meta_data"],
            connection_type=connection_type,
        )
        print("DONE DB OBJ!")

        CHAT_ID_TO_MANAGER_MAPPING[websocket_request.chat_session_id] = ChatManager(
            database_object,
            socket_object,
            socket_id,
        )
        print("CHATSESSIONIDS:", CHAT_ID_TO_MANAGER_MAPPING.keys())

        # Send out a response
        websocket_response = WebsocketResponse(
            message="CONNECTION INITIALIZED SUCCESSFULLY",
        )
        socket_object.emit("message", websocket_response.dict(), socket_id)

    except Exception as exc:
        logger.error(str(exc), exc_info=True)

        websocket_response = WebsocketResponse(
            status_code=400,
            message="Error in handling websocket connection: ",
            error_message=str(exc),
        )
        socket_object.emit("message", websocket_response.dict(), socket_id)


def handle_chat_disconnected(
    socket_object, socket_id, websocket_request: WebsocketRequest
):
    """Handle Chat Disconnected
    TODO:
        1. Add validation to check if all ids and relations are valid
        2. Move creating response entry to rabbitmq
    """

    try:
        print("Handling Chat Connected Message", socket_id, websocket_request)

        start_time = time.time()

        # Get connection metadata
        if websocket_request.chat_session_id in CHAT_ID_TO_MANAGER_MAPPING:
            del CHAT_ID_TO_MANAGER_MAPPING[websocket_request.chat_session_id]

        # Send out a response
        websocket_response = WebsocketResponse(message="DISCONNECTED SUCCESSFULLY")
        socket_object.emit("message", websocket_response.dict(), socket_id)

    except Exception as exc:
        logger.error(str(exc), exc_info=True)

        websocket_response = WebsocketResponse(
            status_code=400,
            message="Error in handling websocket connection: ",
            error_message=str(exc),
        )
        socket_object.emit("message", websocket_response.dict(), socket_id)


def handle_incoming_message(
    socket_object, socket_id, websocket_request: WebsocketRequest
):
    """Handle Chat Connected"""
    try:
        print("Handling Incoming Message", socket_id, websocket_request)

        print("CHATSESSIONIDS:", CHAT_ID_TO_MANAGER_MAPPING.keys())

        if websocket_request.chat_session_id in CHAT_ID_TO_MANAGER_MAPPING:
            chat_manager = CHAT_ID_TO_MANAGER_MAPPING[websocket_request.chat_session_id]

            print("Checking for valid authentication")

            status, msg = True,"authentication succesfull"
            if not status:
                websocket_response = WebsocketResponse(message=msg, status_code=500)
                socket_object.emit("message", websocket_response.dict(), socket_id)
            else:
                # TODO: log user questions
                import uuid

                response = chat_manager.run_query(websocket_request, str(uuid.uuid4()))
                socket_object.emit("message", response, socket_id)

        else:
            print("Corresponding Chat ID Does Not Exist")
            websocket_response = WebsocketResponse(message="Invalid Chat Id.")
            socket_object.emit("message", websocket_response.dict(), socket_id)
            print("Event emitited")
            # socket_object.disconnect(socket_id)

    except Exception as exc:
        logger.error(str(exc), exc_info=True)

        websocket_response = WebsocketResponse(
            status_code=400,
            message="Error in handling incoming user message : ",
            error_message=str(exc),
        )
        socket_object.emit("message", websocket_response.dict(), socket_id)
