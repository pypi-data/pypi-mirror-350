from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Chapter:
    """Represents a Manga Chapter as a dataclass."""

    url: str
    download_url: str
    title: str
    index: float
    release_date: str = "N/A"
    cover: Optional[str] = None  # TODO: Implement covers based on first page

    def __str__(self) -> str:
        return f"\n{self.index} - {self.title}\nDownload zip: {self.download_url}\n"

    def __repr__(self) -> str:
        return (
            f"Chapter(\n"
            f"  title={repr(self.title)},\n"
            f"  index={self.index},\n"
            f"  url={repr(self.url)},\n"
            f"  download_url={repr(self.download_url)},\n"
            f"  release_date={self.release_date},\n"
            f")"
        )
