from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from mugennocore.model.genre import Genre
from mugennocore.model.interfaces import IChapter


@dataclass(slots=True)
class Manga:
    title: str
    url: str
    cover: str
    synopsis: str
    language: str = "Unknown"
    status: str = "Unknown"
    rating: float = 0.0
    release_date: date = field(default_factory=datetime.now().date)
    last_update: date = field(default_factory=datetime.now().date)
    author: str = "Unknown"
    artists: str = "Unknown"
    serialization: str = "Unknown"
    genres: list[Genre] = field(default_factory=list)

    def update_info(
        self,
        title: Optional[str] = None,
        url: Optional[str] = None,
        synopsis: Optional[str] = None,
        cover: Optional[str] = None,
        language: Optional[str] = None,
        status: Optional[str] = None,
        rating: Optional[float] = None,
        release_date: Optional[str] = None,
        last_update: Optional[str] = None,
        author: Optional[str] = None,
        artists: Optional[str] = None,
        serialization: Optional[str] = None,
        genres: Optional[list[Genre]] = None,
    ) -> None:
        """Atualiza múltiplos campos do mangá de uma vez."""
        if title is not None:
            self.title = title
        if url is not None:
            self.url = url
        if synopsis is not None:
            self.synopsis = synopsis
        if cover is not None:
            self.cover = cover
        if language is not None:
            self.language = language
        if status is not None:
            self.status = status
        if rating is not None:
            self.rating = rating
        if release_date is not None:
            self.release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
        if last_update is not None:
            self.last_update = datetime.strptime(last_update, "%Y-%m-%d").date()
        if author is not None:
            self.author = author
        if artists is not None:
            self.artists = artists
        if serialization is not None:
            self.serialization = serialization
        if genres is not None:
            self.genres = genres

    def __str__(self) -> str:
        return (
            f"{self.title}\n"
            f"{self.cover}\n"
            f"Genres: {', '.join(genre.value for genre in self.genres)}"
        )

    def __repr__(self) -> str:
        return (
            f"Manga(\n"
            f"  title={repr(self.title)},\n"
            f"  url={repr(self.url)},\n"
            f"  status={repr(self.status)},\n"
            f"  rating={self.rating},\n"
            f"  genres={[g.value for g in self.genres]},\n"
            f"  author={repr(self.author)},\n"
            f"  release_date={self.release_date.isoformat()},\n"
            f")"
        )

    def detailed_info(self) -> str:
        """Método adicional para exibição formatada completa."""
        return f"""
📖 {self.title.upper()}
{'=' * (len(self.title) + 2)}

🔗 URL: {self.url}
✍️ Autor(es): {self.author}
🎨 Artista(s): {self.artists}
📰 Serialização: {self.serialization}
📌 Status: {self.status}
⭐ Nota: {self.rating}
🏷️ Gêneros: {', '.join(genre.value for genre in self.genres)}
🌐 Idioma: {self.language}

📝 Sinopse:
{self.synopsis}

🗓️ Data de Lançamento: {self.release_date}
🔄 Última Atualização: {self.last_update}
"""
