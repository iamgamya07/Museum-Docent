import requests
import json
import time
import os
import sys

# --- CONFIGURATION ---
# The Met's official API endpoints
SEARCH_ENDPOINT = "https://collectionapi.metmuseum.org/public/collection/v1/search"
OBJECT_DETAIL_ENDPOINT = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
MAX_ARTWORKS_TO_FETCH = 50 # You can increase this number to get more data

def get_artwork_ids():
    """Gets a pre-filtered list of artwork IDs using the search endpoint."""
    print("➡️ Step 1: Searching for highlighted, public domain artworks via the Met API...")
    
    # This query searches for artworks that are highlighted and in the public domain
    params = {
        'q': 'a',  # A general query to get a broad set of results
        'isHighlight': 'true',
        'isPublicDomain': 'true'
    }
    
    try:
        response = requests.get(SEARCH_ENDPOINT, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        object_ids = data.get("objectIDs", [])
        
        if not object_ids:
            print("❌ Error: API search returned no artwork IDs for the query.")
            return []
            
        print(f"✅ Found {len(object_ids)} relevant artworks. Fetching details for the first {MAX_ARTWORKS_TO_FETCH}.")
        # Return a slice of the IDs found
        return object_ids[:MAX_ARTWORKS_TO_FETCH]
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return []

def get_artwork_details(object_id):
    """Fetches and processes details for a single artwork ID."""
    detail_url = f"{OBJECT_DETAIL_ENDPOINT}{object_id}"
    try:
        response = requests.get(detail_url, timeout=15)
        response.raise_for_status()
        data = response.json()

        # We can be confident these conditions will be met because of our search query
        return {
            "title": data.get("title", "No Title"),
            "artist": data.get("artistDisplayName", "Unknown Artist"),
            "date": data.get("objectDate", "Unknown Date"),
            "medium": data.get("medium", "Unknown Medium"),
            # Use a more descriptive field if available, otherwise fallback
            "description": data.get("creditLine", data.get("objectName", "No Description")),
            "url": data.get("objectURL", "")
        }
        
    except requests.exceptions.RequestException:
        return None # Skip if an individual request fails

def main(output_path="data/met_artworks.jsonl"):
    """Main function to run the data fetching process."""
    os.makedirs("data", exist_ok=True)
    
    artwork_ids = get_artwork_ids()
    
    if not artwork_ids:
        print("❌ Critical Error: Could not get any artwork IDs. Aborting.")
        sys.exit(1)
        
    print(f"\n➡️ Step 2: Fetching details for {len(artwork_ids)} artworks...")
    
    artwork_count = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for i, object_id in enumerate(artwork_ids):
            # Simple progress indicator
            print(f"  - ({i+1}/{len(artwork_ids)}) Fetching object ID: {object_id}")
            details = get_artwork_details(object_id)
            
            if details:
                f.write(json.dumps(details, ensure_ascii=False) + "\n")
                artwork_count += 1
            
            time.sleep(0.1) # Brief pause to be respectful to the API server

    if artwork_count > 0:
        print(f"\n✅ Success! Saved data for {artwork_count} artworks to {output_path}")
    else:
        print("\n❌ Warning: Finished without saving any artwork data. There may be a temporary API issue.")

if __name__ == "__main__":
    main()