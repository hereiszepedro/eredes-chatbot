"""FastAPI backend for the E-REDES Storm Kristin chatbot."""

import asyncio
import json
import logging
import os
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from openai import AsyncOpenAI, BadRequestError
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

logger = logging.getLogger(__name__)

from config import GROQ_BASE_URL, GROQ_MODEL
from openai_tools import TOOLS, handle_tool_call
from system_prompt import SYSTEM_PROMPT

CHAT_TIMEOUT_SECONDS = 60

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="E-REDES Chatbot — Tempestade Kristin")
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Limite de pedidos atingido. Por favor, aguarde um momento antes de tentar novamente."
        },
    )


# ── CORS middleware ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── Groq client (OpenAI-compatible) ─────────────────────────────────────────
client: AsyncOpenAI | None = None


@app.on_event("startup")
async def startup():
    global client
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        client = AsyncOpenAI(api_key=api_key, base_url=GROQ_BASE_URL)
    else:
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
    session_id: str = Field(..., pattern=r"^[a-zA-Z0-9_-]{1,100}$")
    message: str = Field(..., max_length=2000)


class ChatResponse(BaseModel):
    reply: str
    session_id: str


# ── Chat endpoint ───────────────────────────────────────────────────────────
@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(request: Request, req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

    if client is None:
        raise HTTPException(
            status_code=503,
            detail="Serviço temporariamente indisponível. Por favor, tente mais tarde.",
        )

    session_id = req.session_id or str(uuid.uuid4())
    messages = get_session(session_id)
    messages.append({"role": "user", "content": req.message})

    try:
        reply = await asyncio.wait_for(
            _process_chat(messages),
            timeout=CHAT_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError:
        messages.pop()
        raise HTTPException(
            status_code=504,
            detail="O pedido demorou demasiado tempo. Por favor, tente novamente.",
        )
    except Exception as e:
        # Remove the user message since the call failed
        messages.pop()
        err_str = str(e)
        if "rate_limit" in err_str.lower() or "429" in err_str:
            raise HTTPException(
                status_code=429,
                detail="Limite de utilização atingido. Por favor, tente novamente dentro de alguns segundos.",
            )
        logger.error("Chat processing error: %s", e)
        raise HTTPException(
            status_code=502,
            detail="Erro interno do serviço. Por favor, tente novamente.",
        )

    # Trim session to avoid unbounded growth
    sessions[session_id] = trim_session(messages)

    return ChatResponse(reply=reply, session_id=session_id)


async def _process_chat(messages: list[dict]) -> str:
    """Run the tool-call loop and return the final reply text."""
    max_iterations = 10
    reply = ""

    for _ in range(max_iterations):
        try:
            response = await client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                tools=TOOLS,
            )
        except BadRequestError as e:
            if "tool_use_failed" in str(e):
                logger.warning("Tool call failed, retrying without tools: %s", e)
                response = await client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=messages,
                )
            else:
                raise

        choice = response.choices[0]

        if choice.finish_reason == "tool_calls" or choice.message.tool_calls:
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

    return reply


# ── Serve static frontend ───────────────────────────────────────────────────
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def index():
    return FileResponse(static_dir / "index.html")
