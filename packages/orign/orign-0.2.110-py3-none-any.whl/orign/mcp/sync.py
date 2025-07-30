# This is a synchronous wrapper for the mcp_use library
import asyncio
import time  # Add import
from typing import Any, Coroutine, Dict, TypeVar

from mcp_use import MCPClient as AsyncMCPClient
from mcp_use.session import MCPSession as AsyncMCPSession

T = TypeVar("T")


def _run_async(awaitable: Coroutine[Any, Any, T]) -> T:
    """Helper function to run an awaitable in a new event loop."""
    return asyncio.run(awaitable)


class MCPSession:
    """Synchronous wrapper for MCPSession."""

    def __init__(self, session: AsyncMCPSession):
        self._session = session
        # Initialize the session synchronously
        time.sleep(2)  # Add a small delay
        self.session_info = _run_async(self._session.initialize())
        self.tools = self._session.tools  # Tools are populated during initialize

    def discover_tools(self) -> list[dict[str, Any]]:
        """Synchronously discover available tools."""
        # Tools are discovered during initialization in this wrapper
        return self.tools

    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Synchronously call an MCP tool."""
        return _run_async(self._session.call_tool(name, arguments))

    # Optional: Add methods to manage connection state if needed, e.g., close
    def close(self) -> None:
        """Synchronously close the session connection."""
        if self._session.is_connected:
            _run_async(self._session.disconnect())


class MCPClient:
    """Synchronous wrapper for MCPClient."""

    def __init__(self, config: Dict[str, Any]):
        self._client = AsyncMCPClient.from_dict(config)

    def new_session(self, server_name: str) -> MCPSession:
        """Creates a new synchronous MCP session."""
        # Create the underlying async session
        async_session = _run_async(self._client.create_session(server_name))
        # Wrap it in the synchronous wrapper
        sync_session = MCPSession(async_session)
        return sync_session
