"""Actor for summarizing transcript content."""

from typing import Any, Dict, List
import re
from .base import BaseActor


class Summarizer(BaseActor):
    """Generates concise summaries of transcript content."""

    def __init__(self, name: str = "summarizer"):
        """Initialize summarizer actor.

        Args:
            name: Name of the actor
        """
        super().__init__(name, "summarizer")

    def process(self, input_data: Any) -> Dict[str, Any]:
        """Generate summary of transcript.

        Args:
            input_data: Dictionary with 'transcript' key or transcript text

        Returns:
            Dictionary with summary and stats
        """
        if isinstance(input_data, dict):
            transcript = input_data.get("transcript")
        else:
            transcript = input_data

        if not transcript:
            raise ValueError("Transcript text is required")

        # Generate summaries of different lengths
        short_summary = self._generate_summary(transcript, sentences=3)
        medium_summary = self._generate_summary(transcript, sentences=5)
        long_summary = self._generate_summary(transcript, sentences=10)

        # Get key sentences
        key_sentences = self._extract_key_sentences(transcript, count=5)

        return {
            "short_summary": short_summary,
            "medium_summary": medium_summary,
            "long_summary": long_summary,
            "key_sentences": key_sentences,
            "original_length": len(transcript.split()),
            "summary_ratio": round(
                len(medium_summary.split()) / len(transcript.split()), 3
            ),
        }

    @staticmethod
    def _generate_summary(text: str, sentences: int = 5) -> str:
        """Generate extractive summary of text.

        Args:
            text: Text to summarize
            sentences: Number of sentences to include

        Returns:
            Summary text
        """
        # Split into sentences
        sentence_list = re.split(r"[.!?]+", text)
        sentence_list = [s.strip() for s in sentence_list if s.strip()]

        if len(sentence_list) <= sentences:
            return text

        # Score sentences by word frequency
        words = re.findall(r"\b\w+\b", text.lower())
        word_freq = {}
        for word in words:
            if len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Score and select top sentences
        scored_sentences = []
        for i, sentence in enumerate(sentence_list):
            score = 0
            for word in re.findall(r"\b\w+\b", sentence.lower()):
                score += word_freq.get(word, 0)
            scored_sentences.append((i, sentence, score))

        # Get top sentences in original order
        top_sentences = sorted(scored_sentences, key=lambda x: x[2], reverse=True)[
            :sentences
        ]
        top_sentences = sorted(top_sentences, key=lambda x: x[0])

        return ". ".join([s[1] for s in top_sentences]) + "."

    @staticmethod
    def _extract_key_sentences(text: str, count: int = 5) -> List[str]:
        """Extract key sentences from text.

        Args:
            text: Text to analyze
            count: Number of sentences to extract

        Returns:
            List of key sentences
        """
        # Split into sentences
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Return first sentences as key sentences
        return sentences[:count]
