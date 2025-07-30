"""
ServifAI - AI-Powered PDF Parsing and Retrieval Library

A powerful Python library that provides intelligent PDF processing through
multiple subscription tiers optimized for different use cases.
"""

__version__ = "1.0.0"
__author__ = "ServifAI Team"

from .client import ServifAI
from .config import ServifAIConfig, SubscriptionTier
from .exceptions import (
    ServifAIException,
    AuthenticationError,
    RateLimitError,
    ProcessingError,
    SubscriptionError
)
from .models import (
    ProcessingResult,
    SearchResult,
    DocumentAsset,
    Citation
)

__all__ = [
    "ServifAI",
    "ServifAIConfig",
    "SubscriptionTier",
    "ServifAIException",
    "AuthenticationError", 
    "RateLimitError",
    "ProcessingError",
    "SubscriptionError",
    "ProcessingResult",
    "SearchResult", 
    "DocumentAsset",
    "Citation",
]