from typing import List, Literal, Optional, Union

import uvicorn
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: Optional[str] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage


class ChatCompletionResponse(BaseModel):
    model: str
    object: Literal["chat.completion"]
    choices: List[Union[ChatCompletionResponseChoice]]


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]


@app.get("/health")
async def health() -> Response:
    return Response(status_code=200)


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest):
    print(f"request: {request}")

    if len(request.messages) < 1 or request.messages[-1].role == "assistant":
        raise HTTPException(status_code=400, detail="Invalid request")

    return ChatCompletionResponse(
        model=request.model,
        choices=[ChatCompletionResponseChoice(
            index=0,
            message=ChatMessage(
                role="assistant",
                content="just a joke",
            ),
        )],
        object="chat.completion",
    )


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
