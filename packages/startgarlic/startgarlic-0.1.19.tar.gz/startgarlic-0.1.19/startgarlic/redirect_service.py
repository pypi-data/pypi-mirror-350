from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from startgarlic.utils.database import DatabaseManager
from datetime import datetime
from urllib.parse import unquote

app = FastAPI()
db = DatabaseManager()

@app.get("/redirect")
async def redirect(request: Request):
    try:
        params = dict(request.query_params)
        print(f"Received params: {params}")  # Debug log
        
        destination_url = params.pop('url', None)
        company_id = params.pop('cid', None)
        
        print(f"Destination URL: {destination_url}")  # Debug log
        print(f"Company ID: {company_id}")  # Debug log
        
        if destination_url and company_id:
            # Decode the URL if it's encoded
            destination_url = unquote(destination_url)
            
            # Get current clicks and company name
            response = db.supabase.table('ads') \
                .select('clicks, name') \
                .eq('id', company_id) \
                .execute()
            
            print(f"Database response: {response.data}")  # Debug log
            
            if response.data:
                current_clicks = response.data[0].get('clicks', 0) or 0
                company_name = response.data[0].get('name', '')
                
                print(f"Current clicks: {current_clicks}")  # Debug log
                print(f"Company name: {company_name}")  # Debug log
                
                # Update clicks count
                update_response = db.supabase.table('ads') \
                    .update({'clicks': current_clicks + 1}) \
                    .eq('id', company_id) \
                    .execute()
                    
                print(f"Update response: {update_response.data}")  # Debug log
                
                # Log the click with company name and additional metadata
                analytics_data = {
                    'company_name': company_name,
                    'interaction_type': 'click',
                    'timestamp': datetime.now().isoformat(),
                    'user_agent': request.headers.get("user-agent"),
                    'referrer': request.headers.get("referer"),
                    'ip_address': request.client.host
                }
                
                analytics_response = db.supabase.table('analytics_logs').insert(analytics_data).execute()
                print(f"Analytics response: {analytics_response.data}")  # Debug log
            
            # Build final URL with just ref=Garlic
            final_url = f"{destination_url}{'?' if '?' not in destination_url else '&'}ref=Garlic"
            print(f"Final URL: {final_url}")  # Debug log
            
            return RedirectResponse(url=final_url, status_code=307)
            
        return RedirectResponse(url=destination_url if destination_url else "/")
        
    except Exception as e:
        print(f"Error in redirect: {e}")
        print(f"Full error details: {str(e)}")  # More detailed error
        return RedirectResponse(url=destination_url if destination_url else "/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 