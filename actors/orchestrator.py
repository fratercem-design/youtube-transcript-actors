"""Orchestrator for coordinating all transcript processing actors."""

from typing import Any, Dict, Optional
from datetime import datetime
from .transcript_fetcher import TranscriptFetcher
from .data_cleaner import DataCleaner
from .sentiment_analyzer import SentimentAnalyzer
from .topic_extractor import TopicExtractor
from .summarizer import Summarizer
from .quality_validator import QualityValidator
from utils.logger import get_logger
from utils.storage import StorageManager


class TranscriptOrchestrator:
    """Orchestrates the workflow of all actors in the transcript processing pipeline."""

    def __init__(self, storage_type: str = "json", output_dir: str = "./results"):
        """Initialize orchestrator with all actors.

        Args:
            storage_type: Type of storage ('json', 'csv', 'database')
            output_dir: Directory for output files
        """
        self.logger = get_logger("orchestrator")
        self.storage = StorageManager(storage_type, output_dir)

        # Initialize all actors
        self.fetcher = TranscriptFetcher()
        self.cleaner = DataCleaner()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.topic_extractor = TopicExtractor()
        self.summarizer = Summarizer()
        self.validator = QualityValidator()

        self.actors = [
            self.fetcher,
            self.cleaner,
            self.sentiment_analyzer,
            self.topic_extractor,
            self.summarizer,
            self.validator,
        ]

    def process_video(self, video_id: str) -> Dict[str, Any]:
        """Process a complete video through the entire pipeline.

        Args:
            video_id: YouTube video ID

        Returns:
            Dictionary with complete analysis results
        """
        self.logger.info(f"Starting pipeline for video: {video_id}")

        pipeline_start = datetime.now()
        results = {"video_id": video_id, "started_at": pipeline_start.isoformat()}

        try:
            # Stage 1: Fetch transcript
            self.logger.info("Stage 1: Fetching transcript")
            fetch_result = self.fetcher.execute(video_id)
            if fetch_result["status"] == "error":
                self.logger.error(f"Failed to fetch transcript: {fetch_result['error']}")
                return {**results, "status": "error", "error": fetch_result["error"]}

            # Stage 2: Clean data
            self.logger.info("Stage 2: Cleaning transcript data")
            clean_result = self.cleaner.execute(fetch_result)
            if clean_result["status"] == "error":
                return {**results, "status": "error", "error": clean_result["error"]}

            # Stage 3: Validate quality
            self.logger.info("Stage 3: Validating transcript quality")
            validation_result = self.validator.execute(clean_result)
            if validation_result["status"] == "error":
                return {**results, "status": "error", "error": validation_result["error"]}

            if not validation_result.get("is_valid"):
                self.logger.warning(
                    f"Transcript quality validation failed: {validation_result.get('issues')}"
                )

            # Stage 4: Sentiment analysis
            self.logger.info("Stage 4: Analyzing sentiment")
            sentiment_result = self.sentiment_analyzer.execute(clean_result)

            # Stage 5: Extract topics
            self.logger.info("Stage 5: Extracting topics")
            topic_result = self.topic_extractor.execute(clean_result)

            # Stage 6: Generate summary
            self.logger.info("Stage 6: Generating summary")
            summary_result = self.summarizer.execute(clean_result)

            # Compile results
            results = {
                **results,
                "status": "success",
                "transcript": {
                    "original_length": fetch_result.get("entries_count", 0),
                    "cleaned_transcript": clean_result.get("transcript", "")[:500],  # First 500 chars
                    "cleaning_stats": clean_result.get("cleaning_stats", {}),
                },
                "quality": {
                    "is_valid": validation_result.get("is_valid", False),
                    "quality_score": validation_result.get("quality_score", 0),
                    "issues": validation_result.get("issues", []),
                    "recommendations": validation_result.get("recommendations", []),
                },
                "sentiment": sentiment_result.get("overall_sentiment", {}),
                "topics": topic_result.get("key_terms", []),
                "summary": {
                    "short": summary_result.get("short_summary", ""),
                    "medium": summary_result.get("medium_summary", ""),
                    "long": summary_result.get("long_summary", ""),
                },
            }

            # Save results
            self.storage.save(video_id, results)

            # Calculate pipeline stats
            pipeline_end = datetime.now()
            results["completed_at"] = pipeline_end.isoformat()
            results["processing_time_seconds"] = (
                pipeline_end - pipeline_start
            ).total_seconds()
            results["actor_stats"] = [actor.get_stats() for actor in self.actors]

            self.logger.info(f"Pipeline completed successfully for video: {video_id}")
            return results

        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            return {**results, "status": "error", "error": str(e)}

    def process_batch(self, video_ids: list) -> list:
        """Process multiple videos.

        Args:
            video_ids: List of YouTube video IDs

        Returns:
            List of results for each video
        """
        results = []
        for video_id in video_ids:
            result = self.process_video(video_id)
            results.append(result)
        return results

    def get_actor_stats(self) -> Dict[str, Any]:
        """Get statistics for all actors.

        Returns:
            Dictionary with stats for each actor
        """
        return {"actors": [actor.get_stats() for actor in self.actors]}
