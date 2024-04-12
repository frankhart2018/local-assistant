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


@app.post("/prompt")
async def store_prompt(user_input: UserPromptInput):
    inserted_id = db_conn.insert_one(user_input.dict())

    return {"prompt_id": inserted_id}


@app.get("/stream-assistant/")
async def stream_assistant(prompt_id: str):
    async def event_generator():
        prompt = db_conn.find_by_id(prompt_id)

        for i, response in enumerate(
            ollama.generate(
                model=prompt["model"],
                system=prompt["system"],
                prompt=prompt["prompt"],
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
