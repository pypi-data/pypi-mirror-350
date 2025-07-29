import threading
from typing import Any, List
import json
import time
from pynostr.event import Event
import requests
from agentstr.nostr_client import NostrClient


class NostrAgentServer(object):
    def __init__(self,
                 agent_url: str,
                 satoshis: int,
                 nostr_client: NostrClient = None,
                 relays: List[str] = None,
                 private_key: str = None,
                 nwc_str: str = None,
                 ):
        self.client = nostr_client or NostrClient(relays=relays, private_key=private_key, nwc_str=nwc_str)
        self.agent_url = agent_url
        self.satoshis = satoshis
        self._agent_info = self._get_agent_info()

    def _get_agent_info(self) -> dict[str, Any]:
        return requests.get(f"{self.agent_url}/info",
                            headers={'Content-Type': 'application/json'},
                            ).json()

    def agent_info(self) -> dict[str, Any]:
        return self._agent_info

    def chat(
        self,
        message: str,
        thread_id: str | None = None,
    ) -> Any:
        """Call a tool by name with arguments."""
        request = {
            'messages': [message],
        }
        if thread_id:
            request['thread_id'] = thread_id
        print(f'Sending request: {json.dumps(request)}')
        response = requests.post(
            f"{self.agent_url}/chat",
            headers={'Content-Type': 'application/json'},
            json=request,
        )
        try:
            response.raise_for_status()
            result = response.text.replace('\\n', '\n').strip('"').strip()
        except Exception as e:
            print(f"Error: {e}")
            result = f'Unknown error'
        print(f'Response: {result}')
        return result

    def _direct_message_callback(self, event: Event, message: str):
        if message.strip().startswith('{'):
            print(f'Ignoring non-chat messages')
            return
        """
        Callback function to handle incoming direct messages.
        :param event: The event object containing the message.
        :param message: The message content.
        """
        # Process the incoming message
        message = message.strip()
        print(f"Request: {message}")
        try:

            satoshis = self.satoshis
            if satoshis > 0:
                # Requires payment first
                invoice = self.client.nwc_client.make_invoice(amt=satoshis,
                                                              desc="Payment for agent")
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
                    response = f"Payment failed. Please try again."
                    print(f"On failure response: {response}")
                    thr = threading.Thread(
                        target=self.client.send_direct_message_to_pubkey,
                        args=(event.pubkey, response),
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
        # Update list_tools metadata
        thr = threading.Thread(
            target=self.client.update_metadata,
            kwargs={
                'name': 'agent_server',
                'display_name': self._agent_info['name'],
                'about': json.dumps(self.agent_info())
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
    private_key = os.getenv('NOSTR_SERVER_PRIVATE_KEY')
    nwc_str = os.getenv('NWC_CONN_STR')
    agent_url = os.getenv('AGENT_URL')

    # Create an instance of NostrClient
    client = NostrClient(relays, private_key, nwc_str)
    server = NostrAgentServer(agent_url, 0, client)
    server.start()
