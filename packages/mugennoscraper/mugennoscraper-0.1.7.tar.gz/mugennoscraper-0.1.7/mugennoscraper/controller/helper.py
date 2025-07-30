from enum import Enum
import re
from urllib.parse import quote
import warnings


class Sources(Enum):
    RAWKUMA = "rawkuma"


# Define as fontes suportadas e seus idiomas
SOURCES = {"rawkuma": {"en", "jp"}}


async def extract_search_params(query: str) -> tuple[str, str, str, int, bool]:
    """
    Extrai e trata parâmetros de busca, formatando o título para URLs.

    Formato esperado: "/title=One Piece&page?=3&source?=rawkuma&lang?=pt&nsfw?=true"

    Retorna:
    - title: str (formatado para URL)
    - source: str (padrão 'rawkuma')
    - lang: str (padrão 'en')
    - page: int (padrão 1)
    - include_nsfw: bool (padrão False)
    """
    # Regex para capturar parâmetros
    pattern = re.compile(r"(?:&|\?|^)(\w+)(?:\?)?=([^&]+)")
    matches = pattern.findall(f"?{query}" if query.startswith("/") else query)
    params = {key.lower(): value for key, value in matches}

    if "title" not in params:
        raise ValueError("title is not opcional (ex: title=One Piece)")

    # Codificação URL PROPER (trata espaços e caracteres especiais)
    title = quote(params["title"])

    # Parâmetros opcionais
    source = params.get("source", "rawkuma").lower()
    lang = params.get("lang", "en").lower()
    include_nsfw = params.get("nsfw", "false").lower() in ("true", "1", "yes")

    try:
        page = max(1, int(params.get("page", "1")))  # Garante página mínima = 1
    except ValueError:
        page = 1

    return title, source, lang, page, include_nsfw


async def extract_az_params(string: str) -> tuple[str, str, str, int, bool]:
    """
    Extrai parâmetros de busca A-Z de uma string no formato:
    "letter=A&source?=rawkuma&lang?=en&page?=1&nsfw?=true"

    Parâmetros obrigatórios:
    - letter: str (A-Z ou #)

    Parâmetros opcionais:
    - source: str (padrão 'rawkuma')
    - lang: str (padrão 'en')
    - page: int (padrão 1)
    - include_nsfw: bool (padrão False)

    Retorna:
    tuple (source, lang, letter, page, include_nsfw)

    Levanta:
    ValueError - Se o parâmetro 'letter' não for fornecido ou for inválido
    """
    # Regex para capturar parâmetros
    pattern = re.compile(r"(?:&|\?|^)(\w+)(?:\?)?=([^&]+)")
    matches = pattern.findall(f"?{string}" if string.startswith("/") else string)
    params = {key.lower(): value for key, value in matches}

    # Validação obrigatória do letter
    if "letter" not in params:
        raise ValueError("letter is not opcional (ex: letter=A)")

    letter = params["letter"].upper()
    if not (letter.isalpha() or letter.isdigit() or letter == "#"):
        raise ValueError("Letter must be: A-Z, 0-9 or '#'")

    if len(letter) > 1:
        raise ValueError("Letter should be a single character")

    # Parâmetros opcionais com defaults
    source = params.get("source", "rawkuma").lower()
    lang = params.get("lang", "en").lower()
    include_nsfw = params.get("nsfw", "false").lower() in ("true", "1", "yes")

    try:
        page = int(params.get("page", "1"))
    except ValueError:
        page = 1

    return letter, source, lang, page, include_nsfw


async def check_source(source: str, lang: str) -> Sources | None:
    "Verifica se a fonte e o idioma são válidos"
    if source in SOURCES and lang in SOURCES[source]:
        return Sources[source.upper()]
    return None


async def convert_pagination_to_int_list(pagination_list: list[str]) -> list[int]:
    """Converte lista de strings para inteiros, descartando valores inválidos com warning."""
    result = []
    for item in pagination_list:
        try:
            num = int(item)
            result.append(num)
        except ValueError:
            warnings.warn(
                f"Value discarted: {item}",
                UserWarning,
                stacklevel=2,
            )
    return result
