from firecrawl import FirecrawlApp, ScrapeOptions
from firecrawl import AsyncFirecrawlApp
from firecrawl import ScrapeOptions
import asyncio
import os
from lightrag.lightrag import LightRAG, QueryParam
from lightrag.llm.azure_openai import azure_openai_complete, azure_openai_embed
from lightrag.kg.shared_storage import initialize_pipeline_status
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("lightrag-mm-cs")

async def initialize_rag():
    WORKING_DIR = "./mm-cs"
    if not os.path.exists(WORKING_DIR):
        os.mkdir(WORKING_DIR)

    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=azure_openai_embed,
        llm_model_func=azure_openai_complete,
    )
    await rag.initialize_storages()
    await initialize_pipeline_status()
    return rag

async def extract_cs():
    app = AsyncFirecrawlApp(api_key='fc-1f35331013174fa285d4e2df0f162f5a')
    response = await app.crawl_url(
        url='https://www.marimekko.com/fi_fi/cs',
        limit=10,
        include_paths=['cs/.+'],
        scrape_options=ScrapeOptions(
            onlyMainContent=True,
            includeTags=['#mainContent'],
            formats=['markdown', 'rawHtml'],
            excludeTags=['img']
        )
    )

    with open('mm_cs.txt', 'w', encoding='utf-8', newline='\n') as file:
        file.write('')

    for document in response.data:
        with open('mm_cs.txt', 'a', encoding='utf-8') as file:
            file.write(document.markdown + '\r\n')

    print("Extracted content has been saved to mm_cs.txt")


@mcp.tool()
async def query(q: str):
    """Search information related to the query.

    Args:
        q: query/question that needs to be queried.

    Returns:
        Information related to the query/question.
    """
    rag = await initialize_rag()
    mode = "hybrid"

    return await rag.aquery(
            q,
            param=QueryParam(mode=mode)
        )

async def main2():
    rag = await initialize_rag()
    '''with open("mm_cs.txt", "r", encoding="utf-8") as f:''
        content = f.read()
        await rag.ainsert(content)'''

    mode = "hybrid"
    print(
        await rag.aquery(
            "What are available payment methods?",
            param=QueryParam(mode=mode)
        )
    )

def main():
    mcp.run(transport="stdio")

'''if __name__ == "__main__":
    # asyncio.run(main())
    mcp.run(transport="stdio")'''
