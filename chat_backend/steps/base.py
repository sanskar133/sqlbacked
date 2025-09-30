import logging
from datetime import datetime

from custom_exceptions.ProceedFalseException import (
    ProceedFalseException,
)
from interface import StepData

logger = logging.getLogger(__name__)


class Step:
    START_MESSAGE = "Starting"
    END_MESSAGE = "Ended"
    ERROR_MESSAGE = "Error"

    query_id = None

    def __init__(self, step_number, chat_manager):
        self.chat_manager = chat_manager
        self.step_number = step_number

    def input_keys(self):
        pass

    def output_keys(self):
        pass

    def run(self, query_id, benchmark, **kwargs):
        logger.info(f"Running step {self} for query id {query_id}")

        # set the query id as an instance variable
        self.query_id = query_id

        # fn logic
        start_time = datetime.now()
        if not benchmark:
            self.chat_manager.send_message(
                _type="INTERMEDIATE", message=f"{self.START_MESSAGE}", query_id=query_id
            )

        output, message, error_message = {}, None, None
        try:
            output = self(**kwargs)
            message = f"{self.END_MESSAGE}"
        except Exception as exc:
            logger.error(str(exc), exc_info=True)
            error_message = f"{self.ERROR_MESSAGE}"

        time_taken = (datetime.now() - start_time).total_seconds()
        step_data = StepData(
            step_id=self.step_number,
            display_name=str(self),
            message=message,
            error_message=error_message,
            time_taken=time_taken,
            data=output,
        )

        if not benchmark:
            self.chat_manager.send_message(
                _type="INTERMEDIATE", message=message, query_id=query_id, data=output
            )

        if "proceed" in output and not output["proceed"]:
            raise ProceedFalseException("Cannot Execute Query", output, step_data)

        return output, step_data
