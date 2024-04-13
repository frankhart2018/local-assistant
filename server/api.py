import logging
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import ollama
import asyncio

from models.user_prompt_input import UserPromptInput
from utils.mongo_connection import MongoDB
from utils.dict_utils import safe_dict_get


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


@app.get("/list-models")
async def list_models():
    model_list = [
        {
            "name": safe_dict_get(
                dictionary=model, keys=["name"], default_value=""
            ).split(":")[0],
            "parameters": safe_dict_get(
                dictionary=model,
                keys=["details", "parameter_size"],
                default_value="",
            ),
        }
        for model in ollama.list().get("models", {})
    ]

    return model_list


@app.post("/prompt")
async def store_prompt(user_input: UserPromptInput):
    inserted_id = db_conn.insert_one(user_input.dict())

    return {"prompt_id": inserted_id}


@app.get("/stream-assistant/")
async def stream_assistant(prompt_id: str):
    async def event_generator():
        prompt = db_conn.find_by_id(prompt_id)

        try:
            for i, response in enumerate(
                ollama.generate(
                    model=prompt["model"],
                    system=prompt["system"],
                    prompt=prompt["prompt"],
                    stream=True,
                    template=ollama.show(prompt["model"])["template"],
                )
            ):
                response_val = response["response"].replace("\n", "<NEWLINE>")
                done = response["done"]
                if not done:
                    yield f"id: {i}\n\ndata: {response_val}\n\n"
                else:
                    yield f"id: {i}\n\ndata: END\n\n"
                await asyncio.sleep(0)  # this is to handle abrupt client termination
        except asyncio.CancelledError:
            logger.error("ERROR: Client disconnected, stopping generation.")

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
