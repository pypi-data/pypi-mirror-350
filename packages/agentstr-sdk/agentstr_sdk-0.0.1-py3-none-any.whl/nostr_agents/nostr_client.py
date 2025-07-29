from typing import List, Any, Optional, Callable
import logging
import uuid
import time
import json

from pynostr.base_relay import RelayPolicy
from pynostr.key import PrivateKey
from pynostr.message_type import RelayMessageType
from pynostr.relay_manager import RelayManager
from pynostr.event import EventKind
from pynostr.filters import Filters, FiltersList
from pynostr.encrypted_dm import EncryptedDirectMessage
from pynostr.metadata import Metadata
from pynostr.event import Event
from pynostr.utils import get_public_key, get_timestamp

from nostr_agents.nwc_client import NWCClient


logging.basicConfig(level=logging.WARNING)  # Set the minimum logging level


logger = logging.getLogger(__name__)
ack = set([])


def log_callback(*args):
    logging.info(f"Received message from {args}")


class NostrClient(object):
    def __init__(self,
                 relays: List[str],
                 private_key: str,
                 nwc_str: str = None,
                 ):
        """
        Initialize the NostrClient with a list of relays, private key, and NWC string.
        :param relays: List of relay URLs.
        :param private_key: nsec private key.
        :param nwc_str: Nostr Wallet Connection string (optional).
        """
        self.relays = relays
        self.private_key = PrivateKey.from_nsec(private_key)
        self.public_key = self.private_key.public_key
        self.nwc_client = NWCClient(nwc_str) if nwc_str else None

    def sign(self, event: Event):
        """Sign the event with the private key."""
        event.sign(self.private_key.hex())
        return event

    def get_relay_manager(self,
                          message_callback=log_callback,
                          timeout: int = 2,
                          error_threshold: int = 3,
                          close_on_eose: bool = False,
                          policy: RelayPolicy = RelayPolicy()) -> RelayManager:
        relay_manager = RelayManager(timeout=timeout,
                                     error_threshold=error_threshold)

        for relay in self.relays:
            relay_manager.add_relay(relay.strip(),
                                    close_on_eose=close_on_eose,
                                    policy=policy,
                                    timeout=timeout,
                                    message_callback=message_callback)
        return relay_manager

    def read_posts_by_tag(self, tag: str, limit: int = 10) -> list[dict]:
        relay_manager = self.get_relay_manager(timeout=10)

        filter1 = Filters(
            limit=limit,
            kinds=[EventKind.TEXT_NOTE],
        )
        filter1.add_arbitrary_tag("t", [tag])
        subscription_id = uuid.uuid1().hex

        relay_manager.add_subscription_on_all_relays(subscription_id, FiltersList([filter1]))
        relay_manager.run_sync()

        posts = {}
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            event_id = event_msg.event.id
            if event_id not in posts:
                posts[event_id] = event_msg.event.to_dict()
        return list(posts.values())

    def get_metadata_for_pubkey(self, public_key: str | PrivateKey = None) -> Optional[Metadata]:
        relay_manager = self.get_relay_manager()
        public_key = get_public_key(public_key if isinstance(public_key, str) else public_key.hex()) if public_key else self.public_key
        filters = FiltersList(
            [  # enter filter condition
                Filters(
                    kinds=[EventKind.SET_METADATA],
                    authors=[
                        public_key.hex(),
                    ],
                    limit=1
                )
            ]
        )

        subscription_id = uuid.uuid1().hex
        relay_manager.add_subscription_on_all_relays(subscription_id, filters)
        relay_manager.run_sync()
        messages = []
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            logger.info(event_msg.event.to_dict())
            messages.append(event_msg.event.to_dict())
            break
        if len(messages) > 0:
            latest_metadata: dict = sorted(messages, key=lambda x: x['created_at'], reverse=True)[0]
            return Metadata.from_dict(latest_metadata)
        else:
            return None

    def update_metadata(self,
                        name: Optional[str] = None,
                        about: Optional[str] = None,
                        nip05: Optional[str] = None,
                        picture: Optional[str] = None,
                        banner: Optional[str] = None,
                        lud16: Optional[str] = None,
                        lud06: Optional[str] = None,
                        username: Optional[str] = None,
                        display_name: Optional[str] = None,
                        website: Optional[str] = None):
        previous_metadata = self.get_metadata_for_pubkey(self.public_key)

        metadata = Metadata()
        if previous_metadata:
            metadata.set_metadata(previous_metadata.metadata_to_dict())

        if name:
            metadata.name = name
        if about:
            metadata.about = about
        if nip05:
            metadata.nip05 = nip05
        if picture:
            metadata.picture = picture
        if banner:
            metadata.banner = banner
        if lud16:
            metadata.lud16 = lud16
        if lud06:
            metadata.lud06 = lud06
        if username:
            metadata.username = username
        if display_name:
            metadata.display_name = display_name
        if website:
            metadata.website = website

        metadata.created_at = int(time.time())
        metadata.update()

        if previous_metadata and previous_metadata.content == metadata.content:
            print("No changes in metadata, skipping update.")
            return

        event = self.sign(metadata.to_event())
        relay_manager = self.get_relay_manager(timeout=5)

        relay_manager.publish_event(event)
        relay_manager.run_sync()

    def send_direct_message_to_pubkey(self,
                                      recipient_pubkey: str,
                                      message: str):
        recipient = get_public_key(recipient_pubkey)
        dm = EncryptedDirectMessage()
        if isinstance(message, dict):
            message = json.dumps(message)
        dm.encrypt(
            self.private_key.hex(),
            cleartext_content=message,
            recipient_pubkey=recipient.hex(),
        )

        dm_event = dm.to_event()
        dm_event.sign(self.private_key.hex())

        relay_manager = self.get_relay_manager()
        relay_manager.publish_message(dm_event.to_message())
        relay_manager.run_sync()

    def direct_message_listener(self,
                                callback: Callable[[Event, str], Any],
                                recipient_pubkey: str = None,
                                timeout: int = 0,
                                timestamp: int = None,
                                close_after_first_message: bool = False):
        if recipient_pubkey:
            authors = [get_public_key(recipient_pubkey).hex()]
        else:
            authors = None

        filters = FiltersList(
            [
                Filters(
                    authors=authors,
                    kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE],
                    since=timestamp or get_timestamp(),
                    limit=10,
                )
            ]
        )

        subscription_id = uuid.uuid1().hex

        def print_dm(message_json, *args):
            message_type = message_json[0]
            success = False
            if message_type == RelayMessageType.EVENT:
                event = Event.from_dict(message_json[2])
                if event.kind == EventKind.ENCRYPTED_DIRECT_MESSAGE:
                    if event.id in ack:
                        return
                    ack.add(event.id)
                    if event.has_pubkey_ref(self.public_key.hex()):
                        rdm = EncryptedDirectMessage.from_event(event)
                        rdm.decrypt(self.private_key.hex(), public_key_hex=event.pubkey)
                        success = callback(event, rdm.cleartext_content)
                        logging.info(f"New dm received:{event.date_time()} {rdm.cleartext_content}")
            elif message_type == RelayMessageType.OK:
                logging.info(message_json)
            elif message_type == RelayMessageType.NOTICE:
                logging.info(message_json)
            if success and close_after_first_message:
                relay_manager.close_subscription_on_all_relays(subscription_id)

        relay_manager = self.get_relay_manager(message_callback=print_dm, timeout=timeout)
        relay_manager.add_subscription_on_all_relays(subscription_id, filters)
        relay_manager.run_sync()


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Get the environment variables
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('AGENT_PRIVATE_KEY')
    server_public_key = PrivateKey.from_nsec(os.getenv('MCP_MATH_PRIVATE_KEY')).public_key.hex()

    # Create an instance of NostrClient
    client = NostrClient(relays, private_key, None)
    events = client.read_posts_by_tag('mcp_tool_discovery')
    print([event.to_dict() for event in events])