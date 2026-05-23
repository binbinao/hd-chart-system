"""AI-powered deep reading service using OpenAI-compatible API."""
import os
import json
from typing import Generator

from openai import OpenAI

from hd_api.dependencies import do_calculate, do_reading
from hd_interp.formatter import format_reading_markdown


# ============================================================
# Configuration (from environment variables)
# ============================================================

def get_ai_config() -> dict:
    """Return current AI configuration (safe to expose, no key)."""
    api_key = os.environ.get("AI_API_KEY", "")
    return {
        "configured": bool(api_key),
        "base_url": os.environ.get("AI_BASE_URL", "https://api.openai.com/v1"),
        "model": os.environ.get("AI_MODEL", "gpt-4o"),
    }


def _get_client() -> OpenAI:
    """Create an OpenAI client from environment config."""
    api_key = os.environ.get("AI_API_KEY")
    if not api_key:
        raise RuntimeError("AI_API_KEY 未配置。请在 .env 或环境变量中设置。")
    base_url = os.environ.get("AI_BASE_URL", "https://api.openai.com/v1")
    return OpenAI(api_key=api_key, base_url=base_url)


# ============================================================
# Prompt Templates
# ============================================================

SYSTEM_PROMPT = """你是一位资深的人类图（Human Design）分析师，拥有丰富的解读经验。请基于以下人类图数据，为用户提供深度、个性化的解读分析。

分析要求：
1. 综合分析此人的能量类型、权威和人生角色之间的互动关系
2. 解读通道组合带来的独特天赋和潜在挑战
3. 针对此人的定义类型，给出人际关系和决策方面的建议
4. 结合人生交叉，阐述此人的人生方向和使命
5. 给出实际可操作的生活建议

请用温暖、专业的中文回答，避免过于学术化。使用 Markdown 格式组织内容。"""


def _build_user_prompt(reading: dict) -> str:
    """Build the user prompt with full chart reading as context."""
    markdown_reading = format_reading_markdown(reading)
    return f"以下是此人的完整人类图数据：\n\n{markdown_reading}"


# ============================================================
# Streaming AI Reading
# ============================================================

def stream_ai_reading(chart_result) -> Generator[str, None, None]:
    """Stream AI analysis as SSE events.

    Yields SSE-formatted strings: 'data: {"content": "..."}\n\n'
    Final event: 'data: [DONE]\n\n'
    """
    # Generate structured reading
    reading = do_reading(chart_result)
    user_prompt = _build_user_prompt(reading)
    model = os.environ.get("AI_MODEL", "gpt-4o")

    client = _get_client()

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            stream=True,
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        error_msg = f"AI 分析出错: {str(e)}"
        yield f"data: {json.dumps({'error': error_msg}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"
