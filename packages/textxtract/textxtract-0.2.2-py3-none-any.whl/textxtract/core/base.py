"""Abstract base classes for text extraction."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union


class FileTypeHandler(ABC):
    """Abstract base class for file type-specific handlers."""

    @abstractmethod
    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        """Extract text synchronously from a file."""
        pass

    @abstractmethod
    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        """Extract text asynchronously from a file."""
        pass


class TextExtractor(ABC):
    """Abstract base class for text extractors."""

    @abstractmethod
    def extract(
        self,
        source: Union[Path, str, bytes],
        filename: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> str:
        """Extract text synchronously from file path or bytes."""
        pass
