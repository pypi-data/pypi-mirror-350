import argparse
import uvicorn
import os
from .main import app, setup_cors

def main():
    """Start the API server"""
    parser = argparse.ArgumentParser(description='Start the Garlic API server')
    parser.add_argument('--host', type=str, default="0.0.0.0", help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8001, help='Port to run the server on')
    parser.add_argument('--cors-origins', type=str, help='Comma-separated list of allowed origins for CORS')
    args = parser.parse_args()
    
    # Set up CORS from environment variables or command line args
    # Default now includes both localhost and production domains
    default_origins = 'http://localhost:3000,https://startgarlic.com,https://api.startgarlic.com'
    cors_origins = args.cors_origins or os.environ.get('GARLIC_CORS_ORIGINS', default_origins)
    origins = [origin.strip() for origin in cors_origins.split(',')]
    setup_cors(app, origins)
    
    # Get port from environment variable (for Render) or use default
    port = int(os.environ.get('PORT', args.port))
    
    print(f"Starting Garlic API server on {args.host}:{port}...")
    print(f"CORS enabled for: {origins}")
    uvicorn.run(app, host=args.host, port=port)

if __name__ == "__main__":
    main()