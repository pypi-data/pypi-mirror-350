import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, List, Union, Dict, Any, Tuple

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.mcp import MCPServerStdio

# --- Configuration ---
def load_gemini_llm_config() -> GeminiModel:
    load_dotenv()
    # Default model, can be overridden by GEMINI_MODEL_NAME in .env
    # Keeping gemini-2.5-flash-preview-04-17 as per current content unless a change is explicitly requested.
    model_name = os.environ.get('GEMINI_MODEL_NAME', 'gemini-2.5-flash-preview-04-17')
    model = GeminiModel(
        model_name=model_name,
    )
    return model

# --- Agent Response Model (for Pydantic AI Agent's structured output) ---
# These models should now mirror the Pydantic models defined in doc_tool_server.py for tool outputs.

class OperationStatus(BaseModel):
    """Generic status for operations. Mirrors server model."""
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None

class ChapterMetadata(BaseModel):
    """Metadata for a chapter. Mirrors server model."""
    chapter_name: str
    title: Optional[str] = None
    word_count: int
    paragraph_count: int
    last_modified: str # Assuming datetime will be serialized to string by MCP/Pydantic

class LongDocumentInfo(BaseModel):
    """Metadata for a long document. Mirrors server model."""
    document_name: str
    total_chapters: int
    total_word_count: int
    total_paragraph_count: int
    last_modified: str # Assuming datetime will be serialized to string
    chapters: List[ChapterMetadata]

class ParagraphDetail(BaseModel):
    """Detailed information about a paragraph. Mirrors server model."""
    document_name: str
    chapter_name: str
    paragraph_index_in_chapter: int
    content: str
    word_count: int

class ChapterContent(BaseModel):
    """Content of a chapter file. Mirrors server model."""
    document_name: str
    chapter_name: str
    content: str
    word_count: int
    paragraph_count: int
    last_modified: str # Assuming datetime will be serialized to string

class FullLongDocumentContent(BaseModel):
    """Content of an entire long document. Mirrors server model."""
    document_name: str
    chapters: List[ChapterContent]
    total_word_count: int
    total_paragraph_count: int

class StatisticsReport(BaseModel):
    """Report for analytical queries. Mirrors server model."""
    scope: str
    word_count: int
    paragraph_count: int
    chapter_count: Optional[int] = None
    document_name: Optional[str] = None  # Added for compatibility
    chapter_name: Optional[str] = None   # Added for compatibility


# Define the DetailsType union for the FinalAgentResponse
# This will include all possible direct return types from the new tools.
DetailsType = Union[
    List[LongDocumentInfo],         # from list_long_documents
    Optional[List[ChapterMetadata]],# from list_chapters
    Optional[ChapterContent],       # from read_chapter_content
    Optional[ParagraphDetail],      # from read_paragraph_content
    Optional[FullLongDocumentContent],# from read_full_long_document
    OperationStatus,                # from all write operations (create, delete, write, modify, append, replace)
    Optional[StatisticsReport],     # from get_chapter_statistics, get_document_statistics
    List[ParagraphDetail],          # from find_text_in_chapter, find_text_in_document
    # Fallback for unexpected or direct non-structured tool outputs, though tools should return Pydantic models.
    Optional[Dict[str, Any]],       # For generic details if an operation doesn't fit cleanly
    Optional[str]                   # For simple string messages if a tool were to return that
]

class FinalAgentResponse(BaseModel):
    """Defines the final structured output expected from the Pydantic AI agent."""
    summary: str
    details: DetailsType
    error_message: Optional[str] = None

# --- System Prompt ---
SYSTEM_PROMPT = """You are an assistant that manages structured local Markdown long documents using provided tools.
A 'long document' is a directory containing multiple 'chapter' files (Markdown .md files). Chapters are ordered alphanumerically by their filenames (e.g., '01-intro.md', '02-topic.md').

The available tools (like `list_long_documents`, `create_long_document`, `list_chapters`, `read_chapter_content`, `write_chapter_content`, `get_document_statistics`, `find_text_in_document`, etc.) will be discovered from an MCP server named 'LongDocumentManagementTools'.
For detailed information on how to use each tool, including its parameters and expected behavior, refer to the description of the tool itself (which will be provided to you).
Your goal is to help the user manage their long documents and chapters by using these tools effectively.

When a user asks for an operation:
1. Identify the correct tool by understanding the user's intent and matching it to the tool's description and the document/chapter structure.
2. Determine the necessary parameters for the chosen tool based on its description and the user's query. Clarify `document_name` and `chapter_name` if ambiguous.
3. Chapter names should include the .md extension (e.g., "01-introduction.md").
4. Before invoking the tool, briefly explain your reasoning: why this tool and these parameters.
5. After receiving results, analyze what you found and determine if further actions are needed.
6. Formulate a response conforming to the `FinalAgentResponse` model, ensuring the `details` field contains the direct and complete output from the invoked tool.

**General Guidelines:**
- Always clarify `document_name` if ambiguous. A document must exist before chapters can be added to it, unless using `create_long_document`.
- Do not assume a document or chapter exists unless listed by `list_long_documents`, `list_chapters` or confirmed by the user recently.
- If a tool call fails or an entity is not found, this should be reflected in the `summary` and potentially in the `error_message` field of the `FinalAgentResponse`. The `details` field (which should be an `OperationStatus` model in case of errors from write/modify tools, or None for read tools) should reflect the tool's direct output.

**Specific Tool Usage Notes (Examples - refer to actual tool descriptions for full details):**
- `list_long_documents()`: Lists all available long documents (directories).
- `create_long_document(document_name="my_book")`: Creates a new directory for a long document.
- `list_chapters(document_name="my_book")`: Lists all chapters (e.g., "01-intro.md", "02-body.md") in "my_book".
- `read_chapter_content(document_name="my_book", chapter_name="01-intro.md")`: Reads the full content of a specific chapter.
- `read_full_long_document(document_name="my_book")`: Reads all chapters of "my_book" and concatenates their content.
- `write_chapter_content(document_name="my_book", chapter_name="01-intro.md", new_content="# New Chapter Content...")`: Overwrites an entire chapter. Creates the chapter if it doesn't exist within an existing document.
- `modify_paragraph_content(document_name="my_book", chapter_name="01-intro.md", paragraph_index=0, new_paragraph_content="Revised first paragraph.", mode="replace")`: Modifies a specific paragraph. Other modes include "insert_before", "insert_after", "delete".
- `append_paragraph_to_chapter(document_name="my_book", chapter_name="01-intro.md", paragraph_content="This is a new paragraph at the end.")`
- `replace_text_in_chapter(document_name="my_book", chapter_name="01-intro.md", text_to_find="old_term", replacement_text="new_term")`: Replaces text within one chapter.
- `replace_text_in_document(document_name="my_book", text_to_find="global_typo", replacement_text="corrected_text")`: Replaces text across all chapters of "my_book".
- `get_chapter_statistics(document_name="my_book", chapter_name="01-intro.md")`: Gets word/paragraph count for a chapter.
- `get_document_statistics(document_name="my_book")`: Gets aggregate word/paragraph/chapter counts for "my_book".
- `find_text_in_chapter(...)` and `find_text_in_document(...)`: For locating text.

If a user asks to access or process the *content* of multiple chapters within a document (e.g., "read all chapters of 'my_book'"):
1. Use `read_full_long_document(document_name="my_book")`. The `details` field will be a `FullLongDocumentContent` object.
2. Your `summary` should state that the full document content has been retrieved.

If a user asks to get the content of *all documents* (i.e., all chapters from all documents):
1. **Mandatory First Step**: Call `list_long_documents()` to identify all document names.
2. **Mandatory Second Step**: For EACH document identified, call `read_full_long_document(document_name: str)` to retrieve its complete content (all its chapters).
3. **Result Consolidation**: Collect ALL `FullLongDocumentContent` objects. The `details` field of your `FinalAgentResponse` MUST be a list of these `FullLongDocumentContent` objects (i.e., `List[FullLongDocumentContent]`).
4. **Summary**: Your `summary` must clearly state that the content of all documents has been retrieved. A response just listing document names is INCOMPLETE if content was requested.

If a search tool like `find_text_in_chapter` or `find_text_in_document` returns no results, your `summary` should explicitly state that the queried text was not found and clearly mention the specific text that was searched for.

Follow the user's instructions carefully and to the letter without asking for clarification or further instructions unless absolutely necessary for tool parameterization.
"""

# --- Agent Setup and Processing Logic ---
async def initialize_agent_and_mcp_server() -> Tuple[Agent, MCPServerStdio]:
    """Initializes the Pydantic AI agent and its MCP server configuration."""
    try:
        llm = load_gemini_llm_config()
    except ValueError as e:
        print(f"Error loading LLM config: {e}")
        raise

    server_script_path = Path(__file__).parent / "doc_tool_server.py"
    if not server_script_path.is_file():
        msg = f"Error: Server script not found or is not a file at {server_script_path}"
        print(msg)
        raise FileNotFoundError(msg)

    doc_tools_stdio_server = MCPServerStdio(
        command=sys.executable,
        args=[str(server_script_path.resolve())],
    )

    agent = Agent(
        llm,
        mcp_servers=[doc_tools_stdio_server],
        system_prompt=SYSTEM_PROMPT,
        output_type=FinalAgentResponse
    )
    return agent, doc_tools_stdio_server

async def process_single_user_query(agent: Agent, user_query: str) -> Optional[FinalAgentResponse]:
    """Processes a single user query using the provided agent and returns the structured response."""
    try:
        run_result: AgentRunResult[FinalAgentResponse] = await agent.run(user_query)
        
        if run_result and run_result.output:
            return run_result.output
        elif run_result and run_result.error_message:
            return FinalAgentResponse(
                summary=f"Agent error: {run_result.error_message}", 
                details=None, 
                error_message=run_result.error_message
            )
        else:
            return None
    except Exception as e:
        print(f"Error during agent query processing: {e}")
        return FinalAgentResponse(summary=f"Exception during query processing: {e}", details=None, error_message=str(e))

# --- Main Agent Interactive Loop ---
async def main():
    """Initializes and runs the Pydantic AI agent with an interactive loop."""
    try:
        agent, doc_tools_stdio_server = await initialize_agent_and_mcp_server()
    except (ValueError, FileNotFoundError) as e:
        # Errors from initialize_agent_and_mcp_server are already printed
        return

    try:
        async with agent.run_mcp_servers(): # Use the agent's context manager for the specific mcp_server instance
            print("MCP Server (doc_tool_server.py) started by Pydantic AI agent.")
            print("\n--- Pydantic AI Long Document Agent --- ")
            print("Ask me to manage long documents (directories of chapters).")
            print("Type 'exit' to quit.")

            while True:
                user_query = input("\nUser Query: ")
                if user_query.lower() == 'exit':
                    break
                if not user_query.strip():
                    continue
                
                final_response = await process_single_user_query(agent, user_query)
                
                if final_response:
                    print("\n--- Agent Response ---")
                    print(f"Summary: {final_response.summary}")

                    if isinstance(final_response.details, list):
                        if not final_response.details:
                            print("Details: [] (Empty list)")
                        else:
                            item_type = type(final_response.details[0])
                            print(f"\n--- Details (List of {item_type.__name__}) ---")
                            for item_idx, item_detail in enumerate(final_response.details):
                                print(f"Item {item_idx + 1}:")
                                if hasattr(item_detail, 'model_dump'): # Check if Pydantic model
                                    print(item_detail.model_dump(exclude_none=True))
                                else:
                                    print(item_detail)
                    elif hasattr(final_response.details, 'model_dump'): # Check if Pydantic model
                        print("\n--- Details ---")
                        print(final_response.details.model_dump(exclude_none=True))
                    elif final_response.details is not None:
                        print(f"Details: {final_response.details}")
                    else:
                        print("Details: None")
                        
                    if final_response.error_message:
                        print(f"Error Message: {final_response.error_message}")
                # If final_response is None, process_single_user_query already printed an error
                        
        print("MCP Server (doc_tool_server.py) stopped by Pydantic AI agent.")
    except KeyboardInterrupt:
        print("\nUser requested exit. Shutting down...")
    except Exception as e:
        print(f"An unexpected error occurred in the agent: {e}")
    finally:
        print("Agent has shut down.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        # This will catch errors during asyncio.run(main()) itself if any
        print(f"Critical error during agent startup or shutdown: {e}")

# To run this agent:
# 1. Ensure 'doc_tool_server.py' is in the same directory as this script.
# 2. The server will create a 'long_documents_storage/' directory in the project root 
#    (or as configured by LONG_DOCUMENT_ROOT_DIR env var) on first run if it doesn't exist.
#    You will create document folders (e.g. 'my_book/') and chapter files (e.g. '01-intro.md') within it.
# 3. Create a .env file in the root directory with your GOOGLE_API_KEY (optional, for explicit auth).
#    e.g., GOOGLE_API_KEY='your_google_api_key'
#    You can also specify GEMINI_MODEL_NAME in the .env file, e.g., GEMINI_MODEL_NAME='gemini-1.5-pro-latest'
#    The agent defaults to 'gemini-2.5-flash-preview-04-17' if not set.
# 4. Install dependencies: `pip install -r requirements.txt` (ensure it's up to date)
# 5. Run this script: `python agent.py`