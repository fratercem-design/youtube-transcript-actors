# YouTube Transcript Actor Team

A specialized team of autonomous actors for YouTube transcript scraping, cleaning, analysis, and insights generation.

## Overview

This project implements a multi-actor system for comprehensive YouTube transcript processing:

- **Transcript Fetcher**: Retrieves transcripts from YouTube videos
- **Data Cleaner**: Normalizes and cleans transcript text
- **Sentiment Analyzer**: Analyzes emotional tone and sentiment
- **Topic Extractor**: Identifies key topics and themes
- **Summarizer**: Creates concise summaries of content
- **Quality Validator**: Validates data quality and completeness

## Architecture

Each actor operates as an independent specialized component with clear input/output contracts.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from actors.orchestrator import TranscriptOrchestrator

orchestrator = TranscriptOrchestrator()
results = orchestrator.process_video(video_id="dQw4w9WgXcQ")
```

## Project Structure

```
├── actors/
│   ├── __init__.py
│   ├── base.py                 # Base actor class
│   ├── transcript_fetcher.py   # YouTube transcript retrieval
│   ├── data_cleaner.py         # Text normalization
│   ├── sentiment_analyzer.py   # Sentiment analysis
│   ├── topic_extractor.py      # Topic extraction
│   ├── summarizer.py           # Summary generation
│   ├── quality_validator.py    # Quality validation
│   └── orchestrator.py         # Orchestration logic
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration
├── models/
│   ├── __init__.py
│   └── data_models.py          # Data structures
├── utils/
│   ├── __init__.py
│   ├── logger.py               # Logging setup
│   └── storage.py              # Storage operations
├── requirements.txt
├── main.py                     # Entry point
└── README.md
```

## Configuration

Set environment variables in `.env`:

```
YOUTUBE_API_KEY=your_api_key_here
STORAGE_TYPE=json  # json, csv, or database
OUTPUT_DIR=./results
```

## License

MIT
