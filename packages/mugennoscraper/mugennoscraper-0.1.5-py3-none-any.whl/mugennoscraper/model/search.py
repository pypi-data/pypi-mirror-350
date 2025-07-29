from dataclasses import dataclass


@dataclass(slots=True)
class Search:
    """Represents a Search return Object"""

    title: str
    url: str
    cover_url: str
    score: float
    last_chapter: str

    def __str__(self) -> str:
        return f"""
{self.title}
{self.cover_url}
★ - {self.score} | 🕮 - {self.last_chapter}
"""

    def __repr__(self) -> str:
        return f"""
SearchObj(
    title={self.title!r}
    url={self.url!r}
    cover_url={self.cover_url!r}
    score={self.score!r}
    last_chapter={self.last_chapter!r}
)
"""
