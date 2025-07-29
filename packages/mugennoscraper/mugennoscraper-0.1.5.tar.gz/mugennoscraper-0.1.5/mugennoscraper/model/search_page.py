from dataclasses import dataclass
from mugennoscraper.model.interfaces import ISearch


@dataclass(slots=True)
class SearchPage:
    searchs: list[ISearch]
    pagination: list[int]

    def __str__(self) -> str:
        results_str = "\n".join(str(result) for result in self.searchs)
        return f"""
{results_str}
{'==='* len(self.pagination)}
{self.pagination}
"""

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"  search_results={repr(self.searchs)},\n"
            f"  pagination={repr(self.pagination)}\n"
            f")"
        )
