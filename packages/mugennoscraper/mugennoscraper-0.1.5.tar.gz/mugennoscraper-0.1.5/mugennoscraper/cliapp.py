import asyncio
import typer
import mugennoscraper.controller.scrappers.rawkuma.handler as handler
from mugennoscraper.controller.router import search_query, az_query

app = typer.Typer()  # Cria um app principal


@app.command()
def search(query: str, page: int = 1):
    """Busca títulos de mangá com a query dada."""

    async def run():
        resp = await handler.get_search(query, page)
        print(resp)

    asyncio.run(run())


@app.command()
def manga(url: str):
    """Busca detalhes de um mangá dado a URL."""

    async def run():
        resp = await handler.get_manga(url)
        print(resp)
        print("".join(f"{str(v)}" for v in resp.chapters))

    asyncio.run(run())


@app.command()
def pages(url: str):
    """Busca paginas de um mangá dado a URL do chapter."""

    async def run():
        resp = await handler.get_pages(url)
        print(resp)

    asyncio.run(run())


@app.command()
def az_list(letter: str, page: int = 1):
    """Busca títulos de mangá com a letra dada."""

    async def run():
        resp = await handler.get_az_list(letter, page)
        print(resp)

    asyncio.run(run())


@app.command()
def query(query: str):
    "Busca mangas"

    async def run():
        resp = await search_query(query)
        print(resp)

    asyncio.run(run())


@app.command()
def query_letter(query: str):
    "Busca mangas"

    async def run():
        resp = await az_query(query)
        print(resp)

    asyncio.run(run())


@app.command()
def query_az(query: str):
    "Busca mangas"

    async def run():
        resp = await az_query(query)
        print(
            f"""
{'\n'.join(f'{str(result)}- URL: {result.url}' for result in resp.searchs)}     
     
{resp.pagination}
""")

    asyncio.run(run())


if __name__ == "__main__":
    app()
