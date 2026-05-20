"""Data models for transcript processing."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class TranscriptEntry(BaseModel):
    """Single transcript entry."""

    text: str
    start: float
    duration: Optional[float] = None


class SentimentData(BaseModel):
    """Sentiment analysis data."""

    polarity: float
    subjectivity: float
    label: str


class TopicData(BaseModel):
    """Topic extraction data."""

    term: str
    frequency: int


class TranscriptAnalysis(BaseModel):
    """Complete transcript analysis result."""

    video_id: str
    transcript: str
    cleaned_transcript: str
    sentiment: SentimentData
    topics: List[TopicData]
    summary: str
    quality_score: float
    is_valid: bool
    processed_at: datetime


class ProcessingResult(BaseModel):
    """Pipeline processing result."""

    video_id: str
    status: str
    timestamp: datetime
    result: Optional[TranscriptAnalysis] = None
    error: Optional[str] = None
