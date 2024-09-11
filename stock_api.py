import requests
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_stock_info(stock_code):
    logger.info(f"Fetching stock info for {stock_code}")
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
        logger.debug(f"Sending request to {base_url + symbol}")
        response = requests.get(base_url + symbol, params=params, headers=headers)
        
        logger.info(f"Request URL: {response.url}")
        logger.info(f"Status Code: {response.status_code}")
        
        response.raise_for_status()
        
        data = response.json()
        logger.debug(f"Received data: {data}")
        
        if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
            stock_data = data['chart']['result'][0]
            meta = stock_data.get('meta', {})
            quote = stock_data.get('indicators', {}).get('quote', [{}])[0]
            
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
                f"Change: {change} ({change_percent:.2f}% if isinstance(change_percent, float) else 'N/A'})\n"
                f"Open: {quote.get('open', ['N/A'])[-1] if quote.get('open') else 'N/A'}\n"
                f"High: {quote.get('high', ['N/A'])[-1] if quote.get('high') else 'N/A'}\n"
                f"Low: {quote.get('low', ['N/A'])[-1] if quote.get('low') else 'N/A'}\n"
                f"Volume: {quote.get('volume', ['N/A'])[-1] if quote.get('volume') else 'N/A'}\n"
                f"Previous Close: {previous_close}"
            )
            logger.info(f"Successfully retrieved stock info for {stock_code}")
            return stock_info
        else:
            logger.warning(f"Unexpected data format for {stock_code}")
            return f"Unable to retrieve information for stock code {stock_code}. Unexpected data format."

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error occurred: {str(e)}", exc_info=True)
        return f"Network error occurred while fetching stock information: {str(e)}"
    except json.JSONDecodeError as json_error:
        logger.error(f"JSON decode error: {str(json_error)}", exc_info=True)
        return f"Error decoding API response: {str(json_error)}"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return f"An unexpected error occurred: {type(e).__name__}, {str(e)}"