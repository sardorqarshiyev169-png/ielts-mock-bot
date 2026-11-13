import asyncio
import logging
import aiohttp
from .config import WEBAPP_URL, KEEP_ALIVE

logger = logging.getLogger("KeepAlive")

async def keep_alive_agent():
    """
    Background Keep-Alive Agent for Render.com.
    Pings the service URL every 10 minutes (600 seconds) so Render never sleeps.
    """
    if not KEEP_ALIVE:
        logger.info("Keep-Alive agent is disabled.")
        return

    logger.info("Keep-Alive agent started. Will keep Render instance awake 24/7.")
    
    # Wait 60 seconds after startup before initial ping
    await asyncio.sleep(60)

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                target_url = WEBAPP_URL.rstrip("/") + "/healthz"
                if target_url.startswith("http"):
                    async with session.get(target_url, timeout=15) as resp:
                        logger.info(f"Keep-Alive ping sent to {target_url} -> Status: {resp.status}")
            except Exception as e:
                logger.warning(f"Keep-Alive ping failed: {e}")

            # Sleep 10 minutes (Render sleep threshold is 15 minutes)
            await asyncio.sleep(600)
