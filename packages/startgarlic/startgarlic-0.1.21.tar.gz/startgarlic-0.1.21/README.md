I'll update the README.md to better reflect your project's current state and functionality. Here's an improved version:

```markdown:c:\Users\May\startgarlic\python\README.md
# StartGarlic

A RAG-based contextual advertisement system that provides intelligent ad matching based on natural language queries.

## Installation

```bash
pip install startgarlic
```

## Quick Start

```python
from startgarlic import Garlic

# Initialize the system with your API key
api_key = "your_api_key_here"
garlic = Garlic(api_key)

# Find a relevant advertisement based on a query
ad_data = garlic.find_advertisement("I am interested in quantum computing in finance")
print(ad_data)
```

## Features

- Contextual ad matching using RAG (Retrieval-Augmented Generation)
- Semantic search using sentence transformers
- Real-time bidding and auction system
- User context awareness
- Analytics and performance tracking
- Easy API integration

## API Usage

### Match Endpoint

```python
import requests

response = requests.post(
    "http://localhost:8001/api/match",
    json={
        "query": "I am interested in quantum computing in finance",
        "user_id": "optional_user_id",
        "context": {}
    },
    headers={
        "Authorization": "Bearer your_api_key_here"
    }
)

print(response.json())
```

### Response Format

```json
{
  "company": "Example Company",
  "product_name": "AI Assistant Pro",
  "product_url": "https://example.com/products/ai-assistant",
  "tracking_url": "https://example.com/track/ai-assistant?ref=chat"
}
```

## Requirements

- Python >= 3.7
- FastAPI >= 0.68.0
- pandas >= 1.3.0
- sentence-transformers >= 2.0.0
- numpy >= 1.19.0
- supabase >= 0.0.1

## Authors

- Bogdan Ciolac (bogdan@startgarlic.com)
- May Elshater (may@startgarlic.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

