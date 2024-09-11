import requests
from datetime import datetime, timedelta
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 簡單的緩存
cache = {}
CACHE_DURATION = timedelta(minutes=5)

def get_stock_info(stock_code):
    # 檢查緩存
    if stock_code in cache and datetime.now() - cache[stock_code]['time'] < CACHE_DURATION:
        logger.debug(f"從緩存返回股票 {stock_code} 的信息")
        return cache[stock_code]['data']

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_code}.TW"
    
    try:
        logger.debug(f"正在請求 URL: {url}")
        response = requests.get(url)
        
        if response.status_code == 429:
            logger.warning("遇到請求限制，等待 5 秒後重試")
            time.sleep(5)
            response = requests.get(url)
        
        response.raise_for_status()
        data = response.json()
        logger.debug(f"API 響應: {data}")

        if 'chart' not in data or 'result' not in data['chart'] or len(data['chart']['result']) == 0:
            return f"無法獲取股票 {stock_code} 的數據"

        result = data['chart']['result'][0]
        quote = result['indicators']['quote'][0]
        meta = result['meta']

        current_price = meta.get('regularMarketPrice')
        previous_close = meta.get('previousClose')

        if current_price is None or previous_close is None:
            return f"股票 {stock_code} 的價格數據不完整"

        change = current_price - previous_close
        percent_change = (change / previous_close) * 100

        info = (
            f"股票代碼：{stock_code}\n"
            f"日期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"當前價格：{current_price:.2f} 元\n"
            f"漲跌：{change:.2f} 元 ({percent_change:.2f}%)\n"
            f"開盤價：{quote.get('open', [])[-1]:.2f} 元\n"
            f"最高價：{quote.get('high', [])[-1]:.2f} 元\n"
            f"最低價：{quote.get('low', [])[-1]:.2f} 元\n"
            f"成交量：{quote.get('volume', [])[-1]} 股\n"
            f"前一日收盤價：{previous_close:.2f} 元"
        )

        # 更新緩存
        cache[stock_code] = {'time': datetime.now(), 'data': info}
        return info

    except requests.RequestException as e:
        logger.exception(f"獲取股票 {stock_code} 信息時發生網絡錯誤")
        return f"獲取股票 {stock_code} 信息時發生網絡錯誤：{str(e)}"
    except Exception as e:
        logger.exception(f"獲取股票 {stock_code} 信息時發生錯誤")
        return f"獲取股票 {stock_code} 信息時發生錯誤：{str(e)}"

# 使用示例
# info = get_stock_info("0050")
# print(info)