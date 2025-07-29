from typing import List, Dict, Any
from agentstr.nostr_client import NostrClient
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

class NostrRAG:
    """A Retrieval-Augmented Generation (RAG) system for querying Nostr events.

    This class integrates with the Nostr protocol to fetch events based on tags,
    builds a knowledge base using a vector store, and supports querying the knowledge
    base with optional questions. It uses embeddings to enable similarity-based retrieval.

    Attributes:
        nostr_client (NostrClient): Client for interacting with Nostr relays.
        embeddings (Any): Embedding model for vectorizing documents (defaults to FakeEmbeddings).
        vector_store (InMemoryVectorStore): Vector store for storing and querying documents.
    """
    def __init__(self, nostr_client: NostrClient = None, vector_store=None, relays: List[str] = None,
                 private_key: str = None, nwc_str: str = None, embeddings=None):
        """Initialize the NostrRAG system.

        Args:
            nostr_client: An existing NostrClient instance (optional).
            vector_store: An existing vector store instance (optional).
            relays: List of Nostr relay URLs (if no client provided).
            private_key: Nostr private key in 'nsec' format (if no client provided).
            nwc_str: Nostr Wallet Connect string for payments (optional).
            embeddings: Embedding model for vectorizing documents (defaults to FakeEmbeddings with size 256).
        """
        self.nostr_client = nostr_client or NostrClient(relays=relays, private_key=private_key, nwc_str=nwc_str)
        self.embeddings = embeddings or FakeEmbeddings(size=256)
        self.vector_store = vector_store or InMemoryVectorStore(self.embeddings)

    def _process_event(self, event: Dict[str, Any]) -> Document:
        """Process a Nostr event into a LangChain Document.

        Args:
            event: A dictionary containing the Nostr event data.

        Returns:
            Document: A LangChain Document with the event's content and ID.
        """
        content = event.get('content', '')
        return Document(page_content=content, id=event.get('id'))

    def _build_knowledge_base(self, tags: List[str], limit: int = 50) -> None:
        """Build a knowledge base from Nostr events matching the specified tags.

        Fetches events from Nostr relays, converts them to documents, and stores them
        in the vector store for similarity-based querying.

        Args:
            tags: List of tags to filter Nostr events.
            limit: Maximum number of events to retrieve (default: 50).
        """
        events = self.nostr_client.read_posts_by_tag(tags=tags, limit=limit)
        documents = [self._process_event(event) for event in events]
        self.vector_store.add_documents(documents=documents)

    def query(self, tags: List[str], question: str = None, limit: int = 50) -> List[str]:
        """Query the knowledge base for relevant Nostr event content.

        Builds a knowledge base from events matching the provided tags and performs
        a similarity search using the question or tags. Clears the knowledge base after
        querying to free memory.

        Args:
            tags: List of tags to filter Nostr events for building the knowledge base.
            question: Optional question to use for similarity search (defaults to tags if None).
            limit: Maximum number of events to retrieve for the knowledge base (default: 50).

        Returns:
            List[str]: List of content strings from the most relevant documents.
        """
        self._build_knowledge_base(tags, limit=limit)
        result = [doc.page_content for doc in self.vector_store.similarity_search(question or tags)]
        self._clear_knowledge_base()
        return result

    def _add_to_knowledge_base(self, event: Dict[str, Any]) -> None:
        """Add a single Nostr event to the existing knowledge base.

        Args:
            event: A dictionary containing the Nostr event data to add.

        Raises:
            ValueError: If the vector store is not initialized.
        """
        if not self.vector_store:
            raise ValueError("Knowledge base not initialized. Call build_knowledge_base() first.")
        document = self._process_event(event)
        self.vector_store.add_documents([document])

    def _clear_knowledge_base(self) -> None:
        """Clear the current knowledge base by resetting the vector store.

        This method resets the vector store to None, freeing memory used by the
        knowledge base. A new vector store must be initialized before further use.
        """
        self.vector_store = None

# Example usage:
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    relays = os.getenv('NOSTR_RELAYS').split(',')
    private_key = os.getenv('AGENT_PRIVATE_KEY')
    rag = NostrRAG(relays=relays, private_key=private_key)
    print(rag.query(tags=['bitcoin', 'btc'], question="What's new with Bitcoin?"))