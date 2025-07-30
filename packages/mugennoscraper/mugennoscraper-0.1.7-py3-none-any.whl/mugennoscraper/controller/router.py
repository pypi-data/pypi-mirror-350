from mugennoscraper.model.interfaces import ISearchPage  # type: ignore
from mugennoscraper.controller.scrappers.rawkuma.handler import (
    get_search,
    get_az_list,
)
from mugennoscraper.controller.helper import (
    Sources,
    extract_az_params,
    extract_search_params,
    check_source,
)


async def search_query(query: str) -> ISearchPage:
    title, source, lang, page, include_nsfw = await extract_search_params(query)
    source_enum = await check_source(source, lang)

    if source_enum == Sources.RAWKUMA:
        return await get_search(title, page)

    return await get_search(title, page)


async def az_query(query: str) -> ISearchPage:
    letter, source, lang, page, include_nsfw = await extract_az_params(query)
    source_enum = await check_source(source, lang)

    if source_enum == Sources.RAWKUMA:
        return await get_az_list(letter, page)

    return await get_az_list(letter, page)
