import requests
import json

def get_stock_info(stock_code):
    base_url = "https://openapi.twse.com.tw/v1"
    endpoint = f"/exchangeReport/STOCK_DAY_AVG"
    params = {"stockNo": stock_code}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(base_url + endpoint, params=params, headers=headers)
        
        print(f"Request URL: {response.url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text[:500]}")  # 只打印前500個字符
        print(f"Response Headers: {response.headers}")
        
        response.raise_for_status()
        
        if response.headers.get('Content-Type', '').startswith('application/json'):
            try:
                stock_data = response.json()
                if stock_data:
                    if isinstance(stock_data, list) and len(stock_data) > 0:
                        latest_data = stock_data[0]
                        stock_info = (
                            f"股票代碼 {stock_code} 的資訊：\n"
                            f"日期：{latest_data.get('date', 'N/A')}\n"
                            f"成交股數：{latest_data.get('volumeOfTransactions', 'N/A')} 股\n"
                            f"成交金額：{latest_data.get('valueOfTransactions', 'N/A')} 元\n"
                            f"開盤價：{latest_data.get('openingPrice', 'N/A')} 元\n"
                            f"最高價：{latest_data.get('highestPrice', 'N/A')} 元\n"
                            f"最低價：{latest_data.get('lowestPrice', 'N/A')} 元\n"
                            f"收盤價：{latest_data.get('closingPrice', 'N/A')} 元\n"
                            f"漲跌：{latest_data.get('change', 'N/A')} 元\n"
                            f"成交筆數：{latest_data.get('numberOfTransactions', 'N/A')} 筆"
                        )
                        return stock_info
                    else:
                        return f"API 返回的數據格式不符合預期。返回數據：{stock_data}"
                else:
                    return f"無法獲取股票代碼 {stock_code} 的資訊。API 返回空數據。"
            except json.JSONDecodeError as json_error:
                return f"API 返回的數據不是有效的 JSON 格式。錯誤：{str(json_error)}。原始回應：{response.text[:200]}"
        else:
            return f"API 未返回 JSON 數據。Content-Type: {response.headers.get('Content-Type')}。原始回應：{response.text[:200]}"

    except requests.exceptions.RequestException as e:
        return f"獲取股票資訊時發生網絡錯誤：{str(e)}"
