from typing import List, Dict
import pandas as pd
from datetime import datetime

class AnalyticsManager:
    def __init__(self, db_manager):
        self.db = db_manager

    def increment_views(self, companies: List[Dict]):
        """
        Track when companies appear in search results
        """
        try:
            # Update views count in database
            for company in companies:
                # Increment view count
                self.db.increment_company_metric(company['name'], 'views')
                
                # Log the view with timestamp
                self.log_interaction({
                    'company_name': company['name'],
                    'interaction_type': 'view',
                    'timestamp': datetime.now().isoformat()
                })
                
        except Exception as e:
            # print(f"Error tracking views: {e}")
            pass

    def increment_access(self, company_name: str):
        """
        Track when users click/access company details
        """
        try:
            # Increment access count
            self.db.increment_company_metric(company_name, 'access')
            
            # Log the access with timestamp
            self.log_interaction({
                'company_name': company_name,
                'interaction_type': 'access',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            # print(f"Error tracking access: {e}")
            pass

    def log_interaction(self, interaction_data: Dict):
        """
        Log detailed interaction data to analytics table
        """
        try:
            self.db.insert_analytics_log(interaction_data)
        except Exception as e:
            # print(f"Error logging interaction: {e}")
            pass

    def get_company_stats(self, company_name: str = None) -> Dict:
        """
        Get analytics for specific company or all companies
        """
        try:
            if company_name:
                return self.db.get_company_analytics(company_name)
            return self.db.get_all_companies_analytics()
        except Exception as e:
            # print(f"Error getting analytics: {e}")
            pass

    def get_trending_companies(self, days: int = 7, limit: int = 5) -> List[Dict]:
        """
        Get trending companies based on recent views/access
        """
        try:
            return self.db.get_trending_companies(days, limit)
        except Exception as e:
            # print(f"Error getting trending companies: {e}")
            pass