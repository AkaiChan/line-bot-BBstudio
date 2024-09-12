import os
from venv import logger
import requests
import psycopg2
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from flex_message_library import create_bubble, create_carousel, create_receipt_flex_message, create_shopping_list_flex_message, create_stock_flex_message, create_ticket_flex_message, create_transit_flex_message
from stock_api import TWStockAPI  
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])
OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']  # 請確保設置這個環境變數

# 資料庫連接函數
def get_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=zh_tw"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"{city}的天氣：{weather_description}，溫度：{temperature}°C"
    else:
        return "抱歉，無法獲取天氣資訊。"
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()
    
    if '|' in user_message:
        # 分割訊息並儲存到資料庫
        call, response = user_message.split('|', 1)
        call = call.strip()
        response = response.strip()
        
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO callmemory (call, response) VALUES (%s, %s)", (call, response))
            conn.commit()
            cur.close()
            conn.close()
            reply_text = f"已儲存：\n呼叫: {call}\n回應: {response}"
        except Exception as e:
            print(f"資料庫錯誤: {e}")
            reply_text = "儲存失敗，請稍後再試。"
    else:
        # 查詢資料庫是否有匹配的呼叫
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT response FROM callmemory WHERE call = %s", (user_message,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            
            if result:
                reply_text = result[0]
            else:
                # 如果沒有匹配的呼叫，使用原有的邏輯
                if user_message == "哈囉":
                    reply_text = "你好嗎？"
                elif "天氣" in user_message:
                    city = "台北"  # 預設城市，您可以根據需要修改
                    reply_text = get_weather(city)
                elif user_message == "flexmessage":
                    bubble1 = create_bubble("In Progress", 70, "Buy milk and lettuce before class", {"background": "#27ACB2", "bar": "#0D8186"})
                    bubble2 = create_bubble("Pending", 30, "Wash my car", {"background": "#FF6B6E", "bar": "#DE5658"})
                    bubble3 = create_bubble("In Progress", 100, "Buy milk and lettuce before class", {"background": "#A17DF5", "bar": "#7D51E4"})
                    
                    carousel = create_carousel([bubble1, bubble2, bubble3])
                    
                    flex_message = FlexSendMessage(alt_text="Task Progress", contents=carousel)
                    line_bot_api.reply_message(event.reply_token, flex_message)
                    return
                elif user_message == "ticket":
                    ticket_flex = create_ticket_flex_message(
                        title="BROWN'S ADVENTURE\nIN MOVIE",
                        rating="4.0",
                        date="Monday 25, 9:00PM",
                        place="7 Floor, No.3",
                        seats="C Row, 18 Seat",
                        image_url="https://developers-resource.landpress.line.me/fx/img/01_3_movie.png",
                        qr_code_url="https://developers-resource.landpress.line.me/fx/img/linecorp_code_withborder.png"
                    )
                    flex_message = FlexSendMessage(alt_text="Movie Ticket", contents=ticket_flex)
                    line_bot_api.reply_message(event.reply_token, flex_message)
                    return
                elif user_message == "shopping":
                    items = [
                        {
                            "name": "Arm Chair, White",
                            "price": 49.99,
                            "image_url": "https://developers-resource.landpress.line.me/fx/img/01_5_carousel.png"
                        },
                        {
                            "name": "Metal Desk Lamp",
                            "price": 11.99,
                            "image_url": "https://developers-resource.landpress.line.me/fx/img/01_6_carousel.png",
                            "out_of_stock": True
                        }
                    ]
                    shopping_flex = create_shopping_list_flex_message(items)
                    flex_message = FlexSendMessage(alt_text="Shopping List", contents=shopping_flex)
                    line_bot_api.reply_message(event.reply_token, flex_message)
                    return
                elif user_message == "transit":
                    route = [
                        {"time": "20:30", "station": "Akihabara", "color": "#EF454D", "transit": "Walk 4min"},
                        {"time": "20:34", "station": "Ochanomizu", "color": "#6486E3", "transit": "Metro 1hr"},
                        {"time": "20:40", "station": "Shinjuku", "color": "#6486E3", "transit": ""}
                    ]
                    transit_flex = create_transit_flex_message(
                        from_station="Akihabara",
                        to_station="Shinjuku",
                        total_time="1 hour",
                        route=route
                    )
                    flex_message = FlexSendMessage(alt_text="Transit Route", contents=transit_flex)
                    line_bot_api.reply_message(event.reply_token, flex_message)
                    return
                elif user_message == "receipt":
                    items = [
                        {"name": "Energy Drink", "price": 2.99},
                        {"name": "Chewing Gum", "price": 0.99},
                        {"name": "Bottled Water", "price": 3.33}
                    ]
                    total = sum(item["price"] for item in items)
                    cash = 8.0
                    change = cash - total

                    receipt_flex = create_receipt_flex_message(
                        store_name="Brown Store",
                        address="Flex Tower, 7-7-4 Midori-ku, Tokyo",
                        items=items,
                        total=total,
                        cash=cash,
                        change=change,
                        payment_id="#743289384279"
                    )
                    flex_message = FlexSendMessage(alt_text="Receipt", contents=receipt_flex)
                    line_bot_api.reply_message(event.reply_token, flex_message)
                    return
                elif user_message.startswith("stock"):
                    logger.debug("處理股票信息請求")
                    parts = user_message.split()
                    if len(parts) < 2:
                        reply_text = "請提供股票代碼，例如：stock 0050"
                        logger.debug(f"發送回覆: {reply_text}")
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                    else:
                        stock_code = parts[1]
                        logger.debug(f"獲取股票代碼: {stock_code}")
                        try:
                            stock_info = TWStockAPI.get_stock_info(stock_code)
                            logger.debug(f"獲取到的股票信息: {stock_info}")
                            if isinstance(stock_info, dict) and "error" in stock_info:
                                error_message = stock_info["error"]
                                logger.debug(f"發送錯誤信息: {error_message}")
                                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"抱歉，{error_message}"))
                            else:
                                logger.debug("創建 Flex Message")
                                flex_message = create_stock_flex_message(stock_info)
                                logger.debug("發送 Flex Message")
                                line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text=f"股票 {stock_code} 信息", contents=flex_message))
                        except Exception as e:
                            logger.exception("處理股票信息時發生錯誤")
                            error_message = f"處理股票 {stock_code} 信息時發生錯誤：{str(e)}"
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_message))
                    logger.debug("股票信息處理完成")
                    return
                else:
                    reply_text = user_message
        except Exception as e:
            print(f"資料庫查詢錯誤: {e}")
            reply_text = "查詢失敗，請稍後再試。"
    
    message = TextSendMessage(text=reply_text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)