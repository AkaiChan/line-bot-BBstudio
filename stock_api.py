import yfinance as yf
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TWStockAPI:
    @staticmethod
    def get_stock_info(stock_code):
        logger.debug(f"開始獲取股票 {stock_code} 的信息")
        try:
            # 對於台灣股票，需要在代碼後面加上.TW
            ticker = yf.Ticker(f"{stock_code}.TW")
            info = ticker.info
            history = ticker.history(period="2d")  # 獲取兩天的數據以計算漲跌

            if history.empty:
                return {"error": f"無法獲取股票 {stock_code} 的數據"}

            latest_data = history.iloc[-1]
            prev_data = history.iloc[-2] if len(history) > 1 else latest_data

            change = latest_data['Close'] - prev_data['Close']
            change_percent = (change / prev_data['Close']) * 100

            result = {
                "股票代碼": stock_code,
                "股票名稱": info.get('longName', '未知'),
                "日期": latest_data.name.strftime("%Y-%m-%d"),
                "成交股數": f"{int(latest_data['Volume']):,}",
                "成交金額": f"{int(latest_data['Volume'] * latest_data['Close']):,}",
                "開盤價": f"{latest_data['Open']:.2f}",
                "最高價": f"{latest_data['High']:.2f}",
                "最低價": f"{latest_data['Low']:.2f}",
                "收盤價": f"{latest_data['Close']:.2f}",
                "漲跌": f"{change:.2f}",
                "漲跌幅": f"{change_percent:.2f}%",
                "昨日收盤價": f"{prev_data['Close']:.2f}"
            }
            logger.debug(f"成功獲取股票 {stock_code} 的信息: {result}")
            return result
        except Exception as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生錯誤")
            return {"error": f"獲取股票 {stock_code} 信息時發生錯誤：{str(e)}"}

# 使用示例
if __name__ == "__main__":
    stock_code = "0050"  # 測試 0050
    stock_info = TWStockAPI.get_stock_info(stock_code)
    print(stock_info)