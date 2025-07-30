import warnings
import os
# Suppress all torch warnings at startup
os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning'
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*torch.classes.*')

from .utils_py.logging_config import configure_logging
configure_logging()

from .utils_py.database import DatabaseManager
from .utils_py.embeddings import EmbeddingManager
# from .utils.analytics import AnalyticsManager
from .utils_py.prompts import PromptManager
from .utils_py.auction import AuctionManager
from typing import List, Dict, Optional
# import numpy as np
import gc
import torch

class Garlic:
    def __init__(self, api_key: str):
        """Initialize RAG system with API key authentication"""
        if not api_key:
            raise ValueError("API key is required")
            
        try:
            # Clear memory before initialization
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
            self.db = DatabaseManager()
            api_key = api_key.strip().strip('"\'')
            
            is_valid, self.key_id = self.db.verify_api_key(api_key)
            if not is_valid:
                raise ValueError("Invalid API key")
            
            # Initialize with memory management
            self.embedding_manager = EmbeddingManager()
            self.prompt_manager = PromptManager()
            self.auction_manager = AuctionManager()
            
            # Load campaigns data
            self.df = self.db.get_campaigns()
            
            # Check and update missing embeddings
            self._update_missing_embeddings()
            
        except Exception as e:
            raise

    def _update_missing_embeddings(self):
        """Check and update any missing embeddings in campaigns"""
        try:
            # Filter campaigns with missing embeddings
            missing_embeddings = self.df[self.df['embedding'].isna() & self.df['product_description'].notna()]
            
            if not missing_embeddings.empty:
                # print(f"Found {len(missing_embeddings)} campaigns with missing embeddings. Updating...")
                
                # Process each campaign with missing embedding
                for idx, campaign in missing_embeddings.iterrows():
                    description = campaign['product_description']
                    if description and isinstance(description, str):
                        # Create embedding for the description
                        embedding = self.embedding_manager.create_single_embedding(description)
                        
                        if len(embedding) > 0:
                            # Update the embedding in the database
                            self.db.update_campaign_embedding(campaign['id'], embedding.tolist())
                            
                            # Update the dataframe in memory
                            self.df.at[idx, 'embedding'] = embedding.tolist()
                
                # print("Embedding updates completed")
            
        except Exception as e:
            print(f"Error updating missing embeddings: {e}")

    def find_similar_campaigns(self, query: str, top_k: int = 5) -> List[dict]:
        """Find campaigns similar to the query"""
        try:
            query_embedding = self.embedding_manager.embed_query(query)
            
            if len(query_embedding) == 0:
                return []
            
            query_embedding = query_embedding.tolist()
            
            # Use campaign search instead of companies
            results = self.db.search_similar_campaigns(query_embedding, top_k)
            
            return results
            
        except Exception as e:
            print(f"Error finding similar campaigns: {e}")
            return []

    def generate_response(self, query: str, chat_history: Optional[List] = None) -> str:
        """Generate ad response based on context and bids"""
        try:
            self.db.log_api_call(self.key_id, 'generate')
            
            # Get candidate campaigns
            candidates = self.find_similar_campaigns(query)
            # print(f"Found {len(candidates)} candidates: {candidates}")
            
            # Get campaign bids
            campaign_bids = self.db.get_campaign_bids([c['id'] for c in candidates])
            
            # Select ad through auction mechanism
            selected_campaigns = self.auction_manager.select_ad(candidates, campaign_bids)
            # print(f"Selected campaigns: {selected_campaigns}")
            
            # Format response and increment views
            if selected_campaigns:
                ad_response = self.prompt_manager.format_prompt(
                    query, 
                    selected_campaigns, 
                    self.df  # Pass campaigns DataFrame for user info
                )
                
                # Increment views for selected campaign
                self.db.increment_campaign_views(selected_campaigns)
                
                return ad_response
            
            return ""

        except Exception as e:
            print(f"Error in generate_response: {e}")
            self.db.log_api_call(self.key_id, 'generate', 'error')
            return ""

    def parse_response(self, response: Dict) -> Dict:
        """Parse the response into a clean format"""
        return {
            "query": response.get("query"),
            "response": response.get("response", ""),
            "recommendation": response.get("recommendation", ""),
            "companies": response.get("companies", [])
        }