import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

# Database configuration
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "memory.db"

# Create database directory if missing
DATABASE_DIR.mkdir(exist_ok=True)

# Application configuration
APP_TITLE = "Memory AI"
APP_ICON = "🧠"

# Memory configuration
MAX_SHORT_TERM_MESSAGES = 10
MAX_RETRIEVED_MEMORIES = 5