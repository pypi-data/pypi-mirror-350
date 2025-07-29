from bs4 import BeautifulSoup


async def extract_image_urls(soup: BeautifulSoup) -> list[str]:
    # Seleciona todas as tags <img> dentro de <p>
    images = soup.select("p img")
    return [str(img["src"]) for img in images if img.has_attr("src")]
