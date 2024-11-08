import time
import uuid

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Union

from pychatgpt import ChatGPT

app = FastAPI()
chat = None

class RequestBody(BaseModel):
    model: str
    prompt: str

class Message(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    message: Message
    index: int
    logprobs: Optional[Union[None, dict, float]]  # Assuming logprobs can be None, dict, or float
    finish_reason: str

class OpenAIResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Dict[str, int]

@app.on_event("startup")
async def startup():
    global chat
    chat = ChatGPT(headless=False)
    print("Initialization DONE.", flush=True)

@app.post("/v1/chat/completions", response_model=OpenAIResponse)
async def generate_response(request: RequestBody):
    global chat

    res = chat.predict(request.prompt)
    response = {
        "id": str(uuid.uuid4()),
        "object": "text_completion",
        "created": int(time.time()),  # A mock timestamp
        "model": request.model,
        "choices": [{
            "message": {
                "role": "assistant",
                "content": res["response"]
            },
            "index": 0,
            "logprobs": None,
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": len(request.prompt.split()),
            "completion_tokens": len(res["response"].split()),
            "total_tokens": len(request.prompt.split()) + len(res["response"].split())
        }
    }
    
    return response
