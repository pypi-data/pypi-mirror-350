import aiohttp

_API_URL = "https://browser.translate.yandex.net/api/v1/tr.json/translate"
_DEFAULT_PARAMS = {
    "translateMode": "context",
    "id": "197099eb3ab99f99-4-0",
    "srv": "yabrowser",
    "format": "html",
    "options": "2",
    "version": "8.4"
}

async def translate(text: str, lang: str) -> str:
    """
    Асинхронно переводит текст с помощью API Яндекс Переводчика.

    :param text: текст для перевода
    :param lang: направление перевода, например "en-ru"
    :return: переведённый текст
    """
    params = _DEFAULT_PARAMS.copy()
    params.update({"text": text, "lang": lang})

    async with aiohttp.ClientSession() as session:
        async with session.get(_API_URL, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data["text"][0]
            raise Exception(f"Ошибка API Яндекс Переводчика, статус: {resp.status}")
