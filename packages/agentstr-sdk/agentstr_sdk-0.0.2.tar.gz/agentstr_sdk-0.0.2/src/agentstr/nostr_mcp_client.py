import threading
from typing import Any, List
import json

from pynostr.event import Event
from pynostr.key import PrivateKey
from pynostr.utils import get_timestamp

from agentstr.nostr_client import NostrClient


class NostrMCPClient(object):
    def __init__(self,
                 mcp_pubkey: str,
                 nostr_client: NostrClient = None,
                 relays: List[str] = None,
                 private_key: str = None,
                 nwc_str: str = None,
                 ):
        self.client = nostr_client or NostrClient(relays=relays, private_key=private_key, nwc_str=nwc_str)
        self.mcp_pubkey = mcp_pubkey
        self.tool_to_sats_map = {}

    def _set_result_callback(self, tool_name: str, res: list):
        def inner(event: Event, message: str):
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
        """Retrieve available tools"""
        metadata = self.client.get_metadata_for_pubkey(self.mcp_pubkey)
        tools = json.loads(metadata.about)
        for tool in tools['tools']:
            self.tool_to_sats_map[tool['name']] = tool['satoshis']
        return tools

    def call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
        timeout: int = 60,
    ) -> dict[str, Any] | None:
        """Call a tool by name with arguments (paying satoshis if required)."""
        timestamp = get_timestamp()
        if self.tool_to_sats_map.get(name):
            timeout = 20
        else:
            timeout = 3
        thr = threading.Thread(
            target=self.client.send_direct_message_to_pubkey,
            args=(self.mcp_pubkey, json.dumps({
                'action': 'call_tool',
                'tool_name': name,
                'arguments': arguments
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

    # Get the environment variables
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('AGENT_PRIVATE_KEY')
    server_public_key = PrivateKey.from_nsec(os.getenv('MCP_MATH_PRIVATE_KEY')).public_key.hex()
    nwc_str = os.getenv('NWC_CONN_STR')

    print(f"Server public key: {server_public_key}")

    # Create an instance of NostrClient
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
