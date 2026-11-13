import asyncio
import logging
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# On Windows, set SelectorEventLoopPolicy for robust non-blocking socket operations
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

from aiohttp import web
from backend.config import BOT_TOKEN, WEB_HOST, WEB_PORT, WEBAPP_URL
from backend.database import init_db
from backend.seed_data import seed_initial_tests
from backend.server import create_app
from backend.keep_alive import keep_alive_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("IELTS-Runner")

async def main():
    logger.info("Initializing IELTS Mock Platform...")
    
    # 1. Init Database & Seed data (Synchronous & instant)
    init_db()
    seed_initial_tests()

    # 2. Setup Aiohttp Web Server
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEB_HOST, WEB_PORT)
    await site.start()
    
    logger.info("=" * 60)
    logger.info("🎉 TELEGRAM MINI APP SERVER IS LIVE!")
    logger.info(f"🌐 Mini App URL: http://localhost:{WEB_PORT}")
    logger.info(f"📲 External WebApp URL: {WEBAPP_URL}")
    logger.info("=" * 60)

    # 3. Start Keep-Alive Agent in background
    asyncio.create_task(keep_alive_agent())

    # 4. Setup Telegram Bot if BOT_TOKEN is configured
    if BOT_TOKEN and BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        try:
            from aiogram import Bot
            from backend.bot import start_bot
            bot = Bot(token=BOT_TOKEN)
            logger.info("🚀 Launching Telegram Bot...")
            await start_bot(bot)
        except Exception as e:
            logger.error(f"Error starting Telegram bot: {e}")
            logger.info("Mini App web server continues running...")
            while True:
                await asyncio.sleep(3600)
    else:
        logger.warning("=" * 60)
        logger.warning("⚠️ BOT_TOKEN topilmadi yoki kiritilmagan (.env faylini tekshiring).")
        logger.warning(f"👉 Mini App brauzerda ishlamoqda: http://localhost:{WEB_PORT}")
        logger.warning("Telegram Botga ulash uchun .env faylida BOT_TOKEN ko'rsating!")
        logger.warning("=" * 60)
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Server stopped.")
