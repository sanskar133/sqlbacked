from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class WebsocketRequest(BaseModel):
    chat_session_id: str
    user_id: str
    # database_connection_id: str = None
    request_type: str = None
    message: str
    history: list


class StepData(BaseModel):
    step_id: int
    display_name: str
    message: Union[Optional[str], Optional[list[str]]] = None
    error_message: Optional[str] = None
    data: Union[dict, List[dict]] = []
    time_taken: float


class WebsocketResponse(BaseModel):
    query_id: Optional[str] = None
    message: Union[Optional[str], Optional[list[str]]] = None
    status_code: int = 200
    error_message: Optional[str] = None
    data: Union[dict, List[dict]] = []
    step_data: list[StepData] = []
    type: str = "NORMAL"

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),  # or any other format you prefer
            Decimal: lambda v: str(v),
            date: lambda v: str(v),
        }
