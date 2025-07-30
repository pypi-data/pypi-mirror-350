# Move the FastAPI code here
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
from startgarlic.core import Garlic
from startgarlic.utils_py.database import DatabaseManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_cors(app, origins=None):
    """Set up CORS for the application with the given origins"""
    if origins is None:
        origins = ["http://localhost:3000"]
        
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

# Initialize app
app = FastAPI(title="Garlic API", version="0.1.14")

# We'll let server.py call setup_cors with the appropriate origins

class QueryRequest(BaseModel):
    query: str
    chat_history: Optional[List[dict]] = None
    format: Optional[str] = "structured"
    include_ad: Optional[bool] = True
    ad_url: Optional[str] = None
    ad_campaign_id: Optional[str] = None

# Add this new request model for the match endpoint
class MatchRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    context: Optional[Dict] = None

# Add this response model for advertisements
class AdvertResponse(BaseModel):
    company: str
    product_name: str
    product_url: str
    tracking_url: str

class ApiResponse(BaseModel):
    response: str

async def verify_api_key(api_key: str = Header(None, alias="Authorization")):
    logger.info("Verifying API key...")
    
    if not api_key:
        logger.warning("No API key provided")
        raise HTTPException(status_code=401, detail="API key is required")
    
    try:
        # Remove Bearer prefix if present
        if api_key.startswith("Bearer "):
            api_key = api_key.replace("Bearer ", "")
        
        # For development/testing - accept the hardcoded key from your React app
        test_key = "$2a$06$D2xODJoM9vnBoIpI5mcf8.YtgHmiFqepvtHntN.G51ghWy.rNjcaC"
        if api_key == test_key:
            logger.info("Using test API key")
            return "test-user-id"
            
        # Regular verification for production
        logger.info("Verifying with database...")
        db = DatabaseManager()
        is_valid, key_id = db.verify_api_key(api_key)
        if not is_valid:
            logger.warning(f"Invalid API key: {api_key[:5]}...")
            raise HTTPException(status_code=401, detail="Invalid API key")
        return key_id
    except Exception as e:
        logger.error(f"Error verifying API key: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate", response_model=ApiResponse)
async def generate_response(request: QueryRequest, key_id: str = Depends(verify_api_key)):
    try:
        garlic = Garlic(key_id)
        # Pass the request parameters to generate_response
        # The backend will ignore parameters it doesn't use
        response = garlic.generate_response(request.query, request.chat_history)
        return ApiResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add this new endpoint for advertisement matching
# In the match_advertisement function
# Fix the match endpoint to use POST method correctly
# Fix the match endpoint implementation
@app.post("/api/match", response_model=AdvertResponse)
async def match_advertisement(request: MatchRequest, key_id: str = Depends(verify_api_key)):
    try:
        logger.info(f"Processing match request with query: {request.query}")
        
        # Create Garlic instance with the verified API key
        garlic = Garlic(key_id)
        
        # Use the Garlic instance to find an advertisement
        try:
            # Call the find_advertisement method with the query and user_id
            ad_data = garlic.find_advertisement(
                query=request.query,
                user_id=request.user_id,
                context=request.context
            )
            logger.info(f"Found advertisement: {ad_data}")
        except Exception as e:
            logger.error(f"Error finding advertisement: {str(e)}")
            # Fallback to mock data if there's an error
            ad_data = {
                "company": "Example Company",
                "product_name": "AI Assistant Pro",
                "product_url": "https://example.com/products/ai-assistant",
                "tracking_url": "https://example.com/track/ai-assistant?ref=chat"
            }
        
        return AdvertResponse(
            company=ad_data.get("company", ""),
            product_name=ad_data.get("product_name", ""),
            product_url=ad_data.get("product_url", ""),
            tracking_url=ad_data.get("tracking_url", "")
        )
    except Exception as e:
        logger.error(f"Error in match_advertisement: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}