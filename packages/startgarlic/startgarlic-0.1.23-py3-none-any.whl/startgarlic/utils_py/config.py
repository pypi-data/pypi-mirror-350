import os
from dotenv import load_dotenv
import logging
import pathlib
from .secure_credentials import get_default_credentials, obfuscate_key

def get_credentials():
    """Get Supabase credentials from environment variables or default secure credentials"""
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
        logging.info("No .env file found, using bundled credentials")
    
    # Get credentials from environment variables
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    # Check both possible environment variable names
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_KEY")
    
    # If any credentials are missing, use the default ones
    default_creds = get_default_credentials()
    if not url:
        url = default_creds["SUPABASE_URL"]
        logging.info("Using bundled SUPABASE_URL")
    
    if not key:
        key = default_creds["SUPABASE_KEY"]
        logging.info("Using bundled SUPABASE_KEY")
    
    if not service_role_key:
        service_role_key = default_creds["SUPABASE_SERVICE_ROLE_KEY"]
        logging.info("Using bundled SUPABASE_SERVICE_ROLE_KEY")
    
    # Log the credentials being used (obfuscated for security)
    logging.info(f"Using Supabase URL: {url}")
    logging.info(f"Using Supabase Key: {obfuscate_key(key)}")
    logging.info(f"Using Supabase Service Role Key: {obfuscate_key(service_role_key)}")
    
    # Return credentials
    return {
        "url": url,
        "key": key,
        "service_role_key": service_role_key
    }