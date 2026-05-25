"""
Configuration module for Multimodal Document Analyzer.
Manages application settings and environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.absolute()
UPLOADS_DIR = os.getenv('UPLOADS_DIR', os.path.join(BASE_DIR, 'uploads'))
REPORTS_DIR = os.getenv('REPORTS_DIR', os.path.join(BASE_DIR, 'reports'))
DATABASE_PATH = os.getenv('DATABASE_PATH', os.path.join(BASE_DIR, 'analyzer.db'))

# Create directories if they don't exist
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# OCR Settings
USE_EASYOCR = os.getenv('USE_EASYOCR', 'true').lower() == 'true'
OCR_LANGUAGES = os.getenv('OCR_LANGUAGES', 'en').split(',')

# Upload Settings
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '200'))
ALLOWED_FORMATS = os.getenv('ALLOWED_FORMATS', 'pdf,jpg,jpeg,png,docx,txt').split(',')

# Streamlit Settings
STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', '8501'))
STREAMLIT_THEME = os.getenv('STREAMLIT_THEME', 'light')

# Model Settings
MODEL_DEVICE = os.getenv('MODEL_DEVICE', 'cpu')  # 'cpu' or 'cuda'
USE_GPU = MODEL_DEVICE == 'cuda'

# Security Settings
MAX_FAILED_ATTEMPTS = int(os.getenv('MAX_FAILED_ATTEMPTS', '5'))
SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', '30'))

# API Settings (for future REST API)
API_ENABLE = os.getenv('API_ENABLE', 'false').lower() == 'true'
API_PORT = int(os.getenv('API_PORT', '8000'))

# Logging Settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', os.path.join(BASE_DIR, 'logs', 'app.log'))

# Summarization Settings
SUMMARY_MAX_LENGTH = int(os.getenv('SUMMARY_MAX_LENGTH', '150'))
SUMMARY_MIN_LENGTH = int(os.getenv('SUMMARY_MIN_LENGTH', '50'))
NUM_KEYWORDS = int(os.getenv('NUM_KEYWORDS', '15'))
NUM_TOPICS = int(os.getenv('NUM_TOPICS', '5'))

# QA Settings
QA_CONFIDENCE_THRESHOLD = float(os.getenv('QA_CONFIDENCE_THRESHOLD', '0.3'))
QA_MAX_ANSWER_LENGTH = int(os.getenv('QA_MAX_ANSWER_LENGTH', '256'))

# Application Settings
APP_NAME = "Multimodal Document Analyzer"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# Feature Flags
ENABLE_CHAT = os.getenv('ENABLE_CHAT', 'true').lower() == 'true'
ENABLE_REPORTS = os.getenv('ENABLE_REPORTS', 'true').lower() == 'true'
ENABLE_API = os.getenv('ENABLE_API', 'false').lower() == 'true'
ENABLE_BATCH_PROCESSING = os.getenv('ENABLE_BATCH_PROCESSING', 'false').lower() == 'true'


def validate_config():
    """Validate configuration settings."""
    errors = []

    if MAX_FILE_SIZE_MB <= 0:
        errors.append("MAX_FILE_SIZE_MB must be positive")

    if not os.path.exists(UPLOADS_DIR):
        try:
            os.makedirs(UPLOADS_DIR)
        except Exception as e:
            errors.append(f"Cannot create uploads directory: {e}")

    if not os.path.exists(REPORTS_DIR):
        try:
            os.makedirs(REPORTS_DIR)
        except Exception as e:
            errors.append(f"Cannot create reports directory: {e}")

    if not ALLOWED_FORMATS:
        errors.append("ALLOWED_FORMATS is empty")

    if QA_CONFIDENCE_THRESHOLD < 0 or QA_CONFIDENCE_THRESHOLD > 1:
        errors.append("QA_CONFIDENCE_THRESHOLD must be between 0 and 1")

    if errors:
        raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")

    return True


# Validate configuration on import
try:
    validate_config()
except ValueError as e:
    print(f"Warning: {e}")
