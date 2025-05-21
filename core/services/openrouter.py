import aiohttp
import logging
import re
from core.settings import settings
from core.utils.llm_format import clean_llm_response
from core.utils.http import fetch_json

PROMPT_TEMPLATE = (
    "Объясни на русском языке, что значит английское сленговое выражение: '{query}'. "
    "Приведи пару примеров использования. "
    "Если это не сленговое слово или не является английским выражением, напиши: 'Это не сленговое слово или не является английским выражением.' "
    "В ответе пришли краткий ответ с контекстом без лишней воды."
)

def get_multi_random_slang_prompt(count: int) -> str:
    return (
        f"Придумай и объясни на русском языке {count} современных английских сленговых выражений, кроме Rizz. "
        "Для каждого выражения укажи само слово, его значение и пару примеров использования. "
        "Ответ структурируй по пунктам, чтобы было понятно, где какое выражение. "
        "В ответе пришли кратко, без лишней воды."
    )

RANDOM_SLANG_PROMPT = get_multi_random_slang_prompt(1)

logger = logging.getLogger("openrouter")

async def get_openrouter_explanation(query: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.services.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/",  # OpenRouter требует указать реферер
        "X-Title": "SlangBot"
    }
    data = {
        "model": "deepseek/deepseek-r1",
        "messages": [
            {"role": "user", "content": PROMPT_TEMPLATE.format(query=query)}
        ]
    }
    result = await fetch_json(url, method="POST", headers=headers, json=data, logger=logger)
    return result["choices"][0]["message"]["content"].strip()

async def get_random_slang_openrouter(count: int = 1) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.services.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/",
        "X-Title": "SlangBot"
    }
    prompt = get_multi_random_slang_prompt(count)
    data = {
        "model": "deepseek/deepseek-r1",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    result = await fetch_json(url, method="POST", headers=headers, json=data, logger=logger)
    return result["choices"][0]["message"]["content"].strip() 