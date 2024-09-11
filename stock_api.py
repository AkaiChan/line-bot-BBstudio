import yfinance as yf
from datetime import datetime

def get_stock_info(stock_code):
    try:
        stock = yf.Ticker(stock_code)
        info = stock.info
        price = info.get('regularMarketPrice', 'N/A')
        change = info.get('regularMarketChange', 'N/A')
        percent_change = info.get('regularMarketChangePercent', 'N/A')
        volume = info.get('regularMarketVolume', 'N/A')
        market_time = datetime.fromtimestamp(info.get('regularMarketTime', 0)).strftime('%Y-%m-%d %H:%M:%S')

        return (
            f"股票代碼：{stock_code}\n"
            f"當前價格：{price}\n"
            f"漲跌：{change:.2f} ({percent_change:.2f}%)\n"
            f"成交量：{volume}\n"
            f"更新時間：{market_time}"
        )
    except Exception as e:
        return f"獲取股票 {stock_code} 信息時發生錯誤：{str(e)}"