import logging
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import ollama

from models.user_prompt_input import UserPromptInput
from utils.mongo_connection import MongoDB


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
db_conn = MongoDB(collection="prompts")

prompts = [
    {
        "model": "codegemma",
        "system": "You are an expert coder, but you do not write comments, no documentation. Do not include the python start and end tags",
        "prompt": "Write a FastAPI endpoint to serve a SSE that returns numbers from 1 to 100 after 1 second",
    },
    {
        "model": "codegemma",
        "system": "You are an expert coder, but you do not write comments, no documentation. Do not include the python start and end tags",
        "prompt": "Write a python function to add two numbers",
    },
]


@app.post("/prompt")
async def store_prompt(user_input: UserPromptInput):
    inserted_id = db_conn.insert_one(user_input.dict())

    return {"prompt_id": inserted_id}


@app.get("/stream-assistant/")
async def stream_assistant(id: int):
    async def event_generator():
        for i, response in enumerate(
            ollama.generate(
                model=prompts[id]["model"],
                system=prompts[id]["system"],
                prompt=prompts[id]["prompt"],
                stream=True,
                template="""<start_of_turn>user
{{ if .System }}{{ .System }} {{ end }}{{ .Prompt }}<end_of_turn>
<start_of_turn>model
{{ .Response }}<end_of_turn>""",
            )
        ):
            response_val = response["response"].replace("\n", "<NEWLINE>")
            done = response["done"]
            if not done:
                yield f"id: {i}\n\ndata: {response_val}\n\n"
            else:
                yield f"id: {i}\n\ndata: END\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
