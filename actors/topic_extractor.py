"""Actor for extracting topics from transcripts."""

from typing import Any, Dict, List
import re
from collections import Counter
from .base import BaseActor


class TopicExtractor(BaseActor):
    """Extracts key topics and themes from transcript content."""

    def __init__(self, name: str = "topic_extractor"):
        """Initialize topic extractor actor.

        Args:
            name: Name of the actor
        """
        super().__init__(name, "topic_extractor")
        self.stop_words = self._load_stop_words()

    def process(self, input_data: Any) -> Dict[str, Any]:
        """Extract topics from transcript text.

        Args:
            input_data: Dictionary with 'transcript' key or transcript text

        Returns:
            Dictionary with extracted topics
        """
        if isinstance(input_data, dict):
            transcript = input_data.get("transcript")
        else:
            transcript = input_data

        if not transcript:
            raise ValueError("Transcript text is required")

        # Extract key terms
        key_terms = self._extract_key_terms(transcript)

        # Extract noun phrases
        noun_phrases = self._extract_noun_phrases(transcript)

        # Identify topics by frequency
        topics = self._identify_topics(transcript)

        return {
            "key_terms": key_terms[:20],  # Top 20
            "noun_phrases": noun_phrases[:15],  # Top 15
            "topics": topics,
            "topic_count": len(topics),
        }

    def _extract_key_terms(self, text: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Extract most frequent key terms.

        Args:
            text: Text to analyze
            limit: Number of terms to return

        Returns:
            List of key terms with frequencies
        """
        # Tokenize and clean
        words = re.findall(r"\b[a-z]{4,}\b", text.lower())
        words = [w for w in words if w not in self.stop_words]

        # Get most common
        counter = Counter(words)
        common = counter.most_common(limit)

        return [{"term": term, "frequency": freq} for term, freq in common]

    def _extract_noun_phrases(self, text: str, limit: int = 15) -> List[Dict[str, Any]]:
        """Extract noun phrases from text.

        Args:
            text: Text to analyze
            limit: Number of phrases to return

        Returns:
            List of noun phrases
        """
        # Simple pattern-based extraction
        pattern = r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b"
        phrases = re.findall(pattern, text)
        counter = Counter(phrases)
        common = counter.most_common(limit)

        return [{"phrase": phrase, "frequency": freq} for phrase, freq in common]

    def _identify_topics(self, text: str) -> List[str]:
        """Identify main topics from text.

        Args:
            text: Text to analyze

        Returns:
            List of identified topics
        """
        # Extract noun phrases and key terms
        phrases = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)
        words = re.findall(r"\b[a-z]{5,}\b", text.lower())
        words = [w for w in words if w not in self.stop_words]

        # Combine and get unique topics
        all_terms = phrases + words
        counter = Counter(all_terms)
        topics = [term for term, _ in counter.most_common(10)]

        return topics

    @staticmethod
    def _load_stop_words() -> set:
        """Load common English stop words.

        Returns:
            Set of stop words
        """
        return {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "is", "was", "are", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "must", "can", "this", "that", "these",
            "those", "i", "you", "he", "she", "it", "we", "they", "what", "which",
            "who", "when", "where", "why", "how", "all", "each", "every", "some",
            "any", "many", "much", "more", "most", "other", "same", "such", "as",
        }
