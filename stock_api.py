import requests
import json
from datetime import datetime

def get_stock_info(stock_code):
    symbol = f"{stock_code}.TW"
    base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
    
    params = {
        "region": "TW",
        "lang": "en-US",
        "includePrePost": "false",
        "interval": "1d",
        "range": "1d",
        "corsDomain": "finance.yahoo.com",
        ".tsrc": "finance"
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(base_url + symbol, params=params, headers=headers)
        
        print(f"Request URL: {response.url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        response.raise_for_status()
        
        data = response.json()
        
        if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
            stock_data = data['chart']['result'][0]
            meta = stock_data['meta']
            quote = stock_data['indicators']['quote'][0]
            
            current_price = meta.get('regularMarketPrice', 'N/A')
            previous_close = meta.get('previousClose', meta.get('chartPreviousClose', 'N/A'))
            
            if current_price != 'N/A' and previous_close != 'N/A':
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100
            else:
                change = 'N/A'
                change_percent = 'N/A'
            
            stock_info = (
                f"Stock Code {stock_code} Information:\n"
                f"Date: {datetime.fromtimestamp(meta.get('regularMarketTime', 0)).strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Current Price: {current_price}\n"
                f"Change: {change} ({change_percent:.2f}%)\n"
                f"Open: {quote.get('open', ['N/A'])[-1]}\n"
                f"High: {quote.get('high', ['N/A'])[-1]}\n"
                f"Low: {quote.get('low', ['N/A'])[-1]}\n"
                f"Volume: {quote.get('volume', ['N/A'])[-1]}\n"
                f"Previous Close: {previous_close}"
            )
            return stock_info
        else:
            print(f"Unexpected data format. Received data: {data}")
            return f"Unable to retrieve information for stock code {stock_code}. Unexpected data format."

    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {str(e)}")
        return f"Network error occurred while fetching stock information: {str(e)}"
    except json.JSONDecodeError as json_error:
        print(f"JSON decode error: {str(json_error)}")
        return f"Error decoding API response: {str(json_error)}"
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"

# 用於測試
if __name__ == "__main__":
    print(get_stock_info("2330"))  # 測試台積電的股票代碼
