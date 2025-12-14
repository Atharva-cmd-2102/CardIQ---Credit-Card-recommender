"""Generate embeddings for text chunks"""
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL

class EmbeddingGenerator:
    """Generates embeddings using sentence transformers"""
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self.model = None
    
    def load_model(self):
        """Load the embedding model"""
        if self.model is None:
            print(f"Loading embedding model: {self.model_name}...")
            self.model = SentenceTransformer(self.model_name)
            print("✅ Model loaded successfully")
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text"""
        if self.model is None:
            self.load_model()
        return self.model.encode(text, convert_to_numpy=True)
    
    def embed_texts(self, texts: List[str], show_progress: bool = True) -> np.ndarray:
        """Generate embeddings for multiple texts"""
        if self.model is None:
            self.load_model()
        
        print(f"Generating embeddings for {len(texts)} texts...")
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=show_progress
        )
        print(f"✅ Generated {len(embeddings)} embeddings")
        return embeddings
    
    def embed_chunks(self, chunks: List[dict]) -> np.ndarray:
        """Generate embeddings for card text chunks"""
        texts = [chunk['text'] for chunk in chunks]
        return self.embed_texts(texts)
