import json
from typing import List, Dict, Any, Optional
from agentstr.nostr_client import NostrClient
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

class NostrRAG:
    """A Retrieval-Augmented Generation (RAG) system for querying Nostr events.

    This class integrates with the Nostr protocol to fetch events based on tags,
    builds a knowledge base using a vector store, and supports querying the knowledge
    base with optional questions. It uses embeddings to enable similarity-based retrieval.

    Attributes:
        nostr_client (NostrClient): Client for interacting with Nostr relays.
        embeddings (Any): Embedding model for vectorizing documents (defaults to FakeEmbeddings).
        vector_store (InMemoryVectorStore): Vector store for storing and querying documents.
        llm (ChatOpenAI): Language model for generating responses.
    """
    def __init__(self, nostr_client: NostrClient = None, vector_store=None, relays: List[str] = None,
                 private_key: str = None, nwc_str: str = None, embeddings=None, llm=None, llm_model_name=None, llm_base_url=None, llm_api_key=None):
        """Initialize the NostrRAG system.

        Args:
            nostr_client: An existing NostrClient instance (optional).
            vector_store: An existing vector store instance (optional).
            relays: List of Nostr relay URLs (if no client provided).
            private_key: Nostr private key in 'nsec' format (if no client provided).
            nwc_str: Nostr Wallet Connect string for payments (optional).
            embeddings: Embedding model for vectorizing documents (defaults to FakeEmbeddings with size 256).
            llm: Language model (optional).
            llm_model_name: Name of the language model to use (optional).
            llm_base_url: Base URL for the language model (optional).
            llm_api_key: API key for the language model (optional).
        """
        self.nostr_client = nostr_client or NostrClient(relays=relays, private_key=private_key, nwc_str=nwc_str)
        self.embeddings = embeddings or FakeEmbeddings(size=256)
        self.vector_store = vector_store or InMemoryVectorStore(self.embeddings)
        if llm is None and llm_model_name is None:
            raise ValueError("llm or llm_model_name must be provided")
        self.llm = llm or ChatOpenAI(model_name=llm_model_name, base_url=llm_base_url, api_key=llm_api_key, temperature=0)

    def _select_hashtags(self, question: str, previous_hashtags: List[str] = None) -> List[str]:
        """Select relevant hashtags for the given question.

        Args:
            question: The user's question
            previous_hashtags: Previously used hashtags for this conversation

        Returns:
            List of relevant hashtags
        """
        template = """
You are a hashtag selector for Nostr. Given a question, suggest relevant hashtags that would help find relevant content.
Return ONLY the hashtags in a JSON array format, like: ["#hashtag1", "#hashtag2"]
Use at most 5 hashtags.

Question: {question}
Previous hashtags: {history}
"""
        
        history = json.dumps(previous_hashtags or [])
        prompt = template.format(question=question, history=history)
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            hashtags = json.loads(response.content)
            return hashtags
        except json.JSONDecodeError:
            # If the response isn't valid JSON, try to extract hashtags
            text = response.content
            hashtags = []
            # Find hashtags in the text
            for word in text.split():
                if word.startswith('#'):
                    hashtags.append(word)
            return hashtags[:5]  # Return at most 5 hashtags

    def _process_event(self, event: Dict[str, Any]) -> Document:
        """Process a Nostr event into a LangChain Document.

        Args:
            event: A dictionary containing the Nostr event data.

        Returns:
            Document: A LangChain Document with the event's content and ID.
        """
        content = event.get('content', '')
        return Document(page_content=content, id=event.get('id'))

    def build_knowledge_base(self, question: str, limit: int = 10) -> List[dict]:
        """Build a knowledge base from Nostr events relevant to the question.

        Args:
            question: The user's question to guide hashtag selection
            limit: Maximum number of posts to retrieve

        Returns:
            List of retrieved events
        """
        # Select relevant hashtags for the question
        hashtags = self._select_hashtags(question)
        hashtags = [hashtag.lstrip('#') for hashtag in hashtags]

        print(f"Selected hashtags: {hashtags}")

        # Fetch events for each hashtag
        events = self.nostr_client.read_posts_by_tag(tags=hashtags, limit=limit)
        
        # Process events into documents
        documents = [self._process_event(event) for event in events]
        
        self.vector_store.add_texts([doc.page_content for doc in documents])
        
        return events

    def query(self, question: str) -> str:
        """Ask a question using the knowledge base.

        Args:
            question: The user's question

        Returns:
            The generated response
        """

        self.build_knowledge_base(question)

        # Get relevant documents
        relevant_docs = self.vector_store.similarity_search(question, k=5)
        
        # Generate response using the LLM
        template = """
You are an expert assistant. Answer the following question based on the provided context.

Question: {question}

Context:
{context}

Answer:"""
        
        prompt = template.format(
            question=question,
            context="\n\n".join([doc.page_content for doc in relevant_docs])
        )
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content