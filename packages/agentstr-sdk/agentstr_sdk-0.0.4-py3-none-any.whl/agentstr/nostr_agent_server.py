import threading
import json
import time
from typing import Any, List
from pynostr.event import Event
import requests
from agentstr.nostr_client import NostrClient


class NostrAgentServer:
    """A server that integrates an external agent with Nostr, handling direct messages.

    This server communicates with an external agent (e.g., a chatbot) via an API and
    processes direct messages received over Nostr, with optional payment requirements.

    Attributes:
        client (NostrClient): Nostr client for communication.
        agent_url (str): URL of the external agent API.
        satoshis (int): Satoshis required for agent interaction.
        _agent_info (dict): Metadata about the agent.
    """
    def __init__(self, agent_url: str, satoshis: int, chat_url_path: str = '/chat', info_url_path: str = '/info', nostr_client: NostrClient = None,
                 relays: List[str] = None, private_key: str = None, nwc_str: str = None):
        """Initialize the agent server.

        Args:
            agent_url: URL of the external agent API.
            satoshis: Satoshis required for agent interaction.
            chat_url_path: Path to the chat endpoint of the external agent API.
            info_url_path: Path to the info endpoint of the external agent API.
            nostr_client: Existing NostrClient instance (optional).
            relays: List of Nostr relay URLs (if no client provided).
            private_key: Nostr private key (if no client provided).
            nwc_str: Nostr Wallet Connect string for payments (optional).
        """
        self.client = nostr_client or NostrClient(relays=relays, private_key=private_key, nwc_str=nwc_str)
        self.agent_url = agent_url
        self.satoshis = satoshis
        self.chat_url_path = chat_url_path
        self.info_url_path = info_url_path
        self._agent_info = self._get_agent_info()

    def _get_agent_info(self) -> dict[str, Any]:
        """Fetch metadata from the agent API.

        Returns:
            Dictionary containing agent metadata.
        """
        return requests.get(f"{self.agent_url}{self.info_url_path}", headers={'Content-Type': 'application/json'}).json()

    def agent_info(self) -> dict[str, Any]:
        """Get the agent's metadata.

        Returns:
            Dictionary containing agent metadata.
        """
        return self._agent_info

    def chat(self, message: str, thread_id: str | None = None) -> Any:
        """Send a message to the agent and retrieve the response.

        Args:
            message: The message to send to the agent.
            thread_id: Optional thread ID for conversation context.

        Returns:
            Response from the agent, or an error message.
        """
        request = {'messages': [message]}
        if thread_id:
            request['thread_id'] = thread_id
        print(f'Sending request: {json.dumps(request)}')
        response = requests.post(f"{self.agent_url}{self.chat_url_path}", headers={'Content-Type': 'application/json'}, json=request)
        try:
            response.raise_for_status()
            result = response.text.replace('\\n', '\n').strip('"').strip()
        except Exception as e:
            print(f"Error: {e}")
            result = 'Unknown error'
        print(f'Response: {result}')
        return result

    def _direct_message_callback(self, event: Event, message: str):
        """Handle incoming direct messages for agent interaction.

        Args:
            event: The Nostr event containing the message.
            message: The message content.
        """
        if message.strip().startswith('{'):
            print(f'Ignoring non-chat messages')
            return
        message = message.strip()
        print(f"Request: {message}")
        try:
            if self.satoshis > 0:
                invoice = self.client.nwc_client.make_invoice(amt=self.satoshis, desc="Payment for agent")
                response = invoice

                def on_success():
                    print(f"Payment succeeded for agent")
                    result = self.chat(message, thread_id=event.pubkey)
                    response = str(result)
                    print(f'On success response: {response}')
                    thr = threading.Thread(
                        target=self.client.send_direct_message_to_pubkey,
                        args=(event.pubkey, response),
                    )
                    thr.start()

                def on_failure():
                    response = "Payment failed. Please try again."
                    print(f"On failure response: {response}")
                    thr = threading.Thread(
                        target=self.client.send_direct_message_to_pubkey,
                        args=(event.pubkey, response),
                    )
                    thr.start()

                thr = threading.Thread(
                    target=self.client.nwc_client.on_payment_success,
                    kwargs={'invoice': invoice, 'callback': on_success, 'timeout': 120, 'unsuccess_callback': on_failure}
                )
                thr.start()
            else:
                result = self.chat(message, thread_id=event.pubkey)
                response = str(result)
        except Exception as e:
            response = f'Error: {e}'
        print(f'Response: {response}')
        time.sleep(1)
        thr = threading.Thread(
            target=self.client.send_direct_message_to_pubkey,
            args=(event.pubkey, response),
        )
        thr.start()

    def start(self):
        """Start the agent server, updating metadata and listening for direct messages."""
        thr = threading.Thread(
            target=self.client.update_metadata,
            kwargs={'name': 'agent_server', 'display_name': self._agent_info['name'], 'about': json.dumps(self.agent_info())}
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
    private_key = os.getenv('NOSTR_SERVER_PRIVATE_KEY')
    nwc_str = os.getenv('NWC_CONN_STR')
    agent_url = os.getenv('AGENT_URL')
    client = NostrClient(relays, private_key, nwc_str)
    server = NostrAgentServer(agent_url, 0, client)
    server.start()