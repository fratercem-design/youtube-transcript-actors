"""Actor for cleaning and normalizing transcript data."""

import re
from typing import Any, Dict
from .base import BaseActor


class DataCleaner(BaseActor):
    """Cleans and normalizes transcript text."""

    def __init__(self, name: str = "data_cleaner"):
        """Initialize data cleaner actor.

        Args:
            name: Name of the actor
        """
        super().__init__(name, "data_cleaner")

    def process(self, input_data: Any) -> Dict[str, Any]:
        """Clean and normalize transcript text.

        Args:
            input_data: Dictionary with 'transcript' key containing text

        Returns:
            Dictionary with cleaned transcript
        """
        if isinstance(input_data, dict):
            transcript = input_data.get("transcript")
        else:
            transcript = input_data

        if not transcript:
            raise ValueError("Transcript text is required")

        # Clean the transcript
        cleaned = self._clean_text(transcript)

        return {
            "original_length": len(transcript),
            "cleaned_length": len(cleaned),
            "transcript": cleaned,
            "cleaning_stats": {
                "removed_duplicates": self._count_removed_duplicates(transcript, cleaned),
                "normalized_whitespace": self._whitespace_normalized(cleaned),
            },
        }

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean text by removing noise and normalizing.

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove URLs
        text = re.sub(r"http\S+|www\S+", "", text)

        # Remove email addresses
        text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "", text)

        # Remove special characters but keep punctuation
        text = re.sub(r"[^\w\s\.\,\!\?\-]", "", text)

        # Remove duplicate spaces
        text = re.sub(r"\s+", " ", text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    @staticmethod
    def _count_removed_duplicates(original: str, cleaned: str) -> int:
        """Count approximate duplicates removed.

        Args:
            original: Original text
            cleaned: Cleaned text

        Returns:
            Count of removed items
        """
        return len(original) - len(cleaned)

    @staticmethod
    def _whitespace_normalized(text: str) -> bool:
        """Check if whitespace is properly normalized.

        Args:
            text: Text to check

        Returns:
            True if normalized
        """
        return "\n\n" not in text and "  " not in text
