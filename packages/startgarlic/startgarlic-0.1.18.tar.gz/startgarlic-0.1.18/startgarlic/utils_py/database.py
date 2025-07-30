from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from .config import get_credentials
# import bcrypt
import uuid

class DatabaseManager:
    def __init__(self):
        try:
            # Get credentials using existing config
            credentials = get_credentials()
            
            # Use service_role key for admin operations
            url = credentials.get("url")  
            service_key = credentials.get("service_role_key") or os.getenv("SUPABASE_SERVICE_KEY")
            anon_key = credentials.get("key") or os.getenv("SUPABASE_KEY")
            
            self.supabase_url = url or os.getenv("SUPABASE_URL")
            
            # Ensure we have valid credentials
            # if not self.supabase_url:
            #     raise ValueError("Supabase URL is missing")
                
            # Prioritize service role key for database operations
            self.supabase_key = service_key if service_key else anon_key
            
            # if not self.supabase_key:
            #     raise ValueError("Supabase key is missing")
            
            # Print key type for debugging
            key_type = "service role" if service_key and self.supabase_key == service_key else "anon"
            # print(f"Using {key_type} key for database operations")
            
           
            
            # Initialize Supabase client
            self.supabase = create_client(self.supabase_url, self.supabase_key)
            
            
            
        except Exception as e:
            # print(f"Error initializing database: {e}")
            # print(f"Full error details: {str(e)}")
            # Don't set self.supabase to None, raise the exception to prevent continuing with invalid state
            raise
    
    # def verify_api_key(self, api_key: str) -> tuple:
    #     """Verify API key and return user ID if valid"""
    #     try:
    #         # For development/testing - accept the hardcoded key
    #         test_key = "$2a$06$D2xODJoM9vnBoIpI5mcf8.YtgHmiFqepvtHntN.G51ghWy.rNjcaC"
    #         if api_key == test_key:
    #             print("Using test API key")
    #             return True, "test-user-id"
            
    #         # Regular verification for production
    #         response = self.supabase.table('api_keys').select('user_id, active').eq('key_hash', api_key).execute()
            
    #         if not response.data:
    #             return False, None
                
    #         key_data = response.data[0]
    #         is_active = key_data.get('active', False)
            
    #         if not is_active:
    #             return False, None
                
    #         return True, key_data.get('user_id')
            
    #     except Exception as e:
    #         print(f"Error verifying API key: {e}")
    #         return False, None
    
    def get_user_data(self, user_id: str) -> pd.DataFrame:
            """Get user data including company name"""
            try:
                response = self.supabase.table('users').select(
                    'id, company'
                ).eq('id', user_id).execute()
                
                if response.data:
                    return pd.DataFrame(response.data)
                return pd.DataFrame()
                
            except Exception as e:
                print(f"Error getting user data: {e}")
                return pd.DataFrame()

    def insert_analytics_log(self, product_name: str, interaction_type: str = 'view'):
        """Insert analytics log for product views"""
        try:
            if not product_name or not isinstance(product_name, str):
                return
            
            self.supabase.table('analytics_logs').insert({
                'product_name': product_name,  # Changed from company_name
                'interaction_type': interaction_type,
                'timestamp': datetime.now().isoformat()
            }).execute()
            
        except Exception as e:
            print(f"Error inserting analytics log: {e}")
            pass
    # def update_missing_embeddings(self, companies: pd.DataFrame):
    #     """Update embeddings for companies with null embeddings"""
    #     try:
    #         from .embeddings import EmbeddingManager
    #         embedding_manager = EmbeddingManager()
            
    #         # Create embeddings for companies
    #         embeddings = embedding_manager.create_embeddings(companies)
            
    #         # Update each company with its new embedding
    #         for i, (_, company) in enumerate(companies.iterrows()):
    #             self.supabase.table('ads').update({
    #                 'embedding': embeddings[i].tolist()
    #             }).eq('id', company['id']).execute()
                
    #         # print(f"Updated embeddings for {len(companies)} companies")
            
    #     except Exception as e:
    #         # print(f"Error updating missing embeddings: {e}")
    #         pass  # Added pass statement

    def verify_api_key(self, api_key: str) -> tuple[bool, Optional[str]]:
        """Verify API key and return validity and key ID"""
        try:
            print(f"Verifying API key...")
            result = self.supabase.table('api_keys') \
                .select('id, key, revoked_at') \
                .eq('key', api_key) \
                .is_('revoked_at', 'null') \
                .execute()
            
            if result.data and len(result.data) > 0:
                key_id = result.data[0]['id']
                # print(f"Found valid key with ID: {key_id}")
                print("Key verified")
                return True, key_id
            print("No valid key found")
            return False, None
            
        except Exception as e:
            #print(f"Error verifying API key: {e}")
            return False, None

    def log_api_call(self, api_key_id: str, action: str, status: str = 'success') -> bool:
        """Log API call with status and update last_used timestamp and total_calls"""
        try:
            # First get current total_calls
            current = self.supabase.table('api_keys').select('total_calls').eq('id', api_key_id).single().execute()
            current_calls = current.data.get('total_calls', 0) if current.data else 0
            
            # Update last_used timestamp and increment total_calls
            self.supabase.table('api_keys').update({
                'last_used': datetime.utcnow().isoformat(),
                'total_calls': current_calls + 1
            }).eq('id', api_key_id).execute()
            
            # # Then log the API call with correct column names
            # data = {
            #     'id': str(uuid.uuid4()),
            #     'api_key_id': api_key_id,
            #     'endpoint': action,  # Changed from 'action' to 'endpoint'
            #     'timestamp': datetime.utcnow().isoformat(),  # Changed from 'created_at' to 'timestamp'
            #     'status': status
            # }
            
            # response = self.supabase.table('api_usage_logs').insert(data).execute()
            # return bool(response.data)
            
        except Exception as e:
            # print(f"Error logging API call: {e}")
            return False

    def get_campaigns(self) -> pd.DataFrame:
        """Get all campaigns with their descriptions"""
        try:
            response = self.supabase.table('campaigns').select(
                'id, user_id, name, product_name, product_url, product_description, embedding, views'
            ).eq('status', 'active').execute()
            
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error getting campaigns: {e}")
            return pd.DataFrame()

    
    # def search_similar_campaigns(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
    #             """Search for similar campaigns using vector similarity"""
    #             try:
    #                 # Get campaigns with embeddings
    #                 response = self.supabase.rpc(
    #                     'match_campaigns',
    #                     {
    #                         'query_embedding': query_embedding,
    #                         'match_threshold': 0.5,  # Lower threshold
    #                         'match_count': top_k
    #                     }
    #                 ).execute()
                    
    #                 print(f"Search response: {response}")  # Debug log
                    
    #                 if not response.data:
    #                     return []
                    
    #                 results = []
    #                 for item in response.data:
    #                     if item.get('similarity', 0) > 0.3:
    #                         campaign = {
    #                             'id': item['id'],
    #                             'user_id': item['user_id'],
    #                             'name': str(item['name']),
    #                             'product_name': str(item['product_name']),
    #                             'product_url': str(item['product_url']),
    #                             'similarity': float(item['similarity'])
    #                         }
    #                         results.append(campaign)
                    
    #                 return results
                    
    #             except Exception as e:
    #                 print(f"Error searching similar campaigns: {e}")
    #                 return []

    def search_similar_campaigns(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
            """Search for similar campaigns using vector similarity"""
            try:
                response = self.supabase.rpc(
                    'match_campaigns',
                    {
                        'query_embedding': query_embedding,
                        'match_threshold': 0.3,  # Lowered threshold for more matches
                        'match_count': top_k
                    }
                ).execute()
                
                # print(f"Search response: {response}")  # Debug log
                
                # if not response.data:
                #     return []
                
                results = []
                for item in response.data:
                    campaign = {
                        'id': str(item['id']),  # Convert UUID to string
                        'user_id': str(item['user_id']),
                        'name': str(item['name']),
                        'product_name': str(item['product_name']),
                        'product_url': str(item['product_url']),
                        'similarity': float(item['similarity'])
                    }
                    results.append(campaign)
                
                return results
                
            except Exception as e:
                print(f"Error searching similar campaigns: {e}")
                return []

    # def increment_campaign_views(self, campaigns: List[Dict]) -> bool:
    #     """Increment view count for selected campaigns"""
    #     try:
    #         if not campaigns:
    #             return False
            
    #         campaign_id = campaigns[0].get('id')
    #         if not campaign_id:
    #             return False
            
    #         # Update views count
    #         response = self.supabase.table('campaigns').update({
    #             'views': self.supabase.raw('views + 1')
    #         }).eq('id', campaign_id).execute()
            
    #         return bool(response.data)
            
    #     except Exception as e:
    #         print(f"Error incrementing views: {e}")
    #         return False

    def increment_campaign_views(self, campaigns: List[Dict]) -> bool:
            """Increment view count for selected campaigns"""
            try:
                if not campaigns:
                    return False
                
                campaign_id = campaigns[0].get('id')
                if not campaign_id:
                    return False
                
                # First get current views
                current = self.supabase.table('campaigns').select('views').eq('id', campaign_id).single().execute()
                current_views = current.data.get('views', 0) if current.data else 0
                
                # Update views count
                response = self.supabase.table('campaigns').update({
                    'views': current_views + 1
                }).eq('id', campaign_id).execute()
                
                return bool(response.data)
                
            except Exception as e:
                print(f"Error incrementing views: {e}")
                return False

    def store_campaign_embedding(self, campaign_id: str, product_description: str) -> bool:
        """Store embedding for a new campaign"""
        try:
            # print(f"\nAttempting to create embedding for campaign {campaign_id}")
            # print(f"Product description: {product_description}")
            
            # if not product_description:
            #     print("No product description provided")
            #     return False
            
            # Create embedding for the new product description
            from .embeddings import EmbeddingManager
            embedding_manager = EmbeddingManager()
            embedding = embedding_manager.create_single_embedding(product_description)
            
            # if len(embedding) == 0:
            #     print("Failed to generate embedding")
            #     return False
            
            # Convert numpy array to list and ensure it's the right format
            embedding_list = embedding.tolist()
            # print(f"Generated embedding length: {len(embedding_list)}")
            
            # Update campaign with the new embedding
            result = self.supabase.table('campaigns').update({
                'embedding': embedding_list
            }).eq('id', campaign_id).execute()
            
            # if result.data:
            #     print(f"✓ Successfully stored embedding for campaign {campaign_id}")
            #     return True
            # else:
            #     print(f"✗ Failed to store embedding for campaign {campaign_id}")
            #     print(f"Update result: {result}")
            #     return False
            
        except Exception as e:
            print(f"Error storing campaign embedding: {e}")
            print(f"Error type: {type(e)}")
            return False

    def check_missing_embeddings(self):
        """Check and update any campaigns missing embeddings"""
        try:
            # Get campaigns without embeddings
            response = self.supabase.table('campaigns').select(
                'id, product_description'
            ).is_('embedding', 'null').execute()
            
            if not response.data:
                return
            
            # Create embeddings for each missing one
            for campaign in response.data:
                if campaign.get('product_description'):
                    self.store_campaign_embedding(
                        campaign['id'],
                        campaign['product_description']
                    )
                
        except Exception as e:
            print(f"Error checking missing embeddings: {e}")

    def process_embedding_queue(self):
        """Process pending items in the embedding queue"""
        try:
            # print("Processing embedding queue...")
            
            # Get pending queue items
            response = self.supabase.table('embedding_queue').select(
                'id, campaign_id'
            ).eq('status', 'pending').execute()
            
            # if not response.data:
            #     print("No pending items in embedding queue")
            #     return
            
            # print(f"\nFound {len(response.data)} pending items")
            
            # Process each queue item
            from .embeddings import EmbeddingManager
            embedding_manager = EmbeddingManager()
            
            success_count = 0
            for item in response.data:
                try:
                    # Get campaign details
                    campaign = self.supabase.table('campaigns').select(
                        'id, product_description'
                    ).eq('id', item['campaign_id']).single().execute()
                    
                    if campaign.data and campaign.data.get('product_description'):
                        # Create embedding
                        embedding = embedding_manager.create_single_embedding(
                            campaign.data['product_description']
                        )
                        
                        if len(embedding) > 0:
                            # Update campaign with new embedding
                            result = self.supabase.table('campaigns').update({
                                'embedding': embedding.tolist()
                            }).eq('id', campaign.data['id']).execute()
                            
                            if result.data:
                                # Mark queue item as completed
                                self.supabase.table('embedding_queue').update({
                                    'status': 'completed',
                                    'updated_at': datetime.utcnow().isoformat()
                                }).eq('id', item['id']).execute()
                                
                                success_count += 1
                                # print(f"✓ Updated embedding for campaign {campaign.data['id']}")
                            # else:
                                # print(f"✗ Failed to store embedding for campaign {campaign.data['id']}")
                
                except Exception as e:
                    print(f"Error processing queue item {item['id']}: {e}")
                    continue
                
            # print(f"\nCompleted queue processing. Success: {success_count}/{len(response.data)}")
            
        except Exception as e:
            print(f"Error processing queue: {e}")
            print(f"Error type: {type(e)}")
            print(f"Error details: {str(e)}")

    def get_campaign_bids(self, campaign_ids: List[str]) -> pd.DataFrame:
        """Get bids for specific campaigns using service role to bypass RLS"""
        try:
            if not campaign_ids:
                return pd.DataFrame()
            
            # print(f"\nFetching bids for campaigns: {campaign_ids}")
            
            # Get bids from database
            response = self.supabase.table('campaign_bids') \
                .select('campaign_id, bid_amount') \
                .in_('campaign_id', campaign_ids) \
                .execute()
            
            # print(f"Found bids: {response.data}")
            
            # Return bids as DataFrame, or empty DataFrame if none found
            df = pd.DataFrame(response.data)
            if not df.empty:
                df.set_index('campaign_id', inplace=True)
            
            return df
            
        except Exception as e:
            # print(f"Error getting campaign bids: {e}")
            return pd.DataFrame()

    # def force_update_all_embeddings(self):
    #     """Force update embeddings for all campaigns with product descriptions but null embeddings"""
    #     try:
    #         print("Starting force update of embeddings...")
            
    #         # Get campaigns that have product descriptions but null embeddings
    #         response = self.supabase.table('campaigns').select(
    #             'id, product_description, embedding'
    #         ).not_.is_('product_description', 'null').is_('embedding', 'null').execute()
            
    #         if not response.data:
    #             print("No campaigns found needing embedding updates")
    #             return
            
    #         print(f"\nFound {len(response.data)} campaigns needing embeddings")
            
    #         # Process each campaign
    #         from .embeddings import EmbeddingManager
    #         embedding_manager = EmbeddingManager()
            
    #         success_count = 0
    #         for campaign in response.data:
    #             try:
    #                 # Create embedding for the product description
    #                 embedding = embedding_manager.create_single_embedding(campaign['product_description'])
                    
    #                 if len(embedding) > 0:
    #                     # Update campaign with the new embedding
    #                     result = self.supabase.table('campaigns').update({
    #                         'embedding': embedding.tolist()
    #                     }).eq('id', campaign['id']).execute()
                        
    #                     if result.data:
    #                         success_count += 1
    #                         print(f"✓ Updated embedding for campaign {campaign['id']}")
    #                     else:
    #                         print(f"✗ Failed to store embedding for campaign {campaign['id']}")
                
    #             except Exception as e:
    #                 print(f"Error processing campaign {campaign['id']}: {e}")
    #                 continue
                
    #         print(f"\nCompleted embedding updates. Success: {success_count}/{len(response.data)}")
            
    #     except Exception as e:
    #         print(f"Error in force update: {e}")
    #         print(f"Error type: {type(e)}")
    #         print(f"Error details: {str(e)}")

    # def check_campaign_data(self):
    #     """Debug helper to check campaign data"""
    #     try:
    #         print("\nChecking campaign data...")
            
    #         # Check all campaigns
    #         response = self.supabase.table('campaigns').select(
    #             'id, product_name, product_description, embedding'
    #         ).execute()
            
    #         total = len(response.data)
    #         with_desc = len([c for c in response.data if c.get('product_description')])
    #         with_embed = len([c for c in response.data if c.get('embedding')])
            
    #         print(f"Total campaigns: {total}")
    #         print(f"With descriptions: {with_desc}")
    #         print(f"With embeddings: {with_embed}")
            
    #         # Show sample of campaigns with descriptions
    #         if with_desc > 0:
    #             print("\nSample campaigns with descriptions:")
    #             for campaign in response.data:
    #                 if campaign.get('product_description'):
    #                     print(f"ID: {campaign['id']}")
    #                     print(f"Name: {campaign['product_name']}")
    #                     print(f"Description: {campaign['product_description'][:100]}...")
    #                     print(f"Has embedding: {bool(campaign.get('embedding'))}\n")
                    
    #     except Exception as e:
    #         print(f"Error checking campaign data: {e}")    def update_campaign_embedding(self, campaign_id: str, embedding: List[float]) -> bool:
           # Previous method...
    
    def update_campaign_embedding(self, campaign_id: str, embedding: List[float]) -> bool:
        """Update the embedding for a specific campaign"""
        try:
            if not campaign_id or not embedding:
                return False
                
            response = self.supabase.table('campaigns').update({
                'embedding': embedding
            }).eq('id', campaign_id).execute()
            
            return bool(response.data)
            
        except Exception as e:
            print(f"Error updating campaign embedding: {e}")
            return False
