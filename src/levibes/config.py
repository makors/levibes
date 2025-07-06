"""
Configuration settings for LeVibes
"""

import os
from pathlib import Path

# Default settings
DEFAULT_NUM_IMAGES = 5
DEFAULT_IMAGES_DIR = "./images"
DEFAULT_OUTPUT_DIR = "./output"
DEFAULT_IMAGE_SIZE = (1000, 1000)

# Font settings
FONT_NAMES = [
    "Montserrat-VariableFont_wght.ttf",
    "montserrat.ttf",
    "arial.ttf",
    "DejaVuSans.ttf",
]

# Image processing settings
PADDING_SCALING_FACTOR = 1.0
LINE_SPACING_RATIO = 0.4
MAX_TEXT_WIDTH_RATIO = 0.9
FONT_SIZE_RATIO = 20  # image width divided by this value

# OpenAI settings
OPENAI_MODEL = "gpt-4.1"
OPENAI_TEMPERATURE = 0.9

# Supported image formats
SUPPORTED_IMAGE_FORMATS = (".jpg", ".jpeg", ".png")

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
IMAGES_DIR = PROJECT_ROOT / "images"
OUTPUT_DIR = PROJECT_ROOT / "output"
