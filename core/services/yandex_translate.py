import logging
from core.settings import settings
from core.utils.http import fetch_json

async def translate_yandex(text: str, target_lang: str = 'ru') -> str:
    url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
    headers = {
        'Authorization': f'Api-Key {settings.services.yandex_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'folder_id': settings.services.yandex_folder_id,
        'texts': [text],
        'targetLanguageCode': target_lang
    }
    logger = logging.getLogger('yandex_translate')
    result = await fetch_json(url, method='POST', headers=headers, json=data, logger=logger)
    return result['translations'][0]['text'] 