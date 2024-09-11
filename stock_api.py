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
        response.raise_for_status()
        data = response.json()
        
        if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
            stock_data = data['chart']['result'][0]
            meta = stock_data['meta']
            quote = stock_data.get('indicators', {}).get('quote', [{}])[0]
            
            # 使用 get 方法來安全地獲取數據，如果數據不存在則使用 'N/A'
            current_price = meta.get('regularMarketPrice', 'N/A')
            previous_close = meta.get('previousClose', meta.get('chartPreviousClose', 'N/A'))
            
            stock_info = f"股票代碼 {stock_code} 的資訊：\n"
            stock_info += f"日期：{datetime.fromtimestamp(meta.get('regularMarketTime', 0)).strftime('%Y-%m-%d %H:%M:%S')}\n"
            stock_info += f"當前價格：{current_price} 元\n"
            
            if previous_close != 'N/A' and current_price != 'N/A':
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
                stock_info += f"漲跌：{change:.2f} 元 ({change_percent:.2f}%)\n"
            
            stock_info += f"開盤價：{quote.get('open', ['N/A'])[-1]} 元\n"
            stock_info += f"最高價：{quote.get('high', ['N/A'])[-1]} 元\n"
            stock_info += f"最低價：{quote.get('low', ['N/A'])[-1]} 元\n"
            stock_info += f"成交量：{quote.get('volume', ['N/A'])[-1]} 股\n"
            stock_info += f"前一日收盤價：{previous_close} 元"
            
            return stock_info
        else:
            return f"無法獲取股票代碼 {stock_code} 的資訊。API 返回的數據格式不符合預期。"

    except requests.exceptions.RequestException as e:
        return f"獲取股票資訊時發生網絡錯誤：{str(e)}"
    except json.JSONDecodeError as json_error:
        return f"API 返回的數據不是有效的 JSON 格式。錯誤：{str(json_error)}。"
    except Exception as e:
        return f"獲取股票資訊時發生未知錯誤：{str(e)}\n錯誤類型：{type(e).__name__}"

# 用於測試
if __name__ == "__main__":
    print(get_stock_info("2330"))  # 測試台積電的股票代碼
