import requests
from bs4 import BeautifulSoup

def scrape_website():
    url = "https://www.sparkl.me/learn/ib/biology-hl/biogeochemical-cycles-carbon-nitrogen-and-water-cycles/revision-notes/1274"  # Replace with the target website
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract only the relevant parts (body content)
        main_content = soup.body
        
        return str(main_content)  # Convert HTML to string for frontend rendering
    
    except requests.exceptions.RequestException as e:
        return f"<p>Error fetching content: {e}</p>"
