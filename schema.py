from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator

def get_current_datetime():
    """get current datetime"""
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    today = datetime.today()
    weekday_dict = {0: "Monday", 1: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    weekday = weekday_dict[today.weekday()]
    today_str = f"{time} - {weekday}, {today.year} - {today.month} - {today.day}"
    return today_str

class ChatRequestMemory(BaseModel):
    query: str
    knox_id: str | None = None
    user_name: str | None = None
    isDebugOn: Optional[bool] = False
    history: Optional[list[dict]] = []

    @field_validator('query', 'knox_id')
    def not_empty(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.field_name} field does not allow empty values.")
        return v

class ChatResponseMemory(BaseModel):
    answer: str
    messages: list = []
    debug_info: dict | None = None

    @field_validator('answer')
    def not_empty(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.field_name} field does not allow empty values.")
        return v