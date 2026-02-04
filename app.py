"""FastAPI backend for the E-REDES Storm Kristin chatbot."""

import json
import logging
import os
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import AsyncOpenAI, BadRequestError
from pydantic import BaseModel

logger = logging.getLogger(__name__)

from config import GROQ_BASE_URL, GROQ_MODEL
from openai_tools import TOOLS, handle_tool_call
from system_prompt import SYSTEM_PROMPT

app = FastAPI(title="E-REDES Chatbot — Tempestade Kristin")

# ── Groq client (OpenAI-compatible) ─────────────────────────────────────────
client: AsyncOpenAI | None = None


@app.on_event("startup")
async def startup():
    global client
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        client = AsyncOpenAI(api_key=api_key, base_url=GROQ_BASE_URL)
    else:
        import logging
        logging.warning(
            "GROQ_API_KEY not set. Chat will not work until "
            "the key is provided via environment variable."
        )


# ── In-memory session store ─────────────────────────────────────────────────
sessions: dict[str, list[dict]] = {}
MAX_MESSAGES = 50


def get_session(session_id: str) -> list[dict]:
    if session_id not in sessions:
        sessions[session_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    return sessions[session_id]


def trim_session(messages: list[dict]) -> list[dict]:
    """Keep system prompt + last MAX_MESSAGES messages."""
    if len(messages) <= MAX_MESSAGES + 1:
        return messages
    return [messages[0]] + messages[-(MAX_MESSAGES):]


# ── Request / Response models ───────────────────────────────────────────────
class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    session_id: str


# ── Chat endpoint ───────────────────────────────────────────────────────────
@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if client is None:
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY não configurada. O servidor precisa da variável de ambiente GROQ_API_KEY.",
        )

    session_id = req.session_id or str(uuid.uuid4())
    messages = get_session(session_id)
    messages.append({"role": "user", "content": req.message})

    # Tool-call loop: keep going until the model returns text
    max_iterations = 10
    reply = ""
    try:
        for _ in range(max_iterations):
            try:
                response = await client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=messages,
                    tools=TOOLS,
                )
            except BadRequestError as e:
                if "tool_use_failed" in str(e):
                    # Model generated a malformed tool call — retry without tools
                    logger.warning("Tool call failed, retrying without tools: %s", e)
                    response = await client.chat.completions.create(
                        model=GROQ_MODEL,
                        messages=messages,
                    )
                else:
                    raise

            choice = response.choices[0]

            if choice.finish_reason == "tool_calls" or choice.message.tool_calls:
                # Append the assistant message with tool calls
                # Only include fields Groq supports (exclude 'annotations' etc.)
                assistant_msg = {
                    "role": "assistant",
                    "content": choice.message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in choice.message.tool_calls
                    ],
                }
                messages.append(assistant_msg)

                # Execute each tool call
                for tool_call in choice.message.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments)
                    result = await handle_tool_call(fn_name, fn_args)

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result,
                        }
                    )
            else:
                # Final text response
                reply = choice.message.content or ""
                messages.append({"role": "assistant", "content": reply})
                break
        else:
            reply = (
                "Peço desculpa, não consegui processar o seu pedido. "
                "Por favor, tente novamente ou contacte a Linha de Avarias: "
                "800 506 506."
            )
            messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        # Remove the user message since the call failed
        messages.pop()
        err_str = str(e)
        if "rate_limit" in err_str.lower() or "429" in err_str:
            raise HTTPException(
                status_code=429,
                detail="Limite de utilização da API atingido. Por favor, tente novamente dentro de alguns segundos.",
            )
        raise HTTPException(status_code=502, detail=f"Erro na API: {e}")

    # Trim session to avoid unbounded growth
    sessions[session_id] = trim_session(messages)

    return ChatResponse(reply=reply, session_id=session_id)


# ── Serve static frontend ───────────────────────────────────────────────────
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def index():
    return FileResponse(static_dir / "index.html")
