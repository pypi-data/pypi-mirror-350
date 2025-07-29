# Agentstr - Nostr Agent Tools

## Overview
The agentstr SDK is designed to integrate MCP functionality with the Nostr protocol, enabling developers to create servers and clients that communicate over Nostr's decentralized relay network. It supports:

+ **NostrClient**: A core client for interacting with Nostr relays, handling events, direct messages, and metadata.
+ **NostrMCPServer**: A server that exposes tools (functions) that clients can call, with optional payment requirements in satoshis via Nostr Wallet Connect (NWC).
+ **NostrMCPClient**: A client that discovers and calls tools on an MCP server, handling payments if required.
+ **NostrAgentServer**: A server that interacts with an external agent (e.g., a chatbot) and processes direct messages, with optional payment support.
+ **NWCClient**: A client for Nostr Wallet Connect, managing payments and invoices.

The SDK uses the pynostr library for Nostr protocol interactions and supports asynchronous communication, tool management, and payment processing.

## Usage Example
To demonstrate how to use the agentstr SDK, here's an example of setting up an MCP server with mathematical tools and a client to call them:

```python
from agentstr import NostrClient, NostrMCPServer, NostrMCPClient
import os
from dotenv import load_dotenv

load_dotenv()
relays = os.getenv('NOSTR_RELAYS').split(',')
private_key = os.getenv('MCP_MATH_PRIVATE_KEY')
nwc_str = os.getenv('NWC_CONN_STR')

# Define a tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# Create and start an MCP server
client = NostrClient(relays, private_key, nwc_str)
server = NostrMCPServer("Math MCP Server", client)
server.add_tool(add, satoshis=10)  # Requires 10 satoshis to call
server.start()

# Create an MCP client to call the tool
mcp_client = NostrMCPClient(client, mcp_pubkey=client.public_key.hex())
tools = mcp_client.list_tools()
print(f"Available tools: {tools}")
result = mcp_client.call_tool("add", {"a": 5, "b": 3})
print(f"Result of 5 + 3: {result['content'][0]['text']}")
```

This example sets up an MCP server that exposes an `add` tool, requiring a payment of 10 satoshis. The client discovers the tool and calls it, handling the payment automatically.

### Notes
+ **Dependencies**: The SDK relies on `pynostr` for Nostr protocol interactions and `bolt11` for invoice decoding. Ensure these are installed (`pip install pynostr python-bolt11`).
+ **Environment Variables**: The SDK uses environment variables (`NOSTR_RELAYS`, `MCP_MATH_PRIVATE_KEY`, `NWC_CONN_STR`, etc.) for configuration, loaded via `dotenv`.
+ **Payment Handling**: Tools or agent interactions requiring satoshis use NWC for invoice creation and payment verification.
+ **Threading**: The SDK uses threading for asynchronous operations, such as listening for messages or monitoring payments.
