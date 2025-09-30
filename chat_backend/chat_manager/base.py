import json
import logging
from datetime import datetime

from interface import WebsocketResponse

logger = logging.getLogger(__name__)
"""
TODO
1. Gracefully del connection engines
"""


class ChatManager:
    def __init__(self, database_object, websocket_object, socket_id):
        logger.info("Initializing base chat manager")
        self.database_object = database_object
        self.websocket_object = websocket_object
        self.websocket_id = socket_id

        self.initialized_pipeline = []

    def send_message(
        self,
        _type,
        message=None,
        error_message=None,
        data={},
        query_id=None,
        step_data=None,
        status_code=200,
    ):
        # TODO Update the time taken here while updating query. 2. Jugad of json dumop and load

        if _type == "INTERMEDIATE":
            websocket_response = WebsocketResponse(
                message=message,
                type=_type,
                query_id=query_id,
                status_code=status_code,
                error_message=error_message,
                data=data,
            )
            websocket_response = json.loads(websocket_response.json())

        else:
            websocket_response = WebsocketResponse(
                message=message,
                data=data,
                type=_type,
                query_id=query_id,
                step_data=step_data,
                status_code=status_code,
                error_message=error_message,
            )
            websocket_response = json.loads(websocket_response.json())

        logger.info("Emitting Websocket from Chat Manager")
        self.websocket_object.emit("message", websocket_response, self.websocket_id)

    def run():
        NotImplementedError()

    def run_query(self, websocket_request, query_id):
        """TODO
        1. Test behaviour with mulitple connects
        """
        start_time = datetime.now()
        self.send_message(
            _type="INTERMEDIATE", message="Started Processing", query_id=query_id
        )

        try:
            self.run(websocket_request, query_id)
        except Exception as exc:
            logger.info(
                "Error in processign user query: %s %s",
                query_id,
                str(exc),
                exc_info=True,
            )
            self.send_message(
                _type="FINAL",
                error_message="An error occurred while processing the request.",
                query_id=query_id,
                status_code=400,
            )
