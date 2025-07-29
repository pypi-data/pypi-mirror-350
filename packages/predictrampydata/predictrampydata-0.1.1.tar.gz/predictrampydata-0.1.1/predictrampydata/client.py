import requests
from typing import Dict, Any, List, Optional

class StockDataClient:
    def __init__(self, base_url: str = "https://stock-data-api-vznr.onrender.com"):
        self.base_url = base_url
        
    def get_stock(self, symbol: str) -> Dict[str, Any]:
        """Get stock data by symbol"""
        response = requests.get(f"{self.base_url}/stocks/{symbol}")
        response.raise_for_status()
        return response.json()
        
    def get_industry(self, industry: str) -> Dict[str, Any]:
        """Get all stocks in a specific industry"""
        response = requests.get(f"{self.base_url}/industries/{industry}")
        response.raise_for_status()
        return response.json()
        
    def search_stocks(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search stocks by symbol or name"""
        params = {"query": query, "limit": limit}
        response = requests.get(f"{self.base_url}/search", params=params)
        response.raise_for_status()
        return response.json()
        
    def list_fields(self) -> Dict[str, Any]:
        """List all available data fields"""
        response = requests.get(f"{self.base_url}/fields")
        response.raise_for_status()
        return response.json()