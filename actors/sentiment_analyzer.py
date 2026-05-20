"""Actor for analyzing sentiment in transcripts."""

from typing import Any, Dict, List, Tuple
from textblob import TextBlob
from .base import BaseActor


class SentimentAnalyzer(BaseActor):
    """Analyzes sentiment and emotional tone of transcript content."""

    def __init__(self, name: str = "sentiment_analyzer"):
        """Initialize sentiment analyzer actor.

        Args:
            name: Name of the actor
        """
        super().__init__(name, "sentiment_analyzer")

    def process(self, input_data: Any) -> Dict[str, Any]:
        """Analyze sentiment of transcript text.

        Args:
            input_data: Dictionary with 'transcript' key or transcript entries

        Returns:
            Dictionary with sentiment analysis results
        """
        if isinstance(input_data, dict):
            transcript = input_data.get("transcript")
            entries = input_data.get("transcript_entries", [])
        else:
            transcript = input_data
            entries = []

        if not transcript:
            raise ValueError("Transcript text is required")

        # Analyze overall sentiment
        overall_polarity, overall_subjectivity = self._analyze_text(transcript)

        # Analyze segment sentiments if entries available
        segment_sentiments = []
        if entries:
            segment_sentiments = self._analyze_segments(entries)

        # Determine sentiment label
        sentiment_label = self._label_sentiment(overall_polarity)

        return {
            "overall_sentiment": {
                "polarity": round(overall_polarity, 3),
                "subjectivity": round(overall_subjectivity, 3),
                "label": sentiment_label,
            },
            "segment_sentiments": segment_sentiments,
            "sentiment_distribution": self._get_sentiment_distribution(segment_sentiments),
        }

    @staticmethod
    def _analyze_text(text: str) -> Tuple[float, float]:
        """Analyze sentiment polarity and subjectivity.

        Args:
            text: Text to analyze

        Returns:
            Tuple of (polarity, subjectivity)
        """
        blob = TextBlob(text)
        return blob.sentiment.polarity, blob.sentiment.subjectivity

    def _analyze_segments(self, entries: List[Dict]) -> List[Dict]:
        """Analyze sentiment of individual transcript segments.

        Args:
            entries: List of transcript entries

        Returns:
            List of segment sentiment analysis
        """
        segment_sentiments = []
        for entry in entries:
            text = entry.get("text", "")
            start = entry.get("start", 0)
            if text:
                polarity, subjectivity = self._analyze_text(text)
                segment_sentiments.append(
                    {
                        "timestamp": start,
                        "text": text[:100],  # First 100 chars
                        "polarity": round(polarity, 3),
                        "subjectivity": round(subjectivity, 3),
                        "label": self._label_sentiment(polarity),
                    }
                )
        return segment_sentiments

    @staticmethod
    def _label_sentiment(polarity: float) -> str:
        """Label sentiment based on polarity score.

        Args:
            polarity: Polarity score from -1 to 1

        Returns:
            Sentiment label
        """
        if polarity > 0.1:
            return "positive"
        elif polarity < -0.1:
            return "negative"
        else:
            return "neutral"

    @staticmethod
    def _get_sentiment_distribution(segments: List[Dict]) -> Dict[str, Any]:
        """Get distribution of sentiments across segments.

        Args:
            segments: List of segment sentiments

        Returns:
            Sentiment distribution
        """
        if not segments:
            return {"positive": 0, "negative": 0, "neutral": 0}

        labels = [s["label"] for s in segments]
        total = len(labels)

        return {
            "positive": round(labels.count("positive") / total, 3),
            "negative": round(labels.count("negative") / total, 3),
            "neutral": round(labels.count("neutral") / total, 3),
        }
