"""Nebius AI Studio (OpenAI-compatible) LLM client."""

import json

from app import config
from app.llm import prompts


def evaluate(transcript: str, scenario: str, metrics: dict) -> dict:
    """Score the transcript: {"score": 0-100, "feedback": "..."}."""
    from openai import OpenAI

    client = OpenAI(base_url=config.NEBIUS_BASE_URL, api_key=config.nebius_api_key())
    reply = (
        client.chat.completions.create(
            model=config.NEBIUS_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompts.evaluation_prompt(transcript, scenario, metrics),
                }
            ],
        )
        .choices[0]
        .message.content
    )
    text = reply.strip().removeprefix("```json").removeprefix("```")
    return json.loads(text.removesuffix("```").strip())
