from dataclasses import dataclass
from mugennocore.model.interfaces import IChapter, IManga  # type: ignore


@dataclass(slots=True)
class MangaPage:
    manga: IManga
    chapters: list[IChapter]

    def __str__(self) -> str:
        return f"""
{self.manga.title}
\nSinopses: {self.manga.synopsis}\n
{"\n".join(str(chapter) for chapter in self.chapters)}
"""

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"  manga={repr(self.manga)},\n"
            f"  chapters={repr(self.chapters)}\n"
            f")"
        )
