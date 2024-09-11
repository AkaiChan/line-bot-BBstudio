import requests
from datetime import datetime

def get_stock_info(stock_code):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_code}.TW"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查 HTTP 錯誤
        data = response.json()

        result = data['chart']['result'][0]
        quote = result['indicators']['quote'][0]
        meta = result['meta']

        current_price = meta['regularMarketPrice']
        previous_close = meta['previousClose']
        change = current_price - previous_close
        percent_change = (change / previous_close) * 100

        return (
            f"股票代碼：{stock_code}\n"
            f"日期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"當前價格：{current_price:.2f} 元\n"
            f"漲跌：{change:.2f} 元 ({percent_change:.2f}%)\n"
            f"開盤價：{quote['open'][-1]:.2f} 元\n"
            f"最高價：{quote['high'][-1]:.2f} 元\n"
            f"最低價：{quote['low'][-1]:.2f} 元\n"
            f"成交量：{quote['volume'][-1]} 股\n"
            f"前一日收盤價：{previous_close:.2f} 元"
        )
    except requests.RequestException as e:
        return f"獲取股票 {stock_code} 信息時發生網絡錯誤：{str(e)}"
    except ValueError as e:
        return f"解析股票 {stock_code} 數據時發生錯誤：{str(e)}"
    except KeyError as e:
        return f"股票 {stock_code} 數據格式不正確：{str(e)}"
    except Exception as e:
        return f"獲取股票 {stock_code} 信息時發生未知錯誤：{str(e)}"

# 使用示例
# info = get_stock_info("0050")
# print(info)