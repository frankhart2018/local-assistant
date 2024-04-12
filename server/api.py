import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import uvicorn
from pydantic import BaseModel
import ollama


logger = logging.getLogger()

MESSAGE_STREAM_DELAY = 1
MESSAGE_STREAM_RETRY_TIMEOUT = 15000
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StreamAssistantInput(BaseModel):
    model: str
    prompt: str
    system: str


@app.post("/stream-assistant")
async def stream_assistant(payload: StreamAssistantInput):
    async def event_generator():
        for i, response in enumerate(
            ollama.generate(
                model=payload.model,
                system=payload.system,
                prompt=payload.prompt,
                stream=True,
            )
        ):
            response_val = response["response"]
            done = response["done"]
            if not done:
                yield {
                    "event": "new_message",
                    "id": i,
                    "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
                    "data": response_val,
                }
            else:
                yield {
                    "event": "end_event",
                    "id": i,
                    "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
                    "data": "End",
                }

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
