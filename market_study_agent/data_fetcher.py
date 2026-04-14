import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, Any, List
import time


def fetch_mergr_deals(industry: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch recent deals from Mergr free tier for a given industry.
    Note: This is a basic scraper; respect terms of service and rate limits.
    """
    url = f"https://mergr.com/search?query={industry}&type=deals"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        deals = []
        # Mergr free tier shows deals in a list; adjust selectors based on actual HTML
        deal_items = soup.find_all('div', class_='deal-item')[:max_results]  # Placeholder selector
        for item in deal_items:
            title = item.find('h3').text.strip() if item.find('h3') else "Unknown Deal"
            value = item.find('span', class_='value').text.strip() if item.find('span', class_='value') else "N/A"
            deals.append({"buyer": "Unknown", "target": title, "notes": f"Value: {value}", "source": "Mergr"})
        return deals
    except Exception as e:
        print(f"Error fetching from Mergr: {e}")
        return []


def fetch_crunchbase_news(industry: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch public news from Crunchbase free tier.
    Requires API key; placeholder for demo.
    """
    # Crunchbase free API requires signup: https://data.crunchbase.com/docs
    api_key = "YOUR_API_KEY"  # Replace with actual key
    url = f"https://api.crunchbase.com/api/v4/searches/organizations?query={industry}&user_key={api_key}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        deals = []
        for item in data.get('entities', [])[:max_results]:
            deals.append({
                "buyer": item.get('name', 'Unknown'),
                "target": "N/A",
                "notes": item.get('short_description', ''),
                "source": "Crunchbase"
            })
        return deals
    except Exception as e:
        print(f"Error fetching from Crunchbase: {e}")
        return []


def fetch_bizbuysell_listings(industry: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch listings from BizBuySell (sample data scraper).
    """
    url = f"https://www.bizbuysell.com/{industry}-businesses-for-sale/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = []
        # Placeholder selectors
        items = soup.find_all('div', class_='listing')[:max_results]
        for item in items:
            title = item.find('h2').text.strip() if item.find('h2') else "Unknown Listing"
            price = item.find('span', class_='price').text.strip() if item.find('span', class_='price') else "N/A"
            listings.append({"buyer": "N/A", "target": title, "notes": f"Asking Price: {price}", "source": "BizBuySell"})
        return listings
    except Exception as e:
        print(f"Error fetching from BizBuySell: {e}")
        return []


def aggregate_recent_transactions(industry: str) -> List[Dict[str, Any]]:
    """
    Aggregate recent transactions from multiple sources.
    """
    transactions = []
    transactions.extend(fetch_mergr_deals(industry))
    transactions.extend(fetch_crunchbase_news(industry))
    transactions.extend(fetch_bizbuysell_listings(industry))
    return transactions[:10]  # Limit to 10


if __name__ == "__main__":
    # Test fetch
    deals = aggregate_recent_transactions("hvac")
    print(json.dumps(deals, indent=2))