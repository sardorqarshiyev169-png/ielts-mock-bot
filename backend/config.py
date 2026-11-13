import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

# Bot & Web Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")

# Render automatically sets PORT environment variable
WEB_PORT = int(os.getenv("PORT", os.getenv("WEB_PORT", "8080")))
WEBAPP_URL = os.getenv("WEBAPP_URL", f"http://localhost:{WEB_PORT}").rstrip("/")

# Keep Alive & Auto Pinger for Render
KEEP_ALIVE = os.getenv("KEEP_ALIVE", "true").lower() in ("true", "1", "yes")

# AI & External APIs
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Admin IDs
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]

# Storage paths
DATA_DIR = BASE_DIR / "data"
AUDIO_DIR = DATA_DIR / "audio"
DB_PATH = DATA_DIR / "ielts.db"

# Ensure directories exist
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
