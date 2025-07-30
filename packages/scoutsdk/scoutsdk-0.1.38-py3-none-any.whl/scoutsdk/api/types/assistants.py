from pydantic import BaseModel


class AssistantResponse(BaseModel):
    message: str
    assistant_id: str
