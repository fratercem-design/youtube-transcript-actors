"""Main entry point for YouTube transcript analysis."""

import argparse
import json
from actors.orchestrator import TranscriptOrchestrator
from utils.logger import get_logger


logger = get_logger("main")


def main():
    """Main function to run transcript analysis."""
    parser = argparse.ArgumentParser(
        description="YouTube Transcript Analysis System"
    )
    parser.add_argument(
        "--video-id",
        type=str,
        help="YouTube video ID to analyze",
        required=False,
    )
    parser.add_argument(
        "--batch",
        type=str,
        help="Path to JSON file with list of video IDs",
        required=False,
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./results",
        help="Output directory for results",
    )
    parser.add_argument(
        "--storage",
        type=str,
        default="json",
        choices=["json", "csv"],
        help="Storage format for results",
    )

    args = parser.parse_args()

    # Initialize orchestrator
    orchestrator = TranscriptOrchestrator(
        storage_type=args.storage,
        output_dir=args.output,
    )

    if args.video_id:
        # Process single video
        logger.info(f"Processing video: {args.video_id}")
        result = orchestrator.process_video(args.video_id)
        print(json.dumps(result, indent=2, default=str))

    elif args.batch:
        # Process batch of videos
        try:
            with open(args.batch, "r") as f:
                video_ids = json.load(f)
            logger.info(f"Processing batch of {len(video_ids)} videos")
            results = orchestrator.process_batch(video_ids)
            print(json.dumps(results, indent=2, default=str))
        except FileNotFoundError:
            logger.error(f"Batch file not found: {args.batch}")
            return
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in batch file: {args.batch}")
            return
    else:
        print("Please provide either --video-id or --batch argument")
        parser.print_help()


if __name__ == "__main__":
    main()
