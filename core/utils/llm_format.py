import re

def clean_llm_response(text: str) -> str:
    """
    Универсальная функция для форматирования текста:
    - Markdown-стиль (**жирный**, *курсив*) → HTML
    - Списки и маркеры → единый стиль
    - Удаление лишних пробелов и пустых строк
    """
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # **жирный**
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)        # *курсив*
    text = re.sub(r'^[-—•]\s*', '— ', text, flags=re.MULTILINE)  # маркеры списков
    text = re.sub(r'\n{2,}', '\n', text)  # двойные переносы -> один
    text = re.sub(r'\n\s*\n', '\n', text)  # убрать пустые строки
    text = text.strip()
    return text 