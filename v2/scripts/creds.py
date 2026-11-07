"""Relay credentials, taken from environment variables.

The original working copy read them from text files on the desktop; for the
public release everything is env-based so no secrets can leak.

Set (all optional, only the stage you run needs them):

    SHINKAI_IMAGE_BASE_URL   / SHINKAI_IMAGE_API_KEY    # image generation relay
    SHINKAI_GPT_BASE_URL     / SHINKAI_GPT_API_KEY      # QA / vision relay
    SHINKAI_GEMINI_BASE_URL  / SHINKAI_GEMINI_API_KEY   # tie-break only

A base URL may be given with or without the trailing /v1.
"""

import os


def _pair(prefix):
    base = os.environ.get(prefix + "_BASE_URL", "").strip().rstrip("/")
    key = os.environ.get(prefix + "_API_KEY", "").strip()
    if base and not base.endswith("/v1"):
        base += "/v1"
    return base, key


IMAGE = _pair("SHINKAI_IMAGE")
GPT = _pair("SHINKAI_GPT")
GEMINI = _pair("SHINKAI_GEMINI")

IMAGE_MODELS = {"gpt-image-2.6-sunburst", "gpt-image-2"}
GPT_MODELS = {"gpt-6.1-sol"}
GEMINI_MODELS = {"gemini-3.8-flash"}


def guard(model, allowed):
    if model not in allowed:
        raise ValueError(f"model {model!r} not allowed here (allowed: {sorted(allowed)})")
