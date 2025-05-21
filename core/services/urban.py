from core.utils.http import fetch_json
from core.services.yandex_translate import translate_yandex

async def get_urban_definition(term: str):
    url = f"https://api.urbandictionary.com/v0/define?term={term}"
    result = await fetch_json(url, method="GET")
    if result["list"]:
        entry = result["list"][0]
        definition = entry["definition"]
        example = entry.get("example", "")
        return definition, example
    else:
        return None, None 

async def get_urban_definition_with_translate(term: str, target_lang: str = 'ru'):
    definition, example = await get_urban_definition(term)
    if not definition:
        return None, None, None, None
    definition_translated = await translate_yandex(definition, target_lang)
    example_translated = await translate_yandex(example, target_lang) if example else None
    return definition, example, definition_translated, example_translated 