import threading
from typing import Callable, Any
import json
import time
from pynostr.event import Event
from nostr_agents.nostr_client import NostrClient
from mcp.server.fastmcp.exceptions import ToolError
from mcp.server.fastmcp.tools.tool_manager import ToolManager


class NostrMCPServer(object):
    def __init__(self, display_name: str, nostr_client: NostrClient):
        self.display_name = display_name
        self.client = nostr_client
        self.tool_to_sats_map = {}
        self.tool_manager = ToolManager()

    def add_tool(self,
                 fn: Callable[..., Any],
                 name: str | None = None,
                 description: str | None = None,
                 satoshis: int | None = None):
        if satoshis:
            self.tool_to_sats_map[name or fn.__name__] = satoshis
        self.tool_manager.add_tool(
            fn=fn,
            name=name,
            description=description,
        )

    def list_tools(self) -> dict[str, Any]:
        """Define available tools"""
        return {
            "tools": [{
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.parameters,
                "satoshis": self.tool_to_sats_map.get(tool.name, 0),
            } for tool in self.tool_manager.list_tools()]
        }

    def call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
    ) -> Any:
        """Call a tool by name with arguments."""
        tool = self.tool_manager.get_tool(name)
        if not tool:
            raise ToolError(f"Unknown tool: {name}")
        result = tool.fn(**arguments)
        return result

    def _direct_message_callback(self, event: Event, message: str):
        """
        Callback function to handle incoming direct messages.
        :param event: The event object containing the message.
        :param message: The message content.
        """
        # Process the incoming message
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
                    # Requires payment first
                    invoice = self.client.nwc_client.make_invoice(amt=satoshis,
                                                                  desc="Payment for tool call")
                    response = invoice

                    def on_success():
                        print(f"Payment succeeded for {tool_name}")
                        result = self.call_tool(tool_name, arguments)
                        response = {
                            "content": [{
                                "type": "text",
                                "text": str(result)
                            }]
                        }
                        print(f'On success response: {response}')
                        thr = threading.Thread(
                            target=self.client.send_direct_message_to_pubkey,
                            args=(event.pubkey, json.dumps(response)),
                        )
                        thr.start()

                    def on_failure():
                        response = {
                            "error": f"Payment failed for {tool_name}"
                        }
                        print(f"On failure response: {response}")
                        thr = threading.Thread(
                            target=self.client.send_direct_message_to_pubkey,
                            args=(event.pubkey, json.dumps(response)),
                        )
                        thr.start()
                    thr = threading.Thread(
                        target=self.client.nwc_client.on_payment_success,
                        kwargs={
                            'invoice': invoice,
                            'callback': on_success,
                            'timeout': 120,
                            'unsuccess_callback': on_failure,
                        }
                    )
                    thr.start()
                else:
                    result = self.call_tool(tool_name, arguments)
                    response = {
                        "content": [{
                            "type": "text",
                            "text": str(result)
                        }]
                    }

            else:
                response = {
                    "error": f"Invalid action: {request['action']}"
                }
        except Exception as e:
            response = {
                "content": [{
                    "type": "text",
                    "text": str(e)
                }]
            }

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
        # Update list_tools metadata
        thr = threading.Thread(
            target=self.client.update_metadata,
            kwargs={
                'name': 'mcp_server',
                'display_name': self.display_name,
                'about': json.dumps(self.list_tools())
            }
        )
        print(f'Updating metadata for {self.client.public_key.bech32()}')
        thr.start()
        time.sleep(3)

        print(f'Starting message listener for {self.client.public_key.bech32()}')

        # Start call_tool listener
        self.client.direct_message_listener(
            callback=self._direct_message_callback
        )


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    # Get the environment variables
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('MCP_MATH_PRIVATE_KEY')


    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b


    def multiply(a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b


    def subtract(a: int, b: int) -> int:
        """Subtract two numbers"""
        return a - b


    def divide(a: int, b: int) -> int:
        """Divide two numbers (integer division)"""
        return a // b


    # Create an instance of NostrClient
    client = NostrClient(relays, private_key, None)
    server = NostrMCPServer("Math MCP Server", client)
    server.add_tool(add)  # Add by signature alone
    server.add_tool(multiply, name="multiply", description="Multiply two numbers")  # Add by signature and name
    server.add_tool(subtract)
    server.add_tool(divide)

    server.start()

    '''
    {"action": "call_tool", "tool_name": "add", "arguments": {"a": 1, "b": 2}}
    {"action": "call_tool", "tool_name": "multiply", "arguments": {"a": 2, "b": 5}}
    '''