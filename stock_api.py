import requests
from datetime import datetime, timedelta
import logging
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
from io import BytesIO
import base64

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TWStockAPI:
    @staticmethod
    def get_stock_info(stock_code):
        logger.debug(f"開始獲取股票 {stock_code} 的信息")
        try:
            # 使用 TWSE 公開資訊觀測站 API
            url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_code}.tw"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            logger.debug(f"API 響應狀態碼: {response.status_code}")
            logger.debug(f"API 響應內容: {response.text[:500]}")  # 輸出前500個字符的響應內容

            data = response.json()
            if "msgArray" not in data or len(data["msgArray"]) == 0:
                return {"error": f"無法獲取股票 {stock_code} 的數據"}

            stock_data = data["msgArray"][0]

            result = {
                "股票代碼": stock_code,
                "股票名稱": stock_data.get("n", "未知"),
                "日期": datetime.now().strftime("%Y-%m-%d"),
                "成交股數": stock_data.get("v", "N/A"),
                "成交金額": stock_data.get("a", "N/A"),
                "開盤價": stock_data.get("o", "N/A"),
                "最高價": stock_data.get("h", "N/A"),
                "最低價": stock_data.get("l", "N/A"),
                "收盤價": stock_data.get("z", "N/A"),
                "漲跌": stock_data.get("d", "N/A"),
                "漲跌幅": stock_data.get("z", "N/A"),
                "昨日收盤價": stock_data.get("y", "N/A")
            }

            logger.debug(f"成功獲取股票 {stock_code} 的信息: {result}")
            return result
        except requests.RequestException as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生網絡錯誤")
            return {"error": f"獲取股票 {stock_code} 信息時發生網絡錯誤：{str(e)}"}
        except Exception as e:
            logger.exception(f"獲取股票 {stock_code} 信息時發生錯誤")
            return {"error": f"獲取股票 {stock_code} 信息時發生錯誤：{str(e)}"}

    @staticmethod
    def create_happy_5_lines_chart(stock_code):
        # 獲取股票數據
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # 獲取一年的數據
        stock = yf.Ticker(f"{stock_code}.TW")
        df = stock.history(start=start_date, end=end_date)

        # 計算均線
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA60'] = df['Close'].rolling(window=60).mean()

        # 設置圖表樣式
        mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
        s = mpf.make_mpf_style(marketcolors=mc)

        # 創建圖表
        fig, axes = mpf.plot(df, type='candle', style=s, volume=True, returnfig=True)

        # 添加均線
        axes[0].plot(df.index, df['MA5'], label='MA5', color='blue')
        axes[0].plot(df.index, df['MA20'], label='MA20', color='orange')
        axes[0].plot(df.index, df['MA60'], label='MA60', color='purple')

        # 添加圖例
        axes[0].legend()

        # 設置標題
        plt.title(f"{stock_code} 樂活五線譜")

        # 將圖表轉換為 base64 編碼的字符串
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()

        return image_base64

# 使用示例
if __name__ == "__main__":
    stock_code = "2330"  # 測試台積電
    stock_info = TWStockAPI.get_stock_info(stock_code)
    print(stock_info)
    image_base64 = TWStockAPI.create_happy_5_lines_chart(stock_code)
    print(f"Base64 encoded image: {image_base64[:50]}...")  # 只打印前50個字符