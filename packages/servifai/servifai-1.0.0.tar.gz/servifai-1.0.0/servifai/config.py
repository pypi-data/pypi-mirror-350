"""Configuration management for ServifAI"""

import os
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

class SubscriptionTier(str, Enum):
    """Available subscription tiers"""
    QUICKEST = "quickest"  
    BALANCED = "balanced"
    SECURED = "secured"

class ServifAIConfig(BaseModel):
    """Configuration settings for ServifAI client"""
    
    api_key: str = Field(description="ServifAI API key")
    api_url: str = Field(default="https://api.syntheialabs.ai", description="API base URL")
    timeout: int = Field(default=300, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retries")
    default_tier: Optional[SubscriptionTier] = Field(default=None, description="Default tier")
    log_level: str = Field(default="INFO", description="Logging level")
    
    @field_validator('api_key')
    def validate_api_key(cls, v):
        if not v or not v.startswith('sai_'):
            raise ValueError("Valid ServifAI API key required (starts with 'sai_')")
        return v
    
    @classmethod
    def from_env(cls, env_file: str = ".env") -> "ServifAIConfig":
        """Load configuration from environment variables"""
        load_dotenv(env_file, override=False)
        
        return cls(
            api_key=os.getenv("SERVIFAI_API_KEY", ""),
            api_url=os.getenv("SERVIFAI_API_URL", "https://api.syntheialabs.ai"),
            timeout=int(os.getenv("SERVIFAI_TIMEOUT", "300")),
            max_retries=int(os.getenv("SERVIFAI_MAX_RETRIES", "3")),
            log_level=os.getenv("SERVIFAI_LOG_LEVEL", "INFO")
        )
