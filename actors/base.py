"""Base actor class for all specialized actors."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
from utils.logger import get_logger


class BaseActor(ABC):
    """Abstract base class for all actors in the system."""

    def __init__(self, name: str, actor_type: str):
        """Initialize base actor.

        Args:
            name: Unique name for the actor instance
            actor_type: Type/role of the actor
        """
        self.name = name
        self.actor_type = actor_type
        self.logger = get_logger(name)
        self.created_at = datetime.now()
        self.processed_count = 0
        self.error_count = 0

    @abstractmethod
    def process(self, input_data: Any) -> Dict[str, Any]:
        """Process input data and return results.

        Args:
            input_data: Input data to process

        Returns:
            Dictionary with processing results
        """
        pass

    def execute(self, input_data: Any) -> Dict[str, Any]:
        """Execute the actor with error handling.

        Args:
            input_data: Input data to process

        Returns:
            Dictionary with results or error information
        """
        try:
            self.logger.info(f"Processing started for {self.name}")
            result = self.process(input_data)
            self.processed_count += 1
            result["actor"] = self.name
            result["actor_type"] = self.actor_type
            result["timestamp"] = datetime.now().isoformat()
            result["status"] = "success"
            self.logger.info(f"Processing completed for {self.name}")
            return result
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Error in {self.name}: {str(e)}")
            return {
                "actor": self.name,
                "actor_type": self.actor_type,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def get_stats(self) -> Dict[str, Any]:
        """Get actor statistics.

        Returns:
            Dictionary with actor statistics
        """
        return {
            "name": self.name,
            "type": self.actor_type,
            "created_at": self.created_at.isoformat(),
            "processed_count": self.processed_count,
            "error_count": self.error_count,
            "success_rate": (
                self.processed_count
                / (self.processed_count + self.error_count)
                if (self.processed_count + self.error_count) > 0
                else 0
            ),
        }
