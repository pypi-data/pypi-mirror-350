"""
KBKI Classifier - Indonesian Commodity Classification
"""

__version__ = "0.1.0"
__author__ = "deplearning"

from .classifier import KBKIClassifier
from .downloader import ModelDownloader

__all__ = ["KBKIClassifier", "ModelDownloader"]
