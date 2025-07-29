from bs4 import BeautifulSoup


async def extract_titles(soup: BeautifulSoup) -> list[str]:
    return [
        title.get_text(strip=True)
        for title in soup.select(".tt")  # ou ".bigor .tt" para ser mais específico
    ]


async def extract_links(soup: BeautifulSoup) -> list[str]:
    return [
        str(a["href"])
        for a in soup.select("div.bs > div.bsx > a")
        if a.has_attr("href")
    ]


async def extract_cover_search(soup: BeautifulSoup) -> list[str]:
    return [
        str(img["src"])
        for item in soup.select("div.bsx")
        if (img := item.select_one("div.limit img.ts-post-image"))
        and img.has_attr("src")
    ]


async def extract_scores(soup: BeautifulSoup) -> list[float]:
    """Extrai as pontuações numéricas dos mangás"""
    scores = []
    for item in soup.select("div.bsx"):
        # Encontra a div de rating dentro de cada item
        rating_div = item.select_one(".rating .numscore")
        if rating_div:
            try:
                # Tenta converter o texto para float
                score = float(rating_div.get_text(strip=True))
                scores.append(score)
            except (ValueError, AttributeError):
                scores.append(0.0)  # Valor padrão se não conseguir converter
    return scores


async def extract_chapters(soup: BeautifulSoup) -> list[str]:
    return [
        chapter.get_text(strip=True)
        for chapter in soup.select(".epxs")  # Os capítulos estão na div com classe epxs
    ]


async def extract_pagination(soup: BeautifulSoup) -> list[str]:
    return [
        page.get_text(strip=True)
        for page in soup.select(
            ".page-numbers"
        )  # Os capítulos estão na div com classe epxs
    ]
