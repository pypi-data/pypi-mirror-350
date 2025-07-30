from pydantic import BaseModel
from typing import Literal, Optional

class CommonResponse(BaseModel):
    status: Literal["success", "error"]
    type: str
    command_id: str
    payload: dict
    error: Optional[dict] = None