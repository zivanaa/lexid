"""Thin client for FREE OpenAI-compatible providers. Plain code — no frameworks.

Roles are separated so judge model != generation model (see docs/evals.md).
Assignment based on the owner's MEASURED per-project free limits (2026-07-07):
  - generator (daily dev):   Gemini 3.1 Flash Lite  — 15 RPM / 500 RPD
  - generator (final/demo):  Groq Llama-3.3-70B     — 100K tokens/DAY binds
  - judge:                   Gemma 4 26B (Gemini API) — 15 RPM / 1,500 RPD /
                             unlimited TPM; different family from both generators

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
        "default_model": "gemini-3.1-flash-lite",  # confirm exact API id via ListModels; console shows this tier at 500 RPD
        "judge_model": "gemma-4-26b",  # confirm exact API id; 1.5K RPD / unlimited TPM in owner console
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key": lambda: settings.groq_api_key,
        "default_model": "llama-3.3-70b-versatile",  # confirmed in console: 131K ctx, 32K max out, JSON mode
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


def judge_model(provider: str) -> str | None:
    """Judge model for a provider (must be a different family than the generator).
    Gemini API serves Gemma here — same key, different family from Gemini/Llama."""
    return _PROVIDERS[provider].get("judge_model")
