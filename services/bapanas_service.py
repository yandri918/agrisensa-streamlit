
import requests
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Robust import strategy for Streamlit + Script usage
try:
    from agrisensa_streamlit.utils.bapanas_constants import API_CONFIG, COMMODITY_MAPPING
except ImportError:
    try:
        # Try relative import (if run as package)
        from ..utils.bapanas_constants import API_CONFIG, COMMODITY_MAPPING
    except ImportError:
        # Final fallback: add parent dir to path (if run as script)
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from utils.bapanas_constants import API_CONFIG, COMMODITY_MAPPING

class BapanasService:
    def __init__(self):
        self.base_url = API_CONFIG["BASE_URL"]
        self.headers = API_CONFIG["HEADERS"]
    
    def get_latest_prices(self, province_id=None, city_id=None):
        """
        Fetch latest prices from Bapanas API
        """
        endpoint = f"{self.base_url}/harga-pangan-informasi"
        
        params = {
            "level_harga_id": 1  # 1 for consumer/retail prices
        }
        
        if province_id and str(province_id) != "0":
            params["province_id"] = province_id
        
        if city_id:
            params["city_id"] = city_id
            
        try:
            response = requests.get(
                endpoint, 
                headers=self.headers, 
                params=params, 
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    return self._parse_price_response(result.get("data", []))
                else:
                    return None
            else:
                return None
                
        except Exception as e:
            print(f"Connection Error: {e}")
            return None
    
    def _parse_price_response(self, data_list):
        """
        Parse success response from API
        Returns DataFrame with standard columns
        """
        if not data_list:
            return None
            
        parsed_data = []
        today_date = datetime.now()
        yesterday_date = today_date - timedelta(days=1)
        
        for item in data_list:
            try:
                # Add Today's Price
                parsed_data.append({
                    'commodity': item.get('name'),
                    'price': float(item.get('today', 0)),
                    'date': today_date,
                    'unit': item.get('satuan', 'Rp/kg')
                })
                
                # Add Yesterday's Price (for trend)
                if item.get('yesterday'):
                    parse_yesterday = item.get('yesterday_date')
                    date_obj = yesterday_date
                    
                    if parse_yesterday:
                        try:
                            date_obj = datetime.strptime(parse_yesterday, '%d-%m-%Y')
                        except:
                            pass
                            
                    parsed_data.append({
                        'commodity': item.get('name'),
                        'price': float(item.get('yesterday', 0)),
                        'date': date_obj,
                        'unit': item.get('satuan', 'Rp/kg')
                    })
            except:
                continue
                
        return pd.DataFrame(parsed_data)

    def get_commodity_list(self):
        return list(COMMODITY_MAPPING.keys())
