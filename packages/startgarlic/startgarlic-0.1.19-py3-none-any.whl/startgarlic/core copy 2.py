import warnings
import os
# Suppress all torch warnings at startup
os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning'
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*torch.classes.*')

from .utils_py.database import DatabaseManager
from .utils_py.embeddings import EmbeddingManager
from .utils_py.auction import AuctionManager
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

class Garlic:
    def __init__(self, api_key: str):
        """Initialize Garlic with API key"""
        self.api_key = api_key
        
        # Initialize database manager with the API key
        self.db_manager = DatabaseManager()
        
        # Verify API key and store key_id
        is_valid, self.key_id = self.db_manager.verify_api_key(api_key)
        
        if not is_valid:
            print("Warning: Invalid API key")
            # Don't raise exception, just log the issue
            self.key_id = "invalid-key"
        
        # Initialize other managers
        self.embedding_manager = EmbeddingManager()
        self.auction_manager = AuctionManager()
        
    def find_advertisement(self, query: str, user_id: Optional[str] = None, context: Optional[Dict] = None) -> Dict:
        """Find the most relevant advertisement for a query"""
        try:
            # Log the request
            print(f"Finding advertisement for query: {query[:30]}...")
            
            # Check if database manager is available
            if self.db_manager is None:
                print("Database manager not available, returning fallback ad")
                return self._get_fallback_ad()
            
            # Get all active campaigns
            campaigns = self.db_manager.get_active_campaigns()
            
            if campaigns.empty:
                print("No active campaigns found")
                return self._get_fallback_ad()
            
            # Create embeddings for campaign descriptions
            campaign_embeddings = self.embedding_manager.create_embeddings(campaigns)
            
            if len(campaign_embeddings) == 0:
                print("No valid embeddings created")
                return self._get_fallback_ad()
            
            # Get similarities between query and campaign descriptions
            similarities = self.embedding_manager.get_similarities(query, campaign_embeddings)
            
            if len(similarities) == 0:
                print("No similarities calculated")
                return self._get_fallback_ad()
            
            # Add similarities to campaigns dataframe
            campaigns['similarity'] = similarities
            
            # Get bids for campaigns
            campaign_bids = self.db_manager.get_campaign_bids()
            
            if campaign_bids.empty:
                print("No campaign bids found")
                # Still continue with default bids
            
            # Run auction to select winning ad
            winning_campaign = self.auction_manager.run_auction(campaigns, campaign_bids, context)
            
            if winning_campaign is None:
                print("No winning campaign from auction")
                return self._get_fallback_ad()
            
            # Log the impression
            self.db_manager.log_impression(winning_campaign['id'], self.key_id, query)
            
            # Format the response
            return {
                'company': winning_campaign.get('company', 'Unknown Company'),
                'product_name': winning_campaign.get('product_name', winning_campaign.get('name', 'Unknown Product')),
                'product_url': winning_campaign.get('product_url', winning_campaign.get('website', 'https://example.com')),
                'tracking_url': self._create_tracking_url(winning_campaign['id'], query)
            }
            
        except Exception as e:
            print(f"Error finding advertisement: {e}")
            return self._get_fallback_ad()
    
    def _create_tracking_url(self, campaign_id: str, query: str) -> str:
        """Create a tracking URL for the ad click"""
        base_url = "https://track.startgarlic.com/click"
        tracking_params = f"?campaign={campaign_id}&key={self.key_id}&q={query[:50]}"
        return f"{base_url}{tracking_params}"
    
    def _get_fallback_ad(self) -> Dict:
        """Return a fallback ad when no suitable ad is found"""
        return {
            'company': 'StartGarlic',
            'product_name': 'AI-Powered Advertising',
            'product_url': 'https://startgarlic.com',
            'tracking_url': 'https://track.startgarlic.com/fallback'
        }
        
    def generate_response(self, query: str, chat_history=None) -> str:
        """Generate a response with an embedded advertisement"""
        try:
            # Find an advertisement
            ad = self.find_advertisement(query)
            
            # Format the ad as a string
            ad_text = f"🎓 {ad['company']}'s {ad['product_name']}\n{ad['tracking_url']}"
            
            return ad_text
        except Exception as e:
            print(f"Error in generate_response: {e}")
            return ""
