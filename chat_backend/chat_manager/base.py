import json
import logging
from datetime import datetime
import mlflow
from interface import WebsocketResponse
import os 
from dotenv import load_dotenv
logger = logging.getLogger(__name__)

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
        load_dotenv()
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
        mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_PATH"))


        # Prepare WebSocket response
        if _type == "INTERMEDIATE":
            websocket_response = WebsocketResponse(
                message=message,
                type=_type,
                query_id=query_id,
                status_code=status_code,
                error_message=error_message,
                data=data,
            )
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
        
        # if step_data:
        #     st = step_data[-1].step_id  # use last step id for run name
        #     with mlflow.start_run(run_name=f"Pipeline_Final_Step_Run:{st}"):
        #         steps_list = [
        #             {
        #             "step_id": s.step_id,
        #             "display_name": s.display_name,
        #             "message": s.message,
        #             "data": s.data,
        #             "time_taken": s.time_taken,
        #             "error_message": s.error_message,
        #             }
        #             for s in step_data
        #         ]
        #         mlflow.log_dict({"step_data": steps_list}, "step_data.json")
        #         mlflow.log_param("final_step_id", step_data[-1].step_id)
        #         mlflow.log_param("final_step_message", step_data[-1].message)
        print(type(step_data))
        for s in step_data or []:
            print(s.step_id, s.message)
            mlflow.start_run(run_name=f"Pipeline_Step_Run:{s.step_id} {query_id}")
            mlflow.log_param("step_id", s.step_id)
            mlflow.log_param("display_name", s.display_name)
            mlflow.log_param("message", s.message)
            mlflow.log_dict(s.data, "data.json")
            mlflow.end_run()
            

        # Send over WebSocket
        websocket_response_dict = json.loads(websocket_response.json())
        logger.info("Emitting Websocket from Chat Manager")
        self.websocket_object.emit("message", websocket_response_dict, self.websocket_id)

    def run(self, websocket_request, query_id):
        raise NotImplementedError("Please implement your pipeline in this method.")

    def run_query(self, websocket_request, query_id):
        start_time = datetime.now()
        self.send_message(_type="INTERMEDIATE", message="Started Processing", query_id=query_id)

        try:
            self.run(websocket_request, query_id)
        except Exception as exc:
            logger.error("Error processing user query: %s %s", query_id, str(exc), exc_info=True)
            self.send_message(
                _type="FINAL",
                error_message="An error occurred while processing the request.",
                query_id=query_id,
                status_code=400,
            )