"""Thin OpenRouter chat-completions client with retries and full response logging."""
from __future__ import annotations
import os
import time
import random
import requests
from dotenv import load_dotenv

API_URL = "https://openrouter.ai/api/v1/chat/completions"
_FATAL = ("400", "401", "402", "403", "404")


class OpenRouterError(RuntimeError):
    pass


def api_key() -> str:
    """Key from the environment, or from .env (KEY=value, or a bare key on one line; BOM tolerated)."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        from pathlib import Path
        env_path = Path(__file__).resolve().parent.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path, encoding="utf-8-sig")
            key = os.environ.get("OPENROUTER_API_KEY")
            if not key:
                raw = env_path.read_text(encoding="utf-8-sig").strip()
                if raw.startswith("sk-or-") and "=" not in raw and "\n" not in raw:
                    key = raw
    if not key:
        raise OpenRouterError("OPENROUTER_API_KEY is not set (copy .env.example to .env)")
    return key


def chat(model: str, messages: list[dict], *, temperature: float = 0.7, max_tokens: int = 1800,
         reasoning: dict | None = None, seed: int | None = None, max_retries: int = 5,
         timeout: int = 180, extra: dict | None = None) -> dict:
    """Return the raw JSON of a successful completion.

    Retries on 429 / 5xx / timeouts with jittered exponential backoff; raises at once on
    4xx client errors. The caller should log resp["model"] (the string the API actually
    served), resp["usage"] and resp["choices"][0]["finish_reason"].
    """
    headers = {
        "Authorization": f"Bearer {api_key()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/adrian-erlikhman/LangLLM",
        "X-Title": os.environ.get("OPENROUTER_APP_TITLE", "LangLLM"),
    }
    body: dict = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if reasoning:
        body["reasoning"] = reasoning
    if seed is not None:
        body["seed"] = seed
    if extra:
        body.update(extra)

    last_err: Exception | None = None
    for attempt in range(max_retries):
        try:
            r = requests.post(API_URL, headers=headers, json=body, timeout=timeout)
            if r.status_code == 200:
                data = r.json()
                if "error" in data:  # OpenRouter can return 200 with an error envelope
                    raise OpenRouterError(f"envelope: {data['error']}")
                if not data.get("choices"):
                    raise OpenRouterError(f"no choices: {str(data)[:300]}")
                return data
            if str(r.status_code) in _FATAL:
                raise OpenRouterError(f"{r.status_code}: {r.text[:500]}")
            last_err = OpenRouterError(f"{r.status_code}: {r.text[:300]}")
        except OpenRouterError as e:
            if str(e)[:3] in _FATAL:
                raise
            last_err = e
        except (requests.Timeout, requests.ConnectionError) as e:
            last_err = e
        time.sleep(min(60, 2 ** attempt + random.random()))
    raise OpenRouterError(f"gave up after {max_retries} attempts: {last_err}")


def text_of(resp: dict) -> str:
    msg = resp["choices"][0]["message"]
    content = msg.get("content") or ""
    if isinstance(content, list):  # some providers return content parts
        content = "".join(p.get("text", "") for p in content if isinstance(p, dict))
    return content.strip()


def usage_of(resp: dict) -> dict:
    u = resp.get("usage") or {}
    return {k: u.get(k) for k in ("prompt_tokens", "completion_tokens", "total_tokens", "cost")}
