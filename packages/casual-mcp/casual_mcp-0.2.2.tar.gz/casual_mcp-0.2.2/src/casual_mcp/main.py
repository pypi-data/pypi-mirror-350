import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from casual_mcp import McpToolChat
from casual_mcp.logging import configure_logging, get_logger
from casual_mcp.models.messages import ChatMessage
from casual_mcp.providers.provider_factory import ProviderFactory
from casual_mcp.utils import load_config, load_mcp_client, render_system_prompt

load_dotenv()
config = load_config("casual_mcp_config.json")
mcp_client = load_mcp_client(config)
provider_factory = ProviderFactory(mcp_client)

app = FastAPI()

default_system_prompt = """You are a helpful assistant.

You have access to up-to-date information through the tools, but you must never mention that tools were used.

Respond naturally and confidently, as if you already know all the facts.

**Never mention your knowledge cutoff, training data, or when you were last updated.**

You must not speculate or guess about dates — if a date is given to you by a tool, assume it is correct and respond accordingly without disclaimers.

Always present information as current and factual.
"""

class GenerateRequest(BaseModel):
    session_id: str | None = Field(
        default=None, title="Session to use"
    )
    model: str = Field(
        title="Model to user"
    )
    system_prompt: str | None = Field(
        default=None, title="System Prompt to use"
    )
    user_prompt: str = Field(
        title="User Prompt"
    )
    messages: list[ChatMessage] | None = Field(
        default=None, title="Previous messages to supply to the LLM"
    )

sys.path.append(str(Path(__file__).parent.resolve()))

# Configure logging
configure_logging(os.getenv("LOG_LEVEL", 'INFO'))
logger = get_logger("main")

async def perform_chat(
    model,
    user,
    system: str | None = None,
    messages: list[ChatMessage] = None,
    session_id: str | None = None
) -> list[ChatMessage]:
    # Get Provider from Model Config
    model_config = config.models[model]
    provider = await provider_factory.get_provider(model, model_config)

    if not system:
        if (model_config.template):
            async with mcp_client:
                system = render_system_prompt(
                    f"{model_config.template}.j2",
                    await mcp_client.list_tools()
                )
        else:
            system = default_system_prompt

    chat = McpToolChat(mcp_client, provider, system)
    return await chat.chat(
        prompt=user,
        messages=messages,
        session_id=session_id
    )


@app.post("/chat")
async def chat(req: GenerateRequest):
    messages = await perform_chat(
        req.model,
        system=req.system_prompt,
        user=req.user_prompt,
        messages=req.messages,
        session_id=req.session_id
    )

    return {
        "messages": messages,
        "response": messages[len(messages) - 1].content
    }


# This endpoint will either go away or be used for something else, don't use it
@app.post("/generate")
async def generate_response(req: GenerateRequest):
    return await chat(req)


@app.get("/chat/session/{session_id}")
async def get_chat_session(session_id):
    session = McpToolChat.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session
