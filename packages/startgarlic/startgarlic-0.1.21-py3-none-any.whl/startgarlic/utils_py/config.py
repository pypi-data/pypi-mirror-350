import os
from dotenv import load_dotenv
import logging
import pathlib

def get_credentials():
    """Get Supabase credentials from environment variables"""
    # Try multiple potential locations for the .env file, prioritizing secure locations
    env_paths = [
        os.path.join(os.path.expanduser("~"), ".config", "startgarlic", ".env"),  # Secure user config location
        os.path.join(os.getcwd(), '.env'),  # Current directory (fallback)
        os.path.join(os.path.dirname(os.getcwd()), '.env'),  # Parent directory (fallback)
        os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), '.env')  # Project root (fallback)
    ]
    
    env_loaded = False
    for env_path in env_paths:
        if os.path.exists(env_path):
            load_dotenv(env_path)
            logging.info(f"Loaded environment from: {env_path}")
            env_loaded = True
            break
    
    if not env_loaded:
        logging.warning("No .env file found in any of the expected locations")
    
    # Get credentials from environment variables
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    # Check both possible environment variable names
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_KEY")
    
    # Check if credentials are available
    if not url or not key or not service_role_key:
        missing = []
        if not url: missing.append("SUPABASE_URL")
        if not key: missing.append("SUPABASE_KEY")
        if not service_role_key: missing.append("SUPABASE_SERVICE_ROLE_KEY/SUPABASE_SERVICE_KEY")
        logging.warning(f"Missing Supabase credentials in environment variables: {', '.join(missing)}")
    else:
        logging.info("Successfully loaded all Supabase credentials")
    
    # Return credentials
    return {
        "url": url or "",
        "key": key or "",
        "service_role_key": service_role_key or ""
    }