
from mcp.server.fastmcp import FastMCP
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import SKLearnVectorStore
import os

# Define common path to the repo locally
PATH = "/Users/visweshwarganesh/Development/MCP/paychex_docs_mcp_tool/notebook/"

# Create an MCP server
mcp = FastMCP("Paychex-Docs-MCP-Server")

# Add a tool to query the Paychex documentation
@mcp.tool()
def paychex_query_tool(query: str):
    """
    Query the Paychex documentation using a retriever.
    
    Args:
        query (str): The query to search the documentation with

    Returns:
        str: A str of the retrieved documents
    """
    embeddings = AzureOpenAIEmbeddings( 
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        #api_version=os.getenv("AZURE_OPENAI_VERSION"),
    )
    retriever = SKLearnVectorStore(
        embedding=embeddings, 
        persist_path=PATH + "sklearn_vectorstore.parquet", 
        serializer="parquet").as_retriever(search_kwargs={"k": 3}
        )

    relevant_docs = retriever.invoke(query)
    print(f"Retrieved {len(relevant_docs)} relevant documents")
    formatted_context = "\n\n".join([f"==DOCUMENT {i+1}==\n{doc.page_content}" for i, doc in enumerate(relevant_docs)])
    return formatted_context

# The @mcp.resource() decorator is meant to map a URI pattern to a function that provides the resource content
@mcp.resource("docs://paychex/full")
def get_all_paychex_docs() -> str:
    """
    Get all the Paychex documentation. Returns the contents of the file llms_full.txt,
    which contains a curated set of paychex documentation (~300k tokens). This is useful
    for a comprehensive response to questions about paychex.

    Args: None

    Returns:
        str: The contents of the Paychex documentation
    """

    # Local path to the Paychex documentation
    doc_path = PATH + "payx_docs.txt"
    try:
        with open(doc_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading log file: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')