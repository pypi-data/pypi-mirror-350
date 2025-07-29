import threading
import json
import time
from typing import Callable, Any, List
from pynostr.event import Event
from agentstr.nostr_client import NostrClient
from mcp.server.fastmcp.exceptions import ToolError
from mcp.server.fastmcp.tools.tool_manager import ToolManager


class NostrMCPServer:
    """A Model Context Protocol (MCP) server running on the Nostr protocol.

    This server registers tools that can be called by clients via direct messages.
    It supports optional payment requirements in satoshis for tool usage, processed
    through Nostr Wallet Connect (NWC).

    Attributes:
        client (NostrClient): Nostr client for communication.
        display_name (str): Display name of the server.
        tool_to_sats_map (dict): Mapping of tool names to required satoshis.
        tool_manager (ToolManager): Manager for registered tools.
    """
    def __init__(self, display_name: str, nostr_client: NostrClient = None,
                 relays: List[str] = None, private_key: str = None, nwc_str: str = None):
        """Initialize the MCP server.

        Args:
            display_name: Display name of the server.
            nostr_client: Existing NostrClient instance (optional).
            relays: List of Nostr relay URLs (if no client provided).
            private_key: Nostr private key (if no client provided).
            nwc_str: Nostr Wallet Connect string for payments (optional).
        """
        self.client = nostr_client or NostrClient(relays=relays, private_key=private_key, nwc_str=nwc_str)
        self.display_name = display_name
        self.tool_to_sats_map = {}
        self.tool_manager = ToolManager()

    def add_tool(self, fn: Callable[..., Any], name: str | None = None,
                 description: str | None = None, satoshis: int | None = None):
        """Register a tool with the server.

        Args:
            fn: The function to register as a tool.
            name: Name of the tool (defaults to function name).
            description: Description of the tool (optional).
            satoshis: Satoshis required to call the tool (optional).
        """
        if satoshis:
            self.tool_to_sats_map[name or fn.__name__] = satoshis
        self.tool_manager.add_tool(fn=fn, name=name, description=description)

    def list_tools(self) -> dict[str, Any]:
        """List all registered tools and their metadata.

        Returns:
            Dictionary containing a list of tools with their names, descriptions,
            input schemas, and required satoshis.
        """
        return {
            "tools": [{
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.parameters,
                "satoshis": self.tool_to_sats_map.get(tool.name, 0),
            } for tool in self.tool_manager.list_tools()]
        }

    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Execute a registered tool by name with provided arguments.

        Args:
            name: Name of the tool to call.
            arguments: Dictionary of arguments for the tool.

        Returns:
            Result of the tool execution.

        Raises:
            ToolError: If the tool is not found.
        """
        tool = self.tool_manager.get_tool(name)
        if not tool:
            raise ToolError(f"Unknown tool: {name}")
        return tool.fn(**arguments)

    def _direct_message_callback(self, event: Event, message: str):
        """Handle incoming direct messages to process tool calls or list requests.

        Args:
            event: The Nostr event containing the message.
            message: The message content.
        """
        message = message.strip()
        print(f"Request: {message}")
        try:
            request = json.loads(message)
            if request['action'] == 'list_tools':
                response = self.list_tools()
            elif request['action'] == 'call_tool':
                tool_name = request['tool_name']
                arguments = request['arguments']
                satoshis = self.tool_to_sats_map.get(tool_name, 0)
                if satoshis > 0:
                    invoice = self.client.nwc_client.make_invoice(amt=satoshis, desc="Payment for tool call")
                    response = invoice

                    def on_success():
                        print(f"Payment succeeded for {tool_name}")
                        result = self.call_tool(tool_name, arguments)
                        response = {"content": [{"type": "text", "text": str(result)}]}
                        print(f'On success response: {response}')
                        thr = threading.Thread(
                            target=self.client.send_direct_message_to_pubkey,
                            args=(event.pubkey, json.dumps(response)),
                        )
                        thr.start()

                    def on_failure():
                        response = {"error": f"Payment failed for {tool_name}"}
                        print(f"On failure response: {response}")
                        thr = threading.Thread(
                            target=self.client.send_direct_message_to_pubkey,
                            args=(event.pubkey, json.dumps(response)),
                        )
                        thr.start()

                    thr = threading.Thread(
                        target=self.client.nwc_client.on_payment_success,
                        kwargs={'invoice': invoice, 'callback': on_success, 'timeout': 120, 'unsuccess_callback': on_failure}
                    )
                    thr.start()
                else:
                    result = self.call_tool(tool_name, arguments)
                    response = {"content": [{"type": "text", "text": str(result)}]}
            else:
                response = {"error": f"Invalid action: {request['action']}"}
        except Exception as e:
            response = {"content": [{"type": "text", "text": str(e)}]}
        if not isinstance(response, str):
            response = json.dumps(response)
        print(f'Response: {response}')
        time.sleep(1)
        thr = threading.Thread(
            target=self.client.send_direct_message_to_pubkey,
            args=(event.pubkey, response),
        )
        thr.start()

    def start(self):
        """Start the MCP server, updating metadata and listening for direct messages."""
        thr = threading.Thread(
            target=self.client.update_metadata,
            kwargs={'name': 'mcp_server', 'display_name': self.display_name, 'about': json.dumps(self.list_tools())}
        )
        print(f'Updating metadata for {self.client.public_key.bech32()}')
        thr.start()
        time.sleep(3)
        print(f'Starting message listener for {self.client.public_key.bech32()}')
        self.client.direct_message_listener(callback=self._direct_message_callback)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('MCP_MATH_PRIVATE_KEY')

    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    def subtract(a: int, b: int) -> int:
        """Subtract two numbers."""
        return a - b

    def divide(a: int, b: int) -> int:
        """Divide two numbers (integer division)."""
        return a // b

    client = NostrClient(relays, private_key, None)
    server = NostrMCPServer("Math MCP Server", client)
    server.add_tool(add)
    server.add_tool(multiply, name="multiply", description="Multiply two numbers")
    server.add_tool(subtract)
    server.add_tool(divide)
    server.start()