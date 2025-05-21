import re
 
def split_queries(text: str):
    return [q.strip() for q in re.split(r'[\n;,]+', text) if q.strip()]

def format_ai_answer(query: str, explanation: str) -> str:
    return (
        f"🤖 <b>AI-объяснение</b>\n"
        f"🌟 <b>{query}</b>\n"
        f"{explanation.strip()}"
    )

def format_urban_answer(query: str, definition_tr: str, example_tr: str = None) -> str:
    text = f"📚 <b>Urban+Яндекс-словарь</b>\n🌈 <b>{query}</b>\n{definition_tr.rstrip()}"
    if example_tr:
        text += f"\n\n💡 <b>Пример:</b> {example_tr.strip()}"
    return text

def format_arena_answer(query: str, ai_explanation: str, definition_tr: str, example_tr: str = None) -> str:
    text = f"🌟 <b>{query}</b>\n"
    text += "━━━━━━━━━━━━━━\n"
    text += "🤖 <b>AI-объяснение</b>\n" + ai_explanation.strip() + "\n"
    text += "──────────────\n"
    text += f"📚 <b>Urban+Яндекс-словарь</b>\n{definition_tr.rstrip()}"
    if example_tr:
        text += f"\n\n💡 <b>Пример:</b> {example_tr.strip()}"
    return text

def format_api_error(query: str = None) -> str:
    if query:
        return f"<b>{query}</b>: ⚠️ Произошла ошибка при обращении к внешнему сервису. Попробуйте позже или выберите другой режим."
    return "⚠️ Произошла ошибка при обращении к внешнему сервису. Попробуйте позже или выберите другой режим."