import logging
from typing import Callable, Any
from mcp.server.fastmcp import FastMCP
from rich.logging import RichHandler
from rich.console import Console

# Rich console for beautiful output
console = Console()

def setup_logging(level: int = logging.INFO):
    """Configures high-quality logging using RichHandler."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, console=console)]
    )
    return logging.getLogger("mcp-agent")

def create_mcp_server(name: str) -> FastMCP:
    """Helper to create and configure a FastMCP server instance."""
    return FastMCP(name)

def tool_error_handler(func: Callable) -> Callable:
    """Decorator to catch exceptions in MCP tools and return a structured error string."""
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"HATA ({func.__name__}): {str(e)}"
            logging.error(error_msg)
            return error_msg
    return wrapper
