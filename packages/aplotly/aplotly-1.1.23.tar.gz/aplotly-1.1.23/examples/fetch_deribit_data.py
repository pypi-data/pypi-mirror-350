import requests
import json
from datetime import datetime, timedelta

def fetch_deribit_data(endpoint, params=None):
    """
    Fetch data from Deribit API
    
    Args:
        endpoint (str): API endpoint
        params (dict): Query parameters
    
    Returns:
        dict: API response
    """
    base_url = "https://test.deribit.com/api/v2"
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    # Example: Fetch volatility index data
    endpoint = "/public/get_volatility_index_data"
    
    # Set up parameters for the last 7 days
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)
    
    params = {
        "index_name": "btc_usd",  # Bitcoin volatility index
        "start_timestamp": start_time,
        "end_timestamp": end_time,
        "resolution": 60  # Daily data
    }
    
    data = fetch_deribit_data(endpoint, params)
    
    if data:
        print("Successfully fetched data:")
        print(json.dumps(data, indent=2))
    else:
        print("Failed to fetch data")

if __name__ == "__main__":
    main() 