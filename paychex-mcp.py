
from mcp.server.fastmcp import FastMCP
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import SKLearnVectorStore
import os
import truststore
truststore.inject_into_ssl()

# Define common path to the repo locally
# Security: Get base path from environment variable or use current directory
BASE_PATH = os.getenv("MCP_BASE_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "notebook"))
# Normalize and resolve the path to prevent directory traversal
BASE_PATH = os.path.normpath(os.path.realpath(BASE_PATH))
# Create an MCP server
mcp = FastMCP("Paychex-Docs-MCP-Server")

# Add a tool to query the Paychex documentation
mcp.description = "Paychex documentation query tool"

def validate_path(file_path: str) -> str:
    """
    Validate that a file path is within the allowed base directory.
    Prevents path traversal attacks.
    
    Args:
        file_path (str): The file path to validate
        
    Returns:
        str: The validated absolute path
        
    Raises:
        ValueError: If the path is outside the allowed directory
    """
    # Resolve the full path
    full_path = os.path.normpath(os.path.realpath(os.path.join(BASE_PATH, file_path)))
    
    # Use commonpath to ensure the path is within BASE_PATH
    # This handles case-insensitive filesystems and symlinks properly
    try:
        common = os.path.commonpath([BASE_PATH, full_path])
        if common != BASE_PATH:
            raise ValueError("Access denied: Path traversal detected")
    except ValueError:
        # commonpath raises ValueError if paths are on different drives (Windows)
        raise ValueError("Access denied: Path traversal detected")
    
    return full_path

@mcp.tool()
def paychex_query_tool(query: str):
    """
    Query the Paychex documentation using a retriever.
    
    Args:
        query (str): The query to search the documentation with

    Returns:
        str: A str of the retrieved documents
    """
    try:
        # Security: Validate API credentials exist before use
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
        
        if not all([api_key, endpoint, deployment]):
            return "Error: Missing required Azure OpenAI configuration"
        
        embeddings = AzureOpenAIEmbeddings( 
            api_key=api_key,
            azure_endpoint=endpoint,
            azure_deployment=deployment,
        )
        
        # Security: Validate the vector store path
        vectorstore_path = validate_path("sklearn_vectorstore.parquet")
        
        retriever = SKLearnVectorStore(
            embedding=embeddings, 
            persist_path=vectorstore_path, 
            serializer="parquet").as_retriever(search_kwargs={"k": 3}
            )

        relevant_docs = retriever.invoke(query)
        print(f"Retrieved {len(relevant_docs)} relevant documents")
        formatted_context = "\n\n".join([f"==DOCUMENT {i+1}==\n{doc.page_content}" for i, doc in enumerate(relevant_docs)])
        return formatted_context
    except ValueError:
        # Security error (path traversal) - don't expose details
        return "Security error: Access denied"
    except FileNotFoundError:
        return "File access error: Required data file not found"
    except Exception as e:
        # Generic errors - don't expose internal details
        return "Configuration error: Unable to process query"

# The @mcp.resource() decorator is meant to map a URI pattern to a function that provides the resource content
@mcp.resource("docs://paychex/full")
def get_all_paychex_docs() -> str:
    """
    Get all the Paychex documentation. Returns the contents of the file payx_docs.txt,
    which contains a curated set of paychex documentation (~300k tokens). This is useful
    for a comprehensive response to questions about paychex.

    Args: None

    Returns:
        str: The contents of the Paychex documentation
    """
    try:
        # Security: Validate the documentation path to prevent path traversal
        doc_path = validate_path("payx_docs.txt")
        
        with open(doc_path, 'r', encoding='utf-8') as file:
            return file.read()
    except ValueError:
        # Security error (path traversal detected) - don't expose details
        return "Security error: Access denied"
    except FileNotFoundError:
        return "File access error: Documentation file not found"
    except PermissionError:
        return "File access error: Permission denied"
    except Exception as e:
        # Generic errors - don't expose internal details
        return "Configuration error: Unable to read documentation"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')