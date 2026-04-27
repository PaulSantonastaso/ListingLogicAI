"""
neighborhood_tool_service.py

Neighborhood Guide Generator — free lead gen tool.
Uses existing geocoding + Places API + neighborhood chain.
Geocoding failure is the input guard — no LLM pre-screen needed.
"""

import logging

logger = logging.getLogger(__name__)

MAX_INPUT_LENGTH = 200
TOOL_RUN_LIMIT = 3
TOOL_TTL = 604800  # 7 days


def _tool_neighborhood_key(ip: str) -> str:
    return f"tool:neighborhood:{ip}"


def _tool_email_key(ip: str) -> str:
    return f"tool:email:{ip}"


def check_ip_gate(ip: str, email: str | None, redis_client) -> dict:
    """
    Check if IP has exceeded free run limit.
    Returns {"allowed": bool, "runs_used": int, "email_on_file": bool}
    """
    key = _tool_neighborhood_key(ip)
    email_key = _tool_email_key(ip)

    raw_count = redis_client.get(key)
    runs_used = int(raw_count) if raw_count else 0
    email_on_file = redis_client.get(email_key) is not None

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
    key = _tool_neighborhood_key(ip)
    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.expire(key, TOOL_TTL)
    pipe.execute()