from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from typing import List, Union # 변수 형태를 가시적으로 보여줌
from chain import chain

# API 불러오기
app = FastAPI()
# CORS 설정
app.add_middleware(  
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
# root를 호출하였을때
@app.get("/")
async def redirect_root_to_chat(): # root 대신 chat 화면으로 보내기
    return RedirectResponse("/prompt/playground")
add_routes(app, chain, path="/prompt")

class InputChat(BaseModel):
    """Input for the chat endpoint."""

    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )

add_routes(
    app,
    chain.with_types(input_type=InputChat),
    path="/chat",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
    playground_type="chat",
)

if __name__ == "__main__":
    import uvicorn # uvicorn으로 app 실행

    uvicorn.run(app, host="localhost", port=8000) # 로컬로 호스팅