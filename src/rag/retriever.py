"""High-level retriever interface for agents"""
from typing import List, Dict
from pathlib import Path
from src.rag.embeddings import EmbeddingGenerator
from src.rag.vector_store import VectorStore
from src.data.card_loader import CardLoader
from src.config import VECTOR_DB_PATH, TOP_K_RETRIEVAL

class CardRetriever:
    """High-level interface for retrieving relevant cards"""
    
    def __init__(self, vector_db_path: Path = VECTOR_DB_PATH):
        self.embedder = EmbeddingGenerator()
        self.embedder.load_model()
        
        self.vector_store = VectorStore()
        self.vector_store.load(vector_db_path)
        
        self.card_loader = CardLoader()
        self.cards_dict = {c['card_id']: c for c in self.card_loader.load_cards()}
    
    def search(self, query: str, k: int = TOP_K_RETRIEVAL) -> List[Dict]:
        """Search for cards relevant to query"""
        # Generate query embedding
        query_embedding = self.embedder.embed_text(query)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, k=k)
        
        # Get full card data for each result
        cards = []
        for chunk, distance in results:
            card_id = chunk['card_id']
            if card_id in self.cards_dict:
                card = self.cards_dict[card_id].copy()
                card['_relevance_score'] = distance
                cards.append(card)
        
        return cards
    
    def search_by_feature(self, feature: str, k: int = TOP_K_RETRIEVAL) -> List[Dict]:
        """Search for cards with a specific feature"""
        query = f"credit card with {feature}"
        return self.search(query, k=k)
    
    def search_by_category(self, category: str, k: int = TOP_K_RETRIEVAL) -> List[Dict]:
        """Search for cards best for a spending category"""
        query = f"best credit card for {category} rewards"
        return self.search(query, k=k)
    
    def get_all_cards(self) -> List[Dict]:
        """Get all cards (for card evaluator)"""
        return self.card_loader.load_cards()
