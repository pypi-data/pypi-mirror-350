import os
import sys
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_core.documents import Document
from mcp.server.fastmcp import FastMCP

from .pdf import PDFRetrievalChain

load_dotenv()

# 파일시스템 경로 가져오기 (MCP 서버가 시작될 때 전달됨)
def get_filesystem_path() -> str:
    """
    Get the filesystem path from command line arguments.
    In MCP, this is passed as an argument when the server is started.
    """
    # claude_desktop_config.json의 args 마지막에 지정한 경로가 여기로 전달됨
    if len(sys.argv) > 1:
        return sys.argv[-1]
    return os.getcwd()  # 기본값으로 현재 디렉토리 사용

filesystem_path = get_filesystem_path()

# 해당 경로 안에 데이터 디렉토리와 벡터 스토어 디렉토리 생성
DATA_DIR = Path(filesystem_path) / "data"
pdf_files = list(DATA_DIR.glob("*.pdf"))
pdf_paths = [str(path) for path in pdf_files]

VECTOR_DIR = Path(filesystem_path) / "vector_store"


rag_chain = PDFRetrievalChain(
    source_uri = pdf_paths,
    persist_directory = str(VECTOR_DIR),
    k = 5,
    embedding_model = "text-embedding-3-small",
).initialize()

mcp = FastMCP(
    name="RAG",
    description="RAG Hybrid Search"
)

def format_search_results(docs: List[Document]) -> str:
    """
    Format search results as markdown.
    
    Args:
        docs: List of documents to format
        
    Returns:
        Markdown formatted search results

    """

    if not docs:
        return "No relevant information found."
    
    markdown_results = "## Search Results\n\n"
    
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown source")
        page = doc.metadata.get("page", None)
        page_info = f" (Page: {page+1})" if page is not None else ""
        
        markdown_results += f"### Result {i}{page_info}\n\n"
        markdown_results += f"{doc.page_content}\n\n"
        markdown_results += f"Source: {source}\n\n"
        markdown_results += "---\n\n"
    
    return markdown_results


@mcp.tool()
async def hybrid_search(query: str, top_k: int = 5) -> str:
    """
    Performs hybrid search (keyword + semantic) on PDF documents.
    Combines exact keyword matching and semantic similarity to deliver optimal results.
    The most versatile search option for general questions or when unsure which search type is best.
    
    Parameters:
        query: Search query
        top_k: Number of results to return

    """

    try:
        results = rag_chain.search_hybrid(query, top_k)
        return format_search_results(results)
    except Exception as e:
        return f"An error occurred during search: {str(e)}"

def serve():
    mcp.run(transport="stdio")
    
if __name__ == "__main__":
    serve()
