import numpy as np
from typing import List, Dict
import pandas as pd

class AuctionManager:
    def __init__(self):
        """Initialize auction manager"""
        self.context_threshold = 0.3    # Minimum similarity threshold
        self.context_weight = 2.0       # Weight for context relevance
        self.min_bid = 0.1              # Minimum required bid
        self.similarity_weight = 0.7    # Weight for similarity in scoring
        self.bid_weight = 0.3           # Weight for bid amount in scoring
        
    def is_relevant(self, similarity: float) -> bool:
        """Determine if an ad is relevant based on context similarity"""
        return similarity >= self.context_threshold
        
    def has_valid_bid(self, bid: float) -> bool:
        """Check if bid meets minimum requirement"""
        return bid >= self.min_bid
        
    def calculate_score(self, bid: float, similarity: float) -> float:
        """Calculate combined score for valid bids"""
        return bid * (similarity ** self.context_weight)
        
    def select_ad(self, candidates: List[dict], bids: pd.DataFrame) -> List[dict]:
        """Select ad based on relevance and bid amount"""
        try:
            if not candidates:
                return []
            
            # Create a DataFrame from candidates for easier manipulation
            candidates_df = pd.DataFrame(candidates)
            
            # Ensure we have similarity scores
            if 'similarity' not in candidates_df.columns:
                return []  # No similarity scores, don't show ads
            
            # Filter out candidates with similarity below threshold
            candidates_df = candidates_df[candidates_df['similarity'] >= self.context_threshold]
            
            if candidates_df.empty:
                return []  # No candidates meet similarity threshold
            
            # Merge with bids data
            if bids.empty:
                return []  # No bids, don't show ads
                
            # Convert campaign_id to string if it's not already
            # Using the recommended approach instead of is_object()
            from pandas.api.types import is_object_dtype
            if not is_object_dtype(bids.index):
                bids.index = bids.index.astype(str)
            
            # Ensure candidates_df['id'] is string type
            candidates_df['id'] = candidates_df['id'].astype(str)
            
            # Create a copy of bids with reset index
            bids_reset = bids.reset_index()
            
            # Merge on campaign_id
            merged = pd.merge(
                candidates_df,
                bids_reset,
                left_on='id',
                right_on='campaign_id',
                how='inner'  # Only keep matches with bids
            )
            
            if merged.empty:
                return []  # No candidates with bids
            
            # Filter out bids below minimum
            merged = merged[merged['bid_amount'] >= self.min_bid]
            
            if merged.empty:
                return []  # No bids meet minimum requirement
            
            # Calculate weighted score
            merged['score'] = (
                merged['similarity'] * self.similarity_weight + 
                merged['bid_amount'] * self.bid_weight
            )
            
            # Sort by score and select top ad
            merged = merged.sort_values('score', ascending=False)
            
            if merged.empty:
                return []
                
            # Return the top candidate as a list with one dict
            top_candidate = merged.iloc[0].to_dict()
            
            # Clean up the result to match expected format
            result = {
                'id': top_candidate['id'],
                'user_id': top_candidate['user_id'],
                'name': top_candidate['name'],
                'product_name': top_candidate['product_name'],
                'product_url': top_candidate['product_url'],
                'similarity': float(top_candidate['similarity'])
            }
            
            return [result]
            
        except Exception as e:
            print(f"Error in ad selection: {e}")
            print(f"Error details: {str(e)}")
            return []