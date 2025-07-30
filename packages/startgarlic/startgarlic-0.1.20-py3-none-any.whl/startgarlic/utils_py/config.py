import os
from dotenv import load_dotenv
import logging

def get_credentials():
    """Get Supabase credentials from environment variables"""
    # Load environment variables from .env file
    load_dotenv()
    
    # Get credentials from environment variables
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    # Check if credentials are available
    if not url or not key or not service_role_key:
        logging.warning("Missing Supabase credentials in environment variables")
    
    # Return credentials
    return {
        "url": url or "",
        "key": key or "",
        "service_role_key": service_role_key or ""
    }