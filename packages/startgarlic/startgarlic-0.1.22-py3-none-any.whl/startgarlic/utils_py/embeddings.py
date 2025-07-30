import warnings
import os
# Set environment variable to ignore warnings
os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning'
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*torch.classes.*')

from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Dict
import numpy as np
import pandas as pd

class EmbeddingManager:
    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
    
    def create_embeddings(self, campaigns: pd.DataFrame) -> np.ndarray:
        """Create embeddings for campaign product descriptions"""
        try:
            # Filter for campaigns with product descriptions
            valid_campaigns = campaigns[campaigns['product_description'].notna()]
            
            if valid_campaigns.empty:
                return np.array([])
                
            descriptions = valid_campaigns['product_description'].tolist()
            embeddings = self.model.embed_documents(descriptions)
            return np.array(embeddings)
        except Exception as e:
            print(f"Error creating embeddings: {e}")
            return np.array([])

    def create_single_embedding(self, description: str) -> np.ndarray:
        """Create embedding for a single new product description"""
        try:
            if not description:
                return np.array([])
            embedding = self.model.embed_documents([description])
            return np.array(embedding[0])
        except Exception as e:
            print(f"Error creating single embedding: {e}")
            return np.array([])

    def get_similarities(self, query: str, campaign_embeddings: np.ndarray) -> np.ndarray:
        """Calculate similarities between query and campaign descriptions"""
        try:
            query_embedding = self.model.embed_query(query)
            query_embedding = np.array(query_embedding)
            
            # Calculate cosine similarity
            similarities = np.dot(campaign_embeddings, query_embedding) / (
                np.linalg.norm(campaign_embeddings, axis=1) * np.linalg.norm(query_embedding)
            )
            
            similarities = np.nan_to_num(similarities, 0)
            return similarities
        except Exception as e:
            print(f"Error calculating similarities: {e}")
            return np.array([])

    def embed_query(self, text: str) -> np.ndarray:
        """Embed a single query"""
        try:
            enhanced_query = f"Find relevant products related to: {text}"
            embedding = self.model.embed_query(enhanced_query)
            return np.array(embedding)
        except Exception as e:
            print(f"Error embedding query: {e}")
            return np.array([])

    def create_query_embedding(self, query: str) -> List[float]:
        """Create embedding for a query string"""
        try:
            embedding = self.model.embed_query(query)
            return embedding
        except Exception as e:
            print(f"Error creating query embedding: {e}")
            return []

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """Embed multiple texts"""
        try:
            embeddings = self.model.embed_documents(texts)
            return np.array(embeddings)
        except Exception as e:
            # print(f"Error embedding documents: {e}")
            return np.array([])

