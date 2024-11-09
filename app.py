import time
import uuid

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Union

from pychatgpt import ChatGPT

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class RequestBody(BaseModel):
    messages: List[Message]
    model: str
    response_format: Dict[str, str]

class Choice(BaseModel):
    message: Message
    index: int
    logprobs: Optional[Union[None, dict, float]]
    finish_reason: str

class OpenAIResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Dict[str, int]

@app.post("/v1/chat/completions", response_model=OpenAIResponse)
async def generate_response(request: RequestBody):
    chat = ChatGPT(headless=True, uc_driver=True)

    prompt = "\n".join([msg.content for msg in request.messages])
    if request.response_format["type"] == "json_object":
        prompt += "\n\nYour response should be in json format ONLY and rendered in text form!"
    # print(f"\nprompt:\n{prompt}", flush=True)

    result = chat.predict(prompt)

    response_text = "\n".join([x["content"] for x in result["response"]])
    response_text = "{" + "{".join(response_text.split("{")[1:])
    print("\nresponse_text:")
    print(response_text)

    response = {
        "id": str(uuid.uuid4()),
        "object": "text_completion",
        "created": int(time.time()),  # A mock timestamp
        "model": request.model,
        "choices": [{
            "message": {
                "role": "assistant",
                "content": response_text
            },
            "index": 0,
            "logprobs": None,
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(response_text.split()),
            "total_tokens": len(prompt.split()) + len(response_text.split())
        }
    }
    
    return response
