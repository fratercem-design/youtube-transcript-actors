"""Configuration settings."""

import os
from dotenv import load_dotenv

load_dotenv()

# YouTube Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# Storage Configuration
STORAGE_TYPE = os.getenv("STORAGE_TYPE", "json")  # json, csv, or database
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./results")

# Processing Configuration
MIN_TRANSCRIPT_LENGTH = int(os.getenv("MIN_TRANSCRIPT_LENGTH", "100"))
MAX_TRANSCRIPT_LENGTH = int(os.getenv("MAX_TRANSCRIPT_LENGTH", "1000000"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "./logs/app.log")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
