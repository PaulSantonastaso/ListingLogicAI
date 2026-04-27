"""
compliance_tool_service.py

Fair Housing Compliance Checker — free lead gen tool.
Validates input, pre-screens with Flash Lite, runs compliance chain.
"""

import logging
import os
import re

from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)

REAL_ESTATE_KEYWORDS = [
    "bedroom", "bathroom", "kitchen", "living room", "garage", "sqft",
    "square feet", "property", "home", "house", "listing", "mls", "agent",
    "realtor", "backyard", "patio", "pool", "floor", "ceiling", "closet",
    "laundry", "dining", "master", "primary", "suite", "condo", "townhouse",
    "neighborhood", "community", "lot", "acre", "price", "offer",
]

MAX_INPUT_LENGTH = 2000
TOOL_RUN_LIMIT = 3
TOOL_TTL = 604800  # 7 days


def _tool_compliance_key(ip: str) -> str:
    return f"tool:compliance:{ip}"


def _tool_email_key(ip: str) -> str:
    return f"tool:email:{ip}"


def _has_real_estate_keywords(text: str) -> bool:
    text_lower = text.lower()
    return any(kw in text_lower for kw in REAL_ESTATE_KEYWORDS)


async def pre_screen_compliance_input(text: str, api_key: str) -> bool:
    """
    Flash Lite pre-screen — is this a real estate listing description?
    Returns True if it passes, False if it should be rejected.
    Fast-path: keyword check first, LLM only if ambiguous.
    """
    # Fast path — obvious real estate content
    if _has_real_estate_keywords(text):
        return True

    # Ambiguous — use Flash Lite for classification
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite",
            temperature=0,
            max_output_tokens=1,
            google_api_key=api_key,
        )
        prompt = (
            "Is the following text a real estate listing description? "
            "Reply YES or NO only.\n\n"
            f"{text[:500]}"
        )
        result = await llm.ainvoke(prompt)
        content = result.content
        if isinstance(content, list):
            content = content[0] if content else ""
        if isinstance(content, dict):
            content = content.get("text", "")
        answer = str(content).strip().upper()
        return answer == "YES"
    except Exception as e:
        logger.error(f"[COMPLIANCE TOOL] Pre-screen failed: {e}")
        # Fail open — don't block on LLM error
        return True


def check_ip_gate(ip: str, email: str | None, redis_client) -> dict:
    """
    Check if IP has exceeded free run limit.
    Returns {"allowed": bool, "runs_used": int, "email_on_file": bool}
    """
    key = _tool_compliance_key(ip)
    email_key = _tool_email_key(ip)

    raw_count = redis_client.get(key)
    runs_used = int(raw_count) if raw_count else 0
    email_on_file = redis_client.get(email_key) is not None

    # If email provided, store it and allow
    if email and not email_on_file:
        redis_client.setex(email_key, TOOL_TTL, email.encode())
        email_on_file = True

    allowed = runs_used < TOOL_RUN_LIMIT or email_on_file

    return {
        "allowed": allowed,
        "runs_used": runs_used,
        "email_on_file": email_on_file,
    }


def increment_run_count(ip: str, redis_client) -> None:
    key = _tool_compliance_key(ip)
    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.expire(key, TOOL_TTL)
    pipe.execute()