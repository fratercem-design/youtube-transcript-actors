"""Actor for validating transcript quality."""

from typing import Any, Dict, List
import re
from .base import BaseActor


class QualityValidator(BaseActor):
    """Validates data quality and completeness of transcripts."""

    def __init__(self, name: str = "quality_validator"):
        """Initialize quality validator actor.

        Args:
            name: Name of the actor
        """
        super().__init__(name, "quality_validator")
        self.min_length = 100  # Minimum characters
        self.max_length = 1000000  # Maximum characters

    def process(self, input_data: Any) -> Dict[str, Any]:
        """Validate transcript quality.

        Args:
            input_data: Dictionary with transcript data or transcript text

        Returns:
            Dictionary with quality validation results
        """
        if isinstance(input_data, dict):
            transcript = input_data.get("transcript")
            video_id = input_data.get("video_id", "unknown")
        else:
            transcript = input_data
            video_id = "unknown"

        if not transcript:
            raise ValueError("Transcript text is required")

        # Run quality checks
        checks = {
            "length_check": self._check_length(transcript),
            "content_check": self._check_content_quality(transcript),
            "encoding_check": self._check_encoding(transcript),
            "structure_check": self._check_structure(transcript),
        }

        # Calculate overall quality score
        quality_score = self._calculate_quality_score(checks)
        is_valid = quality_score >= 0.7

        return {
            "video_id": video_id,
            "is_valid": is_valid,
            "quality_score": round(quality_score, 3),
            "checks": checks,
            "issues": self._get_issues(checks),
            "recommendations": self._get_recommendations(checks),
        }

    def _check_length(self, text: str) -> Dict[str, Any]:
        """Check if transcript length is acceptable.

        Args:
            text: Transcript text

        Returns:
            Check result
        """
        length = len(text)
        passed = self.min_length <= length <= self.max_length

        return {
            "passed": passed,
            "length": length,
            "min_required": self.min_length,
            "max_allowed": self.max_length,
        }

    @staticmethod
    def _check_content_quality(text: str) -> Dict[str, Any]:
        """Check content quality indicators.

        Args:
            text: Transcript text

        Returns:
            Check result
        """
        words = text.split()
        sentences = re.split(r"[.!?]+", text)
        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0

        # Check for meaningful content
        has_alphanumeric = bool(re.search(r"[a-zA-Z0-9]", text))
        avg_sentence_length = len(words) / len([s for s in sentences if s.strip()])

        quality_good = (
            has_alphanumeric
            and 3 <= avg_word_length <= 10
            and 5 <= avg_sentence_length <= 30
        )

        return {
            "passed": quality_good,
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "has_alphanumeric": has_alphanumeric,
        }

    @staticmethod
    def _check_encoding(text: str) -> Dict[str, Any]:
        """Check text encoding quality.

        Args:
            text: Transcript text

        Returns:
            Check result
        """
        try:
            text.encode("utf-8")
            encoding_valid = True
        except UnicodeEncodeError:
            encoding_valid = False

        # Check for common encoding issues
        has_mojibake = bool(re.search(r"[\x80-\xff]{2,}", text))

        return {
            "passed": encoding_valid and not has_mojibake,
            "encoding": "utf-8" if encoding_valid else "invalid",
            "has_mojibake": has_mojibake,
        }

    @staticmethod
    def _check_structure(text: str) -> Dict[str, Any]:
        """Check transcript structure quality.

        Args:
            text: Transcript text

        Returns:
            Check result
        """
        # Check for reasonable punctuation
        punctuation_ratio = len(re.findall(r"[.!?,;:]", text)) / len(text)
        
        # Check for excessive special characters
        special_chars = len(re.findall(r"[^a-zA-Z0-9\s.!?,;:'-]", text))
        
        # Structure is good if punctuation is reasonable and not too many special chars
        structure_good = 0.01 <= punctuation_ratio <= 0.1 and special_chars < len(text) * 0.1

        return {
            "passed": structure_good,
            "punctuation_ratio": round(punctuation_ratio, 3),
            "special_char_count": special_chars,
            "special_char_ratio": round(special_chars / len(text), 3) if text else 0,
        }

    @staticmethod
    def _calculate_quality_score(checks: Dict[str, Any]) -> float:
        """Calculate overall quality score.

        Args:
            checks: Dictionary of check results

        Returns:
            Quality score 0-1
        """
        scores = []
        for check in checks.values():
            if "passed" in check:
                scores.append(1.0 if check["passed"] else 0.0)

        return sum(scores) / len(scores) if scores else 0.0

    @staticmethod
    def _get_issues(checks: Dict[str, Any]) -> List[str]:
        """Get list of quality issues.

        Args:
            checks: Dictionary of check results

        Returns:
            List of issues found
        """
        issues = []
        
        if not checks["length_check"]["passed"]:
            issues.append("Transcript length is outside acceptable range")
        if not checks["content_check"]["passed"]:
            issues.append("Content quality indicators are not met")
        if not checks["encoding_check"]["passed"]:
            issues.append("Encoding issues detected")
        if not checks["structure_check"]["passed"]:
            issues.append("Structure quality is below threshold")

        return issues

    @staticmethod
    def _get_recommendations(checks: Dict[str, Any]) -> List[str]:
        """Get recommendations for improvement.

        Args:
            checks: Dictionary of check results

        Returns:
            List of recommendations
        """
        recommendations = []

        if not checks["length_check"]["passed"]:
            recommendations.append("Ensure transcript has sufficient content (min 100 chars)")
        if not checks["content_check"]["passed"]:
            recommendations.append("Review content for coherence and meaningful text")
        if not checks["encoding_check"]["passed"]:
            recommendations.append("Fix character encoding issues")
        if not checks["structure_check"]["passed"]:
            recommendations.append("Improve punctuation and remove excessive special characters")

        return recommendations
