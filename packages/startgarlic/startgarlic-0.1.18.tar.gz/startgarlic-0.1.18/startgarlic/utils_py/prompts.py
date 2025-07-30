from typing import List, Dict
from urllib.parse import quote
import pandas as pd

from .database import DatabaseManager  # Add this import at the top

class PromptManager:
    def __init__(self):
        self.tracking_params = {
            "ref": "garlic",
            "utm_source": "garlic",
            "utm_medium": "llm_ad",
            "utm_campaign": "contextual"
        }
        self.tracking_base_url = "https://startgarlic.com/redirect"
        self.db = DatabaseManager()  # Initialize DatabaseManager

    def add_tracking_params(self, url: str, company_id: str = None) -> str:
        """Create tracking URL with redirect service"""
        try:
            if not url or not company_id:
                return url
                
            # URL encode the destination URL
            encoded_url = quote(url, safe='')
            
            # Use redirect service to track clicks
            tracked_url = f"{self.tracking_base_url}?url={encoded_url}&cid={company_id}"
            return tracked_url
        except Exception:
            return url
    def format_prompt(self, query: str, campaigns: List[dict], users: pd.DataFrame) -> str:
        """Format prompt with campaign and company information"""
        try:
            if campaigns and len(campaigns) > 0:
                campaign = campaigns[0]
                if campaign.get('similarity', 0) > 0.3:
                    # Get user/company info from Supabase
                    user_id = campaign.get('user_id')
                    # print(f"Looking up user: {user_id}")  # Debug log
                    
                    user_data = self.db.get_user_data(user_id)
                    # print(f"Found user data: {user_data}")  # Debug log
                    
                    company_name = user_data['company'].iloc[0] if not user_data.empty else "Company"
                    # print(f"Company name: {company_name}")  # Debug log
                    
                    # Rest of the code remains the same
                    product_name = campaign.get('product_name', 'Product')
                    product_url = campaign.get('product_url', '')
                    
                    tracked_url = self.add_tracking_params(
                        product_url,
                        campaign.get('id')
                    ) if product_url else ''
                    
                    ad_text = f"\nAD {company_name} {product_name} {tracked_url}"
                    return ad_text
                    
            return ""
        except Exception as e:
            print(f"Error formatting prompt: {e}")
            print(f"Error type: {type(e)}")  # Additional error info
            return ""
    def format_recommendation_prompt(self, query: str, main_response: str) -> str:
        """Format prompt for generating follow-up recommendations"""
        return f"""Based on this conversation:

        User Query: "{query}"
        Assistant Response: "{main_response}"

        Generate ONE natural follow-up suggestion that:
        - Adds value to the conversation
        - Relates to the user's interests
        - Encourages learning more
        - Feels like a natural continuation

        Format: Start with "💡" and make it sound conversational.
        Example: "💡 Have you considered exploring quantum computing's impact on cybersecurity? It's another fascinating application in finance!"
        """