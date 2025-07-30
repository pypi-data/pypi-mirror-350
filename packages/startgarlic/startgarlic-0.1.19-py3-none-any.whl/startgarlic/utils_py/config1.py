import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def get_credentials():
    """Get Supabase credentials from environment or config file"""
    # First try environment variables
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    service_role_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    # Always return a dictionary, even if credentials are not found
    return {
        "url": url or "",
        "key": key or "",
        "service_role_key": service_role_key or ""
    }
    
    # # Then try config file
    # try:
    #     config_path = Path(__file__).parent.parent.parent / "config.json"
    #     if config_path.exists():
    #         with open(config_path, 'r') as f:
    #             config = json.load(f)
                
    #         supabase_config = config.get("supabase", {})
            
    #         # Print debug info about the config
    #         print(f"Found config file at {config_path}")
    #         has_service_key = "service_role_key" in supabase_config
    #         print(f"Config has service role key: {has_service_key}")
            
    #         return supabase_config
    #     else:
    #         print(f"Config file not found at {config_path}")
    # except Exception as e:
    #     print(f"Error loading config: {e}")
    
    # # Default to empty values
    # return {"url": "", "key": "", "service_role_key": ""}