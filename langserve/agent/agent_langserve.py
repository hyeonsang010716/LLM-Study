from typing import Any, List, Union
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, FunctionMessage
from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from agent import agent_executor
from langserve import add_routes

# app 생성
app = FastAPI()


# We need to add these input/output schemas because the current AgentExecutor
# is lacking in schemas.
class Input(BaseModel):
    input: str
    # The field extra defines a chat widget.
    # Please see documentation about widgets in the main README.
    # The widget is used in the playground.
    # Keep in mind that playground support for agents is not great at the moment.
    # To get a better experience, you'll need to customize the streaming output
    # for now.
    chat_history: List[Union[HumanMessage, AIMessage, FunctionMessage]] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "input", "output": "output"}},
    )


class Output(BaseModel):
    output: Any

# @app.get("/")
# async def redirect_root_to_chat(): # root 대신 chat 화면으로 보내기
#     return RedirectResponse("/stream/playground")

# Adds routes to the app for using the chain under:
add_routes(
    app,
    agent_executor.with_types(input_type=Input, output_type=Output).with_config(
        {"run_name": "agent"}
    ),
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)