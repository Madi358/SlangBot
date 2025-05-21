import aiohttp
import logging

async def fetch_json(url, method="POST", headers=None, json=None, logger=None):
    logger = logger or logging.getLogger("http")
    async with aiohttp.ClientSession() as session:
        req = session.post if method == "POST" else session.get
        async with req(url, headers=headers, json=json) as resp:
            logger.info(f"HTTP {method} {url} status: {resp.status}")
            try:
                result = await resp.json()
                logger.info(f"HTTP {method} {url} body: {result}")
            except Exception:
                text = await resp.text()
                logger.error(f"HTTP {method} {url} not JSON: {text}")
                raise
            if resp.status != 200:
                logger.error(f"HTTP {method} {url} error: {result}")
                raise Exception(f"API error: {result}")
            return result 