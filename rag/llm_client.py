"""Thin client for FREE OpenAI-compatible providers. Plain code — no frameworks.

Roles are separated so judge model != generation model (see docs/evals.md):
  - generator: Gemini free tier (primary)
  - judge:     Groq free tier (different family — reduces self-preference bias)

Verified 2026-07-07 (web check; re-verify numbers in your own console after signup):
  - Groq free: no card needed; llama-3.3-70b-versatile ≈ 30 RPM / 1,000 RPD /
    12K TPM / 100K TPD. TPD is the binding constraint for judge suites →
    keep judge prompts lean + cache results (docs/evals.md).
  - Gemini free: no card; exact limits are PER-PROJECT — check the rate-limit
    page in AI Studio after creating your key. Model line-up shifts (3.x line
    exists); pick the current free Flash-class id in AI Studio if 2.5-flash
    is retired. Free-tier prompts may be used for training → fine for public
    legal text, never for private data.
"""
from openai import OpenAI

from config import settings

_PROVIDERS = {
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "key": lambda: settings.gemini_api_key,
        "default_model": "gemini-2.5-flash",  # UNVERIFIED: confirm current free-tier model id
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key": lambda: settings.groq_api_key,
        "default_model": "llama-3.3-70b-versatile",  # UNVERIFIED
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "key": lambda: settings.openrouter_api_key,
        "default_model": None,  # pick a :free model explicitly at call time
    },
}


def client(provider: str) -> OpenAI:
    p = _PROVIDERS[provider]
    key = p["key"]()
    if not key:
        raise RuntimeError(f"No API key configured for provider '{provider}' (see .env.example)")
    return OpenAI(base_url=p["base_url"], api_key=key)


def default_model(provider: str) -> str | None:
    return _PROVIDERS[provider]["default_model"]
