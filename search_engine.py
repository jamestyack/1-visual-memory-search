"""
Vector search engine for semantic screenshot retrieval.
Uses sentence-transformers and ChromaDB for efficient similarity search.
"""

import os
import sys
from typing import List, Dict, Tuple, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

# Fix for Streamlit Cloud SQLite issue
try:
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
except ImportError:
    pass

# Fix for PyTorch meta tensor issues
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'
os.environ['TORCH_SHOW_CPP_STACKTRACES'] = '1'

import chromadb
from chromadb.config import Settings
import hashlib


class SearchEngine:
    """Semantic search engine for screenshot content."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the search engine with embedding model and vector database.
        
        Args:
            model_name: Name of the sentence-transformer model to use
        """
        # Store model name for lazy loading
        self.model_name = model_name
        self.model = None
        
        # Initialize ChromaDB client (in-memory for Streamlit Cloud)
        try:
            # Try basic ephemeral client first
            self.client = chromadb.EphemeralClient()
            print("✅ ChromaDB initialized with EphemeralClient")
        except Exception as e:
            print(f"EphemeralClient failed: {e}")
            try:
                # Fallback to Client with basic settings
                self.client = chromadb.Client(Settings(
                    is_persistent=False,
                    anonymized_telemetry=False,
                    allow_reset=True
                ))
                print("✅ ChromaDB initialized with Client + settings")
            except Exception as e2:
                print(f"ChromaDB Client failed: {e2}")
                try:
                    # Last resort - try with minimal settings
                    self.client = chromadb.Client()
                    print("✅ ChromaDB initialized with default Client")
                except Exception as e3:
                    print(f"❌ All ChromaDB initialization methods failed: {e3}")
                    raise e3
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="screenshots",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Track indexed documents
        self.indexed_docs = {}
        self.doc_count = 0
    
    def _ensure_model_loaded(self):
        """Lazy load the sentence transformer model to avoid initialization issues."""
        if self.model is None:
            try:
                print(f"Loading sentence transformer model: {self.model_name}")
                # Try to initialize with CPU device explicitly to avoid meta tensor issues
                self.model = SentenceTransformer(self.model_name, device='cpu')
                print("✅ Model loaded successfully with CPU device")
            except Exception as e:
                print(f"Failed to initialize with CPU device, trying default: {e}")
                try:
                    # Fallback to default initialization
                    import torch
                    torch.set_default_device('cpu')
                    self.model = SentenceTransformer(self.model_name)
                    print("✅ Model loaded successfully with default settings")
                except Exception as e2:
                    print(f"Model initialization failed: {e2}")
                    try:
                        # Last resort - try with trust_remote_code
                        self.model = SentenceTransformer(self.model_name, trust_remote_code=True, device='cpu')
                        print("✅ Model loaded successfully with trust_remote_code")
                    except Exception as e3:
                        print(f"❌ All model initialization attempts failed: {e3}")
                        raise e3
    
    def _generate_doc_id(self, path: str) -> str:
        """Generate unique document ID from file path."""
        return hashlib.md5(path.encode()).hexdigest()
    
    def index_document(self, document: Dict[str, str]) -> bool:
        """
        Index a single document in the vector database.
        
        Args:
            document: Dictionary with 'path', 'combined_text', and other metadata
        
        Returns:
            Success status
        """
        try:
            # Skip if no text content
            if not document.get('combined_text', '').strip():
                return False
            
            # Generate document ID
            doc_id = self._generate_doc_id(document['path'])
            
            # Skip if already indexed
            if doc_id in self.indexed_docs:
                return True
            
            # Ensure model is loaded
            self._ensure_model_loaded()
            
            # Generate embedding
            embedding = self.model.encode(document['combined_text']).tolist()
            
            # Prepare metadata
            metadata = {
                'path': document['path'],
                'filename': document['filename'],
                'ocr_text_preview': document['ocr_text'][:500] if document['ocr_text'] else '',
                'vision_preview': document['vision_description'][:500] if document['vision_description'] else '',
                'has_ocr': bool(document['ocr_text']),
                'has_vision': bool(document['vision_description'])
            }
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=[embedding],
                metadatas=[metadata],
                documents=[document['combined_text']],
                ids=[doc_id]
            )
            
            # Track indexed document
            self.indexed_docs[doc_id] = document
            self.doc_count += 1
            
            return True
            
        except Exception as e:
            print(f"Failed to index document {document.get('path', 'unknown')}: {e}")
            return False
    
    def index_batch(self, documents: List[Dict[str, str]]) -> int:
        """
        Index multiple documents in batch.
        
        Args:
            documents: List of document dictionaries
        
        Returns:
            Number of successfully indexed documents
        """
        success_count = 0
        
        # Filter valid documents
        valid_docs = [doc for doc in documents if doc.get('combined_text', '').strip()]
        
        if not valid_docs:
            return 0
        
        # Ensure model is loaded
        self._ensure_model_loaded()
        
        # Prepare batch data
        ids = []
        embeddings = []
        metadatas = []
        texts = []
        
        for doc in valid_docs:
            doc_id = self._generate_doc_id(doc['path'])
            
            # Skip if already indexed
            if doc_id in self.indexed_docs:
                continue
            
            ids.append(doc_id)
            embeddings.append(self.model.encode(doc['combined_text']).tolist())
            texts.append(doc['combined_text'])
            metadatas.append({
                'path': doc['path'],
                'filename': doc['filename'],
                'ocr_text_preview': doc['ocr_text'][:500] if doc['ocr_text'] else '',
                'vision_preview': doc['vision_description'][:500] if doc['vision_description'] else '',
                'has_ocr': bool(doc['ocr_text']),
                'has_vision': bool(doc['vision_description'])
            })
            
            self.indexed_docs[doc_id] = doc
            success_count += 1
        
        # Add to ChromaDB if there are new documents
        if ids:
            try:
                self.collection.add(
                    embeddings=embeddings,
                    metadatas=metadatas,
                    documents=texts,
                    ids=ids
                )
                self.doc_count += len(ids)
            except Exception as e:
                print(f"Batch indexing failed: {e}")
                success_count = 0
        
        return success_count
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Search for documents similar to the query.
        
        Args:
            query: Search query text
            top_k: Number of top results to return
        
        Returns:
            List of (document_metadata, confidence_score) tuples
        """
        try:
            # Check if we have indexed documents
            if self.doc_count == 0:
                return []
            
            # Ensure model is loaded
            self._ensure_model_loaded()
            
            # Generate query embedding
            query_embedding = self.model.encode(query).tolist()
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, self.doc_count)
            )
            
            # Format results
            formatted_results = []
            if results['metadatas'] and results['distances']:
                for metadata, distance in zip(results['metadatas'][0], results['distances'][0]):
                    # Convert distance to similarity score (1 - cosine distance)
                    confidence = 1.0 - distance
                    formatted_results.append((metadata, confidence))
            
            return formatted_results
            
        except Exception as e:
            print(f"Search failed: {e}")
            return []
    
    def clear_index(self):
        """Clear all indexed documents."""
        try:
            # Delete and recreate collection
            self.client.delete_collection("screenshots")
            self.collection = self.client.create_collection(
                name="screenshots",
                metadata={"hnsw:space": "cosine"}
            )
            self.indexed_docs = {}
            self.doc_count = 0
        except Exception as e:
            print(f"Failed to clear index: {e}")
    
    def get_stats(self) -> Dict:
        """
        Get search engine statistics.
        
        Returns:
            Dictionary with engine statistics
        """
        stats = {
            'total_documents': self.doc_count,
            'model_name': self.model_name,
            'indexed_files': list(self.indexed_docs.keys())
        }
        
        # Only add embedding dimension if model is loaded
        if self.model is not None:
            try:
                stats['embedding_dimension'] = self.model.get_sentence_embedding_dimension()
            except:
                stats['embedding_dimension'] = 'Unknown (model not loaded)'
        else:
            stats['embedding_dimension'] = 'Not loaded yet'
            
        return stats