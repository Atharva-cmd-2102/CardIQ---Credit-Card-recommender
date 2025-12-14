"""FAISS vector store for card embeddings"""
import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict, Tuple
from src.config import VECTOR_DB_PATH

class VectorStore:
    """FAISS-based vector store for card embeddings"""
    
    def __init__(self):
        self.index = None
        self.chunks = None
        self.dimension = None
    
    def build_index(self, embeddings: np.ndarray, chunks: List[Dict]):
        """Build FAISS index from embeddings"""
        self.dimension = embeddings.shape[1]
        self.chunks = chunks
        
        print(f"Building FAISS index with dimension {self.dimension}...")
        
        # Use L2 distance for similarity
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
        print(f"✅ Index built with {self.index.ntotal} vectors")
    
    def save(self, path: Path = VECTOR_DB_PATH):
        """Save index and metadata to disk"""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_path = path / "faiss_index.bin"
        faiss.write_index(self.index, str(index_path))
        print(f"✅ FAISS index saved to {index_path}")
        
        # Save chunks metadata
        metadata_path = path / "card_metadata.pkl"
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.chunks, f)
        print(f"✅ Metadata saved to {metadata_path}")
    
    def load(self, path: Path = VECTOR_DB_PATH):
        """Load index and metadata from disk"""
        path = Path(path)
        
        # Load FAISS index
        index_path = path / "faiss_index.bin"
        if not index_path.exists():
            raise FileNotFoundError(f"Index not found at {index_path}")
        
        self.index = faiss.read_index(str(index_path))
        self.dimension = self.index.d
        print(f"✅ Loaded FAISS index with {self.index.ntotal} vectors")
        
        # Load chunks metadata
        metadata_path = path / "card_metadata.pkl"
        with open(metadata_path, 'rb') as f:
            self.chunks = pickle.load(f)
        print(f"✅ Loaded metadata for {len(self.chunks)} cards")
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for top-k most similar cards"""
        if self.index is None:
            raise ValueError("Index not built or loaded")
        
        # Ensure query is 2D array
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Search
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Return chunks with distances
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.chunks):  # Valid index
                results.append((self.chunks[idx], float(distance)))
        
        return results
