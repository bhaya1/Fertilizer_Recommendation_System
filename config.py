"""
Configuration file for Fertilizer Recommendation System
Customize API and frontend settings here
"""

import os
from pathlib import Path

# =====================================================
# PROJECT PATHS
# =====================================================
PROJECT_DIR = Path(__file__).parent
BACKEND_DIR = PROJECT_DIR / "backend"
FRONTEND_DIR = PROJECT_DIR / "frontend"
DATA_DIR = PROJECT_DIR

# =====================================================
# API CONFIGURATION
# =====================================================
API_HOST = "0.0.0.0"
API_PORT = 8000
API_DEBUG = False
API_LOG_LEVEL = "info"

# CORS Settings
CORS_ORIGINS = ["*"]  # Change to specific domains in production
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# =====================================================
# MODEL CONFIGURATION
# =====================================================
MODEL_NAME = "multitask_model (1).pth"
DEVICE = "cpu"  # Use "cuda" if GPU available and PyTorch is GPU-enabled

# =====================================================
# PREPROCESSOR FILES
# =====================================================
PREPROCESSORS = {
    "le_cycle": "le_actual_cycle (1).pkl",
    "le_desc": "le_actual_desc (1).pkl",
    "le_fert": "le_actual_fert (1).pkl",
    "scaler_X": "scaler_X (1).pkl",
    "qty_scaler": "qty_scaler (1).pkl",
    "le_soil": "cycle_encoder (1).pkl",
    "le_crop": "desc_encoder (1).pkl"
}

# =====================================================
# FRONTEND CONFIGURATION
# =====================================================
FRONTEND_PORT = 8080
API_BASE_URL = "http://localhost:8000"  # Change for production

# Default input values for demo
DEFAULT_VALUES = {
    "temperature": 25.5,
    "humidity": 65.0,
    "moisture": 55.0,
    "soil_type": "Black",
    "crop_type": "Cotton",
    "nitrogen": 40.0,
    "potassium": 30.0,
    "phosphorous": 20.0
}

# =====================================================
# CROP AND SOIL OPTIONS
# =====================================================
SOIL_TYPES = [
    "Black",
    "Red",
    "Clay",
    "Sandy",
    "Loamy"
]

CROP_TYPES = [
    "Cotton",
    "Rice",
    "Wheat",
    "Corn",
    "Sugarcane",
    "Pulses",
    "Vegetables"
]

# =====================================================
# PREDICTION SETTINGS
# =====================================================
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for warning
QUANTITY_UNIT = "kg"  # Output unit for fertilizer quantity
TEMPERATURE_UNIT = "C"  # Temperature unit (C for Celsius, F for Fahrenheit)

# =====================================================
# LOGGING
# =====================================================
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = PROJECT_DIR / "app.log"

# Enable detailed logging
ENABLE_DETAILED_LOGS = False

# =====================================================
# SECURITY (For Production)
# =====================================================
API_KEY_REQUIRED = False  # Set to True for production and add API key
API_KEYS = []  # Add valid API keys here

RATE_LIMIT_ENABLED = False  # Set to True to enable rate limiting
RATE_LIMIT_REQUESTS = 100  # Requests per minute
RATE_LIMIT_WINDOW = 60  # Time window in seconds

# =====================================================
# HEALTH CHECK SETTINGS
# =====================================================
CHECK_MODEL_ON_STARTUP = True
CHECK_FILES_ON_STARTUP = True

# =====================================================
# FUNCTION TO GET CONFIG VALUES
# =====================================================
def get_config():
    """Return configuration as dictionary"""
    return {
        "project_dir": str(PROJECT_DIR),
        "backend_dir": str(BACKEND_DIR),
        "frontend_dir": str(FRONTEND_DIR),
        "api_host": API_HOST,
        "api_port": API_PORT,
        "frontend_port": FRONTEND_PORT,
        "api_base_url": API_BASE_URL,
        "model_name": MODEL_NAME,
        "device": DEVICE,
        "soil_types": SOIL_TYPES,
        "crop_types": CROP_TYPES
    }

if __name__ == "__main__":
    import json
    config = get_config()
    print(json.dumps(config, indent=2))
