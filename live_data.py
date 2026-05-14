import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class YelpSearcher:
    """Search restaurants on Yelp using free API"""
    
    def __init__(self):
        self.api_key = os.getenv('YELP_API_KEY')
        self.search_url = "https://api.yelp.com/v3/businesses/search"
        self.business_url = "https://api.yelp.com/v3/businesses"
        self.cache_file = "./yelp_cache.json"
        self.api_calls = 0  # Counter
        self.cache = self.load_cache()
    
    def load_cache(self):
        """Load cached search results"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        """Save cache to file"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def search(self, query, location="New York"):
        """Search restaurants on Yelp"""
        
        # Check cache first
        cache_key = f"{query}:{location}".lower()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        if not self.api_key:
            return {"error": "Yelp API key not found in .env"}
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            params = {
                "term": query,
                "location": location,
                "limit": 5,
                "sort_by": "rating"
            }
            
            response = requests.get(self.search_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            self.api_calls += 1
            print(f"✅ API Call #{self.api_calls} - Search: {query} in {location}")
            
            data = response.json()
            businesses = data.get("businesses", [])
            
            results = []
            for biz in businesses:
                results.append({
                    "id": biz.get("id", ""),
                    "name": biz.get("name", ""),
                    "rating": biz.get("rating", 0),
                    "review_count": biz.get("review_count", 0),
                    "location": biz.get("location", {}).get("address1", ""),
                    "phone": biz.get("phone", ""),
                    "url": biz.get("url", ""),
                    "image_url": biz.get("image_url", "")
                })
            
            # Cache results
            self.cache[cache_key] = results
            self.save_cache()
            
            return results
            
        except requests.exceptions.RequestException as e:
            return {"error": f"API Error: {str(e)}"}
        except Exception as e:
            return {"error": f"Error: {str(e)}"}
    
    def get_reviews(self, business_id):
        """Get business info - Works with free tier using business details endpoint"""
        if not self.api_key:
            return ""
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            # Use business details endpoint (works on free tier)
            url = f"{self.business_url}/{business_id}"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            self.api_calls += 1
            print(f"✅ API Call #{self.api_calls} - Business details for: {business_id}")
            
            data = response.json()
            
            # Build summary from available business data
            name = data.get("name", "Business")
            rating = data.get("rating", 0)
            review_count = data.get("review_count", 0)
            categories = ", ".join([c.get("title", "") for c in data.get("categories", [])])
            
            summary = f"Business: {name}\n"
            summary += f"Rating: ⭐ {rating}/5 ({review_count} reviews)\n"
            summary += f"Category: {categories}\n"
            
            # Add attributes if available
            attributes = data.get("attributes", {})
            if attributes:
                summary += "\nHighlights:\n"
                for key, val in list(attributes.items())[:3]:
                    summary += f"• {key}: {val}\n"
            
            print(f"   📊 Business details retrieved successfully")
            return summary
            
        except Exception as e:
            print(f"   ❌ Error fetching business details: {str(e)}")
            return ""


# Initialize searcher
searcher = YelpSearcher()

def search_businesses(query, location="New York"):
    """Public function to search businesses"""
    return searcher.search(query, location)

def get_business_reviews(business_id):
    """Public function to get reviews for a business"""
    return searcher.get_reviews(business_id)
