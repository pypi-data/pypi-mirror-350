from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Page:
    """Object to represent a Manga Page as a dataclass."""

    img_url: str
    page_index: float
    img_binary: Optional[bytes] = None  # Melhor tipo para binário seria bytes

    def __str__(self) -> str:
        return f"\n{self.img_url}\nPage: {self.page_index}\n"

    def __repr__(self) -> str:
        return (
            f"Page(\n"
            f"  img_url={repr(self.img_url)},\n"
            f"  page_index={self.page_index},\n"
            f"  img_binary={'<binary_data>' if self.img_binary else None},\n"
            f")"
        )
