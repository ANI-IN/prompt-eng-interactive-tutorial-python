"""Thin wrapper around the Anthropic Messages API used by every chapter.

The API key is read from the ``ANTHROPIC_API_KEY`` environment variable. A
``.env`` file in the project root (one level up from this ``lib/`` folder) is
loaded first, so the key is found no matter which directory the Jupyter kernel
runs in. A variable that is already set in the environment wins over ``.env``.

Never hardcode your key in a notebook or commit your ``.env`` file.
"""

import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

# override=False: an ANTHROPIC_API_KEY already exported in your shell (or set as
# a Codespaces secret) takes precedence over the value in .env.
load_dotenv(ENV_PATH, override=False)

# The pinned model. Override it without touching code by setting CLAUDE_MODEL
# in your .env file, e.g. CLAUDE_MODEL=claude-sonnet-5-5
MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")

# Room for Claude's internal reasoning plus the visible answer. Current models
# think before answering, and thinking tokens count toward max_tokens.
MAX_TOKENS = 16000

# Current Claude models (Opus 5.5, Sonnet 5.5, ...) do not accept sampling
# parameters such as temperature, and the 1.x Python SDK no longer has a
# `temperature=` keyword. Older models still honour it, so for those we send
# temperature=0 through `extra_body` to make runs as repeatable as possible.
# Pass **SAMPLING_PARAMS to any direct client.messages.create(...) call.
_TEMPERATURE_MODELS = (
    "claude-sonnet-4-6",
    "claude-sonnet-4-5",
    "claude-opus-4-6",
    "claude-opus-4-5",
    "claude-haiku-4-5",
)
SAMPLING_PARAMS = {"extra_body": {"temperature": 0}} if MODEL in _TEMPERATURE_MODELS else {}


def api_key_configured() -> bool:
    """Return True if an API key is visible to this kernel (never prints the key)."""
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


if not api_key_configured():
    print(
        "WARNING: ANTHROPIC_API_KEY is not set.\n"
        f"  Copy .env.example to {ENV_PATH} and add your key, then RESTART the kernel."
    )

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


REFUSAL_MARKER = "WARNING: Claude declined this request"


def response_text(message) -> str:
    """Join the text blocks of a Messages API response.

    A response's ``content`` is a list of blocks. Besides ``text`` blocks it can
    hold ``thinking`` or ``tool_use`` blocks, so never assume ``content[0]`` is
    the text you want.

    If Claude declined the request (``stop_reason == "refusal"``) a warning is
    printed, so an empty answer is never mistaken for a real one.
    """
    if message.stop_reason == "refusal":
        details = getattr(message, "stop_details", None)
        category = getattr(details, "category", None)
        print(f"{REFUSAL_MARKER} (stop_reason='refusal', category={category!r}). Rephrase the prompt.")
    return "".join(block.text for block in message.content if block.type == "text")


PLACEHOLDER_MARKERS = ("[Replace this text", "[Build your prompt here")


def has_placeholder(*texts: str) -> bool:
    """True if any text still contains an unfilled exercise placeholder."""
    return any(marker in (text or "") for text in texts for marker in PLACEHOLDER_MARKERS)


def get_completion(prompt: str, system: str = "") -> str:
    """Send a single-turn prompt to Claude and return the text of the response.

    If the prompt or system prompt still contains an exercise placeholder such
    as "[Replace this text]", no API call is made: a reminder is printed and an
    empty string is returned, so an unsolved exercise grades False for free.

    Args:
        prompt: the user message.
        system: optional system prompt ("" means no system prompt).
    """
    if has_placeholder(prompt, system):
        print("Replace the placeholder text in this cell with your own prompt, then run it again.")
        return ""
    params = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}],
        **SAMPLING_PARAMS,
    }
    if system:
        params["system"] = system
    message = client.messages.create(**params)
    return response_text(message)
