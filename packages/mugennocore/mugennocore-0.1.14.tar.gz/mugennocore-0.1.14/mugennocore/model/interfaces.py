from abc import abstractmethod
from datetime import date
from typing import Optional, Protocol, runtime_checkable

from mugennocore.model.genre import Genre


@runtime_checkable
class IChapter(Protocol):
    """Interface Protocol para um capítulo de mangá."""

    url: str
    download_url: str
    title: str
    index: float
    release_date: str
    cover: Optional[str]

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


@runtime_checkable
class IManga(Protocol):
    """Interface protocol to represent a Manga General Data"""

    title: str
    url: str
    cover: str
    synopsis: str
    language: str
    status: str
    rating: float
    chapters: Optional[list[IChapter]]
    release_date: date
    last_update: date
    author: str
    artists: str
    serialization: str
    genres: list[Genre]

    def update_info(self, **kwargs) -> None: ...
    def detailed_info(self) -> str: ...


@runtime_checkable
class IPage(Protocol):
    """Interface Protocol para uma página de mangá."""

    img_url: str
    page_index: float
    img_binary: Optional[bytes] = None

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
