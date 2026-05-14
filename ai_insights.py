from langchain_ollama.llms import OllamaLLM

model = OllamaLLM(model="llama3.2")

def analyze_business(name, reviews_text):
    """Analyze business using LLM - Works with business details on free tier"""
    
    print(f"\n🔍 Analyzing: {name}")
    print(f"   📝 Data length: {len(reviews_text) if reviews_text else 0} chars")
    
    if not reviews_text or not reviews_text.strip():
        print(f"   ⚠️  No data available - using fallback")
        return {
            "summary": "Business information unavailable",
            "sentiment": "Unknown",
            "top_remarks": ["Please try again", "Limited info available"],
            "atmosphere": "Check Yelp directly",
            "best_for": "See full listing"
        }
    
    print(f"   📋 Data preview:\n{reviews_text[:200]}...")
    
    prompt = f"""You MUST respond with EXACTLY these 5 lines. Include the labels.

Business info:
{reviews_text[:1000]}

OUTPUT FORMAT (EXACT - copy this format):
SUMMARY: One sentence about the business
SENTIMENT: positive or negative or neutral or mixed
REMARKS: 3 key qualities (comma separated, e.g., highly rated, affordable, good service)
VIBE: atmosphere or style (e.g., casual, elegant, modern)
BESTFOR: type of customer (e.g., families, business meetings, quick lunch)

RESPOND WITH ONLY THOSE 5 LINES. INCLUDE THE LABELS."""
    
    try:
        print(f"   🤖 Calling LLM...")
        response = model.invoke(prompt)
        print(f"   ✅ LLM response received")
        return parse_response(response)
    except Exception as e:
        print(f"   ❌ LLM error: {str(e)}")
        return get_default_response()

def parse_response(text):
    """Parse LLM response - Flexible parsing with debugging"""
    print(f"   📄 Raw LLM response:\n{text}\n")
    
    lines = text.strip().split('\n')
    result = {
        "summary": None,
        "sentiment": None,
        "top_remarks": None,
        "atmosphere": None,
        "best_for": None
    }
    
    matched_count = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("SUMMARY:"):
            val = line.replace("SUMMARY:", "").strip()
            if val:
                result["summary"] = val
                matched_count += 1
                print(f"   ✓ Parsed SUMMARY")
        elif line.startswith("SENTIMENT:"):
            val = line.replace("SENTIMENT:", "").strip().lower()
            result["sentiment"] = "Positive" if "positive" in val else "Negative" if "negative" in val else "Mixed" if "mixed" in val else "Neutral"
            matched_count += 1
            print(f"   ✓ Parsed SENTIMENT: {result['sentiment']}")
        elif line.startswith("REMARKS:"):
            remarks = line.replace("REMARKS:", "").strip()
            if remarks:
                result["top_remarks"] = [r.strip() for r in remarks.split(",")][:3]
                matched_count += 1
                print(f"   ✓ Parsed REMARKS")
        elif line.startswith("VIBE:"):
            val = line.replace("VIBE:", "").strip()
            if val:
                result["atmosphere"] = val
                matched_count += 1
                print(f"   ✓ Parsed VIBE")
        elif line.startswith("BESTFOR:"):
            val = line.replace("BESTFOR:", "").strip()
            if val:
                result["best_for"] = val
                matched_count += 1
                print(f"   ✓ Parsed BESTFOR")
    
    print(f"   📊 Matched {matched_count}/5 fields")
    
    # Use defaults only for missing fields
    defaults = get_default_response()
    for key in result:
        if result[key] is None:
            result[key] = defaults[key]
    
    return result

def get_default_response():
    """Default response template"""
    return {
        "summary": "Popular choice in the area",
        "sentiment": "Positive",
        "top_remarks": ["Highly rated", "Customer favorite", "Recommended"],
        "atmosphere": "Welcoming",
        "best_for": "Everyone"
    }
