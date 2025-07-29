from dataclasses import dataclass
from mugennocore.model.interfaces import IPage, IChapter  # type: ignore


@dataclass(slots=True)
class ChaperPage:
    chapter: IChapter
    pages: list[IPage]

    def __str__(self) -> str:
        return f"""
{self.chapter.title}
{self.chapter.download_url}
{"\n".join(str(page) for page in self.pages)}
"""

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"  chapter={repr(self.chapter)},\n"
            f"  pages={repr(self.pages)}\n"
            f")"
        )
