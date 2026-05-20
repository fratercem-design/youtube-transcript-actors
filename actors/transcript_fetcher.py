"""Actor for fetching YouTube transcripts."""

from typing import Any, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from .base import BaseActor


class TranscriptFetcher(BaseActor):
    """Fetches transcripts from YouTube videos."""

    def __init__(self, name: str = "transcript_fetcher"):
        """Initialize transcript fetcher actor.

        Args:
            name: Name of the actor
        """
        super().__init__(name, "transcript_fetcher")

    def process(self, input_data: Any) -> Dict[str, Any]:
        """Fetch transcript from YouTube video.

        Args:
            input_data: Dictionary with 'video_id' key or a video ID string

        Returns:
            Dictionary with transcript data
        """
        # Handle both string and dict inputs
        if isinstance(input_data, str):
            video_id = input_data
        elif isinstance(input_data, dict):
            video_id = input_data.get("video_id")
        else:
            raise ValueError("Input must be a video ID string or dict with 'video_id' key")

        if not video_id:
            raise ValueError("video_id is required")

        try:
            # Fetch transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

            # Combine transcript entries
            full_text = " ".join([entry["text"] for entry in transcript_list])

            return {
                "video_id": video_id,
                "transcript": full_text,
                "entries_count": len(transcript_list),
                "transcript_entries": transcript_list,
                "raw_data": transcript_list,
            }
        except Exception as e:
            self.logger.error(f"Failed to fetch transcript for {video_id}: {str(e)}")
            raise
