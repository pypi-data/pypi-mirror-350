import numpy as np
from typing import List, Dict
import pandas as pd

class AuctionManager:
    def __init__(self):
        """Initialize auction manager"""
        self.context_threshold = 0.3    # Minimum similarity threshold
        self.context_weight = 2.0       # Weight for context relevance
        self.min_bid = 0.1              # Minimum required bid
        
    def is_relevant(self, similarity: float) -> bool:
        """Determine if an ad is relevant based on context similarity"""
        return similarity >= self.context_threshold
        
    def has_valid_bid(self, bid: float) -> bool:
        """Check if bid meets minimum requirement"""
        return bid >= self.min_bid
        
    def calculate_score(self, bid: float, similarity: float) -> float:
        """Calculate combined score for valid bids"""
        return bid * (similarity ** self.context_weight)
        
    def select_ad(self, campaigns: List[Dict], campaign_bids: pd.DataFrame) -> List[Dict]:
        """Select ad based on auction mechanism and context relevance"""
        try:
            if not campaigns:
                return []
            
            # Extract similarities and match with bids
            candidates = []
            for campaign in campaigns:
                # Get bid amount from campaign_bids using index
                bid_amount = campaign_bids.loc[campaign['id']]['bid_amount'] if campaign['id'] in campaign_bids.index else 0
                
                candidates.append({
                    'campaign': campaign,
                    'similarity': campaign.get('similarity', 0),
                    'bid': float(bid_amount)
                })
            
            # Filter for both relevance AND valid bids
            valid_candidates = [
                c for c in candidates 
                if self.is_relevant(c['similarity']) and self.has_valid_bid(c['bid'])
            ]
            
            # If no valid candidates, return empty
            if not valid_candidates:
                return []
                
            # Calculate scores for valid candidates
            for candidate in valid_candidates:
                candidate['score'] = self.calculate_score(
                    candidate['bid'],
                    candidate['similarity']
                )
            
            # Sort by combined score
            valid_candidates.sort(key=lambda x: x['score'], reverse=True)
            
            # Return the top candidate's campaign data
            return [valid_candidates[0]['campaign']] if valid_candidates else []
            
        except Exception as e:
            print(f"Error in ad selection: {e}")
            print(f"Error details: {str(e)}")
            return [] 