"""Storage management for processing results."""

import json
import csv
import os
from typing import Any, Dict
from datetime import datetime
from utils.logger import get_logger


class StorageManager:
    """Manages storage of processing results."""

    def __init__(self, storage_type: str = "json", output_dir: str = "./results"):
        """Initialize storage manager.

        Args:
            storage_type: Type of storage ('json', 'csv', 'database')
            output_dir: Directory for output files
        """
        self.storage_type = storage_type
        self.output_dir = output_dir
        self.logger = get_logger("storage")
        os.makedirs(output_dir, exist_ok=True)

    def save(self, video_id: str, data: Dict[str, Any]) -> bool:
        """Save processing results.

        Args:
            video_id: YouTube video ID
            data: Results dictionary

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.storage_type == "json":
                return self._save_json(video_id, data)
            elif self.storage_type == "csv":
                return self._save_csv(video_id, data)
            else:
                self.logger.error(f"Unknown storage type: {self.storage_type}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to save results: {str(e)}")
            return False

    def _save_json(self, video_id: str, data: Dict[str, Any]) -> bool:
        """Save results as JSON.

        Args:
            video_id: YouTube video ID
            data: Results dictionary

        Returns:
            True if successful
        """
        filename = os.path.join(self.output_dir, f"{video_id}.json")
        with open(filename, "w") as f:
            json.dump(data, f, indent=2, default=str)
        self.logger.info(f"Results saved to {filename}")
        return True

    def _save_csv(self, video_id: str, data: Dict[str, Any]) -> bool:
        """Save results as CSV.

        Args:
            video_id: YouTube video ID
            data: Results dictionary

        Returns:
            True if successful
        """
        filename = os.path.join(self.output_dir, f"{video_id}.csv")
        
        # Flatten nested data for CSV
        flattened = self._flatten_dict(data)
        
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=flattened.keys())
            writer.writeheader()
            writer.writerow(flattened)
        
        self.logger.info(f"Results saved to {filename}")
        return True

    @staticmethod
    def _flatten_dict(d: Dict, parent_key: str = "", sep: str = "_") -> Dict:
        """Flatten nested dictionary.

        Args:
            d: Dictionary to flatten
            parent_key: Parent key prefix
            sep: Separator for keys

        Returns:
            Flattened dictionary
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(
                    StorageManager._flatten_dict(v, new_key, sep=sep).items()
                )
            elif isinstance(v, list):
                items.append((new_key, json.dumps(v)))
            else:
                items.append((new_key, v))
        return dict(items)

    def load(self, video_id: str) -> Dict[str, Any]:
        """Load previously saved results.

        Args:
            video_id: YouTube video ID

        Returns:
            Results dictionary or empty dict if not found
        """
        if self.storage_type == "json":
            filename = os.path.join(self.output_dir, f"{video_id}.json")
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    return json.load(f)
        return {}
