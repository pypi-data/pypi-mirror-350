import logging
from bs4 import BeautifulSoup
from mugennocore.model.genre import Genre  # type: ignore
from mugennocore.model.manga import Manga  # type: ignore
from mugennocore.model.chapter import Chapter  # type: ignore

from mugennoscraper.model.interfaces import IMangaPage
from mugennoscraper.model.manga_page import MangaPage  # type: ignore


# Configure logging
logging.basicConfig(
    filename="debug.txt",
    level=logging.WARNING,
    format="%(asctime)s - %(message)s",
    encoding="utf-8",
)


async def create_manga_instance(soup: BeautifulSoup) -> IMangaPage:
    def handle_genre(genre_str: str) -> str:
        """Handle genre conversion with error logging."""
        try:
            return Genre[genre_str.upper().replace(" ", "_")]
        except KeyError:
            logging.warning("Genre not found: %s", genre_str)
            return Genre.UNKNOWN

    # Extract all data first
    raw_genres = await extract_genres(soup)

    manga = Manga(
        title=await extract_title(soup),
        url=await extract_url(soup),
        synopsis=await extract_synopsis(soup),
        cover=await extract_cover_manga(soup),
        language=await extract_language(soup),
        status=await extract_status(soup),
        rating=await extract_rating(soup),
        release_date=await extract_release_date(soup),
        last_update=await extract_last_update(soup),
        author=await extract_author(soup),
        artists=await extract_artists(soup),
        serialization=await extract_serialization(soup),
        genres=[handle_genre(genre) for genre in raw_genres],
    )
    chapters = (
        [
            Chapter(
                url=chapter_dict["url"],
                download_url=chapter_dict["download_url"],
                title=chapter_dict["title"],
                index=float(chapter_dict["number"]),  # Convertendo para float
                release_date=chapter_dict["date"],
            )
            for chapter_dict in await extract_chapters(soup)
        ],
    )
    return MangaPage(
        manga=manga,
        chapters=chapters,
    )


async def extract_title(soup: BeautifulSoup) -> str:
    title = soup.select_one(".entry-title")
    return title.get_text(strip=True) if title else ""


async def extract_url(soup: BeautifulSoup) -> str:
    url = soup.select_one("link[rel='canonical']")
    return str(url["href"]) if url and url.has_attr("href") else ""


async def extract_synopsis(soup: BeautifulSoup) -> str:
    synopsis = soup.select_one(".entry-content-single")
    return synopsis.get_text(strip=True) if synopsis else ""


async def extract_cover_manga(soup: BeautifulSoup) -> str:
    cover_img = soup.select_one(".wp-post-image")
    if cover_img and cover_img.has_attr("src"):
        return str(cover_img["src"])
    return ""


async def extract_language(soup: BeautifulSoup) -> str:
    # Assumindo que o idioma é inglês (não está explícito no HTML)
    return "No Implementation"


async def extract_status(soup: BeautifulSoup) -> str:
    status = soup.select_one(".imptdt i")
    return status.get_text(strip=True) if status else ""


async def extract_rating(soup: BeautifulSoup) -> float:
    rating = soup.select_one(".num")
    return float(rating.get_text(strip=True)) if rating else 0.0


async def extract_last_chapter(soup: BeautifulSoup) -> list[str]:
    return [
        (
            (chapter.get_text(strip=True).replace("Chapter", "").strip())
            if (chapter := item.select_one(".adds .epxs"))
            else ""
        )
        for item in soup.select("div.bsx")
    ]


async def extract_release_date(soup: BeautifulSoup) -> str:
    date = soup.select_one("time[itemprop='datePublished']")
    if date and date.has_attr("datetime"):
        return str(date["datetime"]).split("T")[0]
    return ""


async def extract_last_update(soup: BeautifulSoup) -> str:
    date = soup.select_one("time[itemprop='dateModified']")
    if date and date.has_attr("datetime"):
        return str(date["datetime"]).split("T")[0]
    return ""


async def extract_author(soup: BeautifulSoup) -> str:
    # Encontra o label "Author" e pega o span seguinte
    for div in soup.select("div.fmed"):
        if "Author" in div.get_text():
            author = div.select_one("span")
            return author.get_text(strip=True) if author else ""
    return ""


async def extract_artists(soup: BeautifulSoup) -> str:
    # Encontra o label "Artist" e pega o span seguinte
    for div in soup.select("div.fmed"):
        if "Artist" in div.get_text():
            artist = div.select_one("span")
            return artist.get_text(strip=True) if artist else ""
    return ""


async def extract_serialization(soup: BeautifulSoup) -> str:
    """Extrai a serialização do manga"""
    # Procura pelo label "Serialization" e pega o span ou link seguinte
    for div in soup.select("div.fmed"):
        if "Serialization" in div.get_text():
            serialization = div.select_one("span, a")  # Pega span ou link
            return serialization.get_text(strip=True) if serialization else "-"
    return "-"  # Retorna "-" como padrão quando não encontrado


async def extract_genres(soup: BeautifulSoup) -> list[str]:
    genres = []
    genre_tags = soup.select(".mgen a")
    for tag in genre_tags:
        genres.append(tag.get_text(strip=True))
    return genres


async def extract_chapters(soup: BeautifulSoup) -> list[dict]:
    chapters = []
    for li in soup.select("li[data-num]"):  # Seleciona todos os <li> com data-num
        chapter_num = li.get("data-num", "")
        chapternum = li.select_one(".chapternum")
        chapterdate = li.select_one(".chapterdate")
        chapter_url = li.select_one(".eph-num a")
        download_url = li.select_one(".dload")

        chapters.append(
            {
                "number": chapter_num,
                "title": chapternum.get_text(strip=True) if chapternum else "N/A",
                "date": chapterdate.get_text(strip=True) if chapterdate else "N/A",
                "url": chapter_url["href"] if chapter_url else "N/A",
                "download_url": download_url["href"] if download_url else "N/A",
            }
        )
    return chapters
