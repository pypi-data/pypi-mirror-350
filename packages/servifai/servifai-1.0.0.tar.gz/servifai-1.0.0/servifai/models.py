"""Data models for ServifAI responses"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum

class DocumentAsset(BaseModel):
    """Represents an extracted document asset"""
    asset_id: str
    asset_type: str  # "image" | "table"
    url: str
    secure_url: Optional[str] = None
    file_name: str
    source_document: str
    page_number: int
    description: Optional[str] = None
    metadata: Dict[str, Any] = {}

class Citation(BaseModel):
    """Represents a source citation"""
    id: int
    source_document: str
    page_number: Optional[int] = None
    section: Optional[str] = None
    relevance_score: float
    text_preview: str
    assets: List[DocumentAsset] = []
    metadata: Dict[str, Any] = {}

class ProcessingStatus(str, Enum):
    """Processing status values"""
    QUEUED = "queued"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"

class ProcessingResult(BaseModel):
    """Result of document processing"""
    session_id: str
    status: ProcessingStatus
    processed_documents: List[str]
    total_pages: int
    total_text_chunks: int
    total_images: int
    total_tables: int
    processing_time_seconds: float
    subscription_tier: str
    created_at: datetime
    metadata: Dict[str, Any] = {}

class SearchResult(BaseModel):
    """Result of search query"""
    query: str
    citations: List[Citation]
    total_results: int
    processing_time_seconds: float
    subscription_tier: str
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = {}

class SubscriptionInfo(BaseModel):
    """Information about user's subscription"""
    tier: str
    features: List[str]
    rate_limit: int
    usage_count: int
    is_active: bool
