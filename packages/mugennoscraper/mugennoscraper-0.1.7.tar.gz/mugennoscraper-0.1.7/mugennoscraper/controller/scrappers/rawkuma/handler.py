from mugennocore.model.interfaces import IPage  # type: ignore
from mugennocore.model.page import Page  # type: ignore
from mugennoscraper.controller.helper import convert_pagination_to_int_list
from mugennoscraper.controller.scrappers.rawkuma.const import (
    URL_AZ_DEEP,
    URL_SEARCH_DEEP,
)
from mugennoscraper.controller.scrappers.rawkuma.manga import (
    create_manga_instance,
    extract_last_chapter,
)
from mugennoscraper.controller.scrappers.rawkuma.page import extract_image_urls
from mugennoscraper.controller.scrappers.rawkuma.search import (
    extract_cover_search,
    extract_links,
    extract_pagination,
    extract_scores,
    extract_titles,
)
from mugennoscraper.model.interfaces import IMangaPage, ISearchPage
from mugennoscraper.model.search import Search
from mugennoscraper.model.search_page import SearchPage
from mugennoscraper.utils.html import get_html, parse_html


async def get_search(query: str, page: int = 1) -> ISearchPage:
    url = URL_SEARCH_DEEP.format(page=page, query=query)
    html = await get_html(url)
    soup = await parse_html(html)

    # Extrair todas as listas necessárias
    links = await extract_links(soup)
    covers = await extract_cover_search(soup)
    titles = await extract_titles(soup)
    scores = await extract_scores(soup)
    last_chapters = await extract_last_chapter(soup)

    # Criar lista de objetos usando compreensão de lista
    searchs = [
        Search(
            title=titles[i],
            url=links[i],
            cover_url=covers[i],
            score=scores[i],
            last_chapter=last_chapters[i],
        )
        for i in range(len(titles))
    ]
    pagination_str = await extract_pagination(soup)  # list[str]
    pagination = await convert_pagination_to_int_list(pagination_str)  # list[int]
    search_page = SearchPage(searchs, pagination)  # type: ignore
    return search_page


async def get_manga(url: str) -> IMangaPage:
    html = await get_html(url)
    soup = await parse_html(html)
    manga_page = await create_manga_instance(soup)
    return manga_page


async def get_az_list(letter: str, page: int = 1) -> ISearchPage:
    url = URL_AZ_DEEP.format(page=page, letter=letter)
    html = await get_html(url)
    soup = await parse_html(html)

    # Extrair todas as listas necessárias
    links = await extract_links(soup)
    covers = await extract_cover_search(soup)
    titles = await extract_titles(soup)
    scores = await extract_scores(soup)
    last_chapters = await extract_last_chapter(soup)

    # Criar lista de objetos usando compreensão de lista
    searchs = [
        Search(
            title=titles[i],
            url=links[i],
            cover_url=covers[i],
            score=scores[i],
            last_chapter=last_chapters[i],
        )
        for i in range(len(titles))
    ]
    pagination_str = await extract_pagination(soup)  # list[str]
    pagination = await convert_pagination_to_int_list(pagination_str)  # list[int]
    search_page = SearchPage(searchs, pagination)  # type: ignore
    return search_page


async def get_pages(url: str) -> list[IPage]:
    """Return the manga Page object"""
    html = await get_html(url)
    soup = await parse_html(html)
    links = await extract_image_urls(soup)
    pages = [
        Page(
            img_url=links[i],
            page_index=i,
        )
        for i in range(len(links))
    ]
    return pages
