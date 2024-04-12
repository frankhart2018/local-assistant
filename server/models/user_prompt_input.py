from pydantic import BaseModel


class UserPromptInput(BaseModel):
    model: str
    prompt: str
    system: str
