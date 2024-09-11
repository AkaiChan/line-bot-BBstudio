import requests
import json
from datetime import datetime

def get_stock_info(stock_code):
    # 為台灣股票添加 .TW 後綴
    symbol = f"{stock_code}.TW"
    base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
    
    params = {
        "region": "TW",
        "lang": "zh-TW",
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
            
            current_price = meta['regularMarketPrice']
            previous_close = meta['previousClose']
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100
            
            stock_info = (
                f"股票代碼 {stock_code} 的資訊：\n"
                f"日期：{datetime.fromtimestamp(meta['regularMarketTime']).strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"當前價格：{current_price:.2f} 元\n"
                f"開盤價：{quote['open'][-1]:.2f} 元\n"
                f"最高價：{quote['high'][-1]:.2f} 元\n"
                f"最低價：{quote['low'][-1]:.2f} 元\n"
                f"成交量：{quote['volume'][-1]:,} 股\n"
                f"漲跌：{change:.2f} 元 ({change_percent:.2f}%)\n"
                f"前一日收盤價：{previous_close:.2f} 元"
            )
            return stock_info
        else:
            return f"無法獲取股票代碼 {stock_code} 的資訊。API 返回的數據格式不符合預期。"

    except requests.exceptions.RequestException as e:
        return f"獲取股票資訊時發生網絡錯誤：{str(e)}"
    except json.JSONDecodeError as json_error:
        return f"API 返回的數據不是有效的 JSON 格式。錯誤：{str(json_error)}。"
    except KeyError as key_error:
        return f"API 返回的數據缺少必要的欄位。錯誤：{str(key_error)}。"
    except Exception as e:
        return f"獲取股票資訊時發生未知錯誤：{str(e)}"
