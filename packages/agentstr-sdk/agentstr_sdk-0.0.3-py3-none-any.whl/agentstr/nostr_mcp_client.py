import threading
import json
from typing import Any, List, Callable
from pynostr.event import Event
from pynostr.key import PrivateKey
from pynostr.utils import get_timestamp
from agentstr.nostr_client import NostrClient


class NostrMCPClient:
    """A client for interacting with a Model Context Protocol (MCP) server on Nostr.

    This client discovers tools available on an MCP server and allows calling them,
    handling any required payments via Nostr Wallet Connect (NWC).

    Attributes:
        client (NostrClient): Nostr client for communication.
        mcp_pubkey (str): Public key of the MCP server.
        tool_to_sats_map (dict): Mapping of tool names to required satoshis.
    """
    def __init__(self, mcp_pubkey: str, nostr_client: NostrClient = None,
                 relays: List[str] = None, private_key: str = None, nwc_str: str = None):
        """Initialize the MCP client.

        Args:
            mcp_pubkey: Public key of the MCP server to interact with.
            nostr_client: Existing NostrClient instance (optional).
            relays: List of Nostr relay URLs (if no client provided).
            private_key: Nostr private key (if no client provided).
            nwc_str: Nostr Wallet Connect string for payments (optional).
        """
        self.client = nostr_client or NostrClient(relays=relays, private_key=private_key, nwc_str=nwc_str)
        self.mcp_pubkey = mcp_pubkey
        self.tool_to_sats_map = {}

    def _set_result_callback(self, tool_name: str, res: List) -> Callable[[Event, str], bool]:
        """Create a callback to handle responses from the MCP server.

        Args:
            tool_name: Name of the tool being called.
            res: List to store the response.

        Returns:
            Callback function that processes server responses and handles payments.
        """
        def inner(event: Event, message: str) -> bool:
            try:
                print(f'MCP Client received message: {message}')
                if isinstance(message, str) and message.startswith('ln'):
                    invoice = message.strip()
                    print(f'Paying invoice: {invoice}')
                    self.client.nwc_client.try_pay_invoice(invoice=invoice, amt=self.tool_to_sats_map[tool_name])
                    return False  # Keep listening
                res[0] = json.loads(message)
                return True
            except Exception as e:
                print(f"Error parsing message: {e}")
            return False
        return inner

    def list_tools(self) -> dict[str, Any] | None:
        """Retrieve the list of available tools from the MCP server.

        Returns:
            Dictionary of tools with their metadata, or None if not found.
        """
        metadata = self.client.get_metadata_for_pubkey(self.mcp_pubkey)
        tools = json.loads(metadata.about)
        for tool in tools['tools']:
            self.tool_to_sats_map[tool['name']] = tool['satoshis']
        return tools

    def call_tool(self, name: str, arguments: dict[str, Any], timeout: int = 60) -> dict[str, Any] | None:
        """Call a tool on the MCP server with provided arguments.

        Args:
            name: Name of the tool to call.
            arguments: Dictionary of arguments for the tool.
            timeout: Timeout in seconds for receiving a response.

        Returns:
            Response dictionary from the server, or None if no response.
        """
        timestamp = get_timestamp()
        timeout = 20 if self.tool_to_sats_map.get(name) else 3
        thr = threading.Thread(
            target=self.client.send_direct_message_to_pubkey,
            args=(self.mcp_pubkey, json.dumps({
                'action': 'call_tool', 'tool_name': name, 'arguments': arguments
            })),
        )
        thr.start()
        res = [None]
        self.client.direct_message_listener(
            callback=self._set_result_callback(name, res),
            recipient_pubkey=self.mcp_pubkey,
            timeout=timeout,
            timestamp=timestamp,
            close_after_first_message=True
        )
        return res[0]

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('AGENT_PRIVATE_KEY')
    server_public_key = PrivateKey.from_nsec(os.getenv('MCP_MATH_PRIVATE_KEY')).public_key.hex()
    nwc_str = os.getenv('NWC_CONN_STR')
    print(f"Server public key: {server_public_key}")
    client = NostrClient(relays, private_key, nwc_str)
    mcp_client = NostrMCPClient(client, mcp_pubkey=server_public_key)
    tools = mcp_client.list_tools()
    print(f'Found tools:')
    print(json.dumps(tools, indent=4))
    result = mcp_client.call_tool("get_weather", {"city": "Seattle"})
    print(f'Result: {result}')
    print(f'The weather in Seattle is: {result["content"][-1]["text"]}')
    result = mcp_client.call_tool("multiply", {"a": 69, "b": 420})
    print(f'The result of 69 * 420 is: {result["content"][-1]["text"]}')
    result = mcp_client.call_tool("get_current_date", {})
    print(f'The current date is: {result["content"][-1]["text"]}')