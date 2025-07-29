from abc import abstractmethod
from typing import Protocol, runtime_checkable
from mugennocore.model.interfaces import IPage, IManga, IChapter  # type: ignore


@runtime_checkable
class ISearch(Protocol):
    """Interface for data in search results."""

    title: str
    url: str
    cover_url: str
    score: float
    last_chapter: str

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


@runtime_checkable
class ISearchPage(Protocol):
    """Interface for search results page with pagination support."""

    # Atributos obrigatórios (type hints apenas)
    searchs: list[ISearch]
    pagination: list[int]

    @abstractmethod
    def __str__(self) -> str:
        """User-friendly string representation."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        pass


@runtime_checkable
class IChapterPage(Protocol):
    """Interface for chapters page with pagination support."""

    # Atributos obrigatórios (type hints apenas)
    chapter: IChapter
    pages: list[IPage]

    @abstractmethod
    def __str__(self) -> str:
        """User-friendly string representation."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        pass


@runtime_checkable
class IMangaPage(Protocol):
    """Interface for manga page with meta and chapter data"""

    # Atributos obrigatórios (type hints apenas)
    manga: IManga
    chapters: list[IChapter]

    @abstractmethod
    def __str__(self) -> str:
        """User-friendly string representation."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        pass
