import os
from venv import logger
import requests
import psycopg2
from flask import Flask, json, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, ImageSendMessage
from line_member_system import LineMemberSystem
from flex_message_library import create_bubble, create_carousel, create_receipt_flex_message, create_shopping_list_flex_message, create_stock_flex_message, create_ticket_flex_message, create_transit_flex_message
from stock_api import TWStockAPI  
import os
import logging
import tempfile
import base64


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])
OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']  # 請確保設置這個環境變數

# 資料庫連接函數
def get_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')

member_system = LineMemberSystem(get_connection)

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
    

# 創建臨時目錄來存儲圖片
TEMP_DIR = tempfile.mkdtemp()

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
    user_id = event.source.user_id
    profile = get_user_profile(user_id)
    member = get_or_create_member(user_id, profile.display_name)

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
                elif user_message.lower().strip() == "flexmessage":
                    bubble1 = create_bubble("In Progress", 70, "Buy milk and lettuce before class", {"background": "#27ACB2", "bar": "#0D8186"})
                    bubble2 = create_bubble("Pending", 30, "Wash my car", {"background": "#FF6B6E", "bar": "#DE5658"})
                    bubble3 = create_bubble("In Progress", 100, "Buy milk and lettuce before class", {"background": "#A17DF5", "bar": "#7D51E4"})
                    
                    carousel = create_carousel([bubble1, bubble2, bubble3])
                    
                    flex_message = FlexSendMessage(alt_text="Task Progress", contents=carousel)
                    line_bot_api.reply_message(event.reply_token, flex_message)
                    return
                elif user_message.lower().strip() == "ticket":
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
                elif user_message.lower().strip() == "shopping":
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
                elif user_message.lower().strip() == "transit":
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
                elif user_message.lower().strip() == "receipt":
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
                elif user_message.lower().strip().startswith("stock"):
                    stock_code = user_message.split()[1]
                    stock_info = TWStockAPI.get_stock_info(stock_code)
                    flex_message = create_stock_flex_message(stock_info)
                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage(alt_text=f"股票 {stock_code} 信息", contents=flex_message)
                    )
                    return
                elif user_message.startswith("chart"):
                    stock_code = user_message.split()[1]
                    image_base64 = TWStockAPI.create_happy_5_lines_chart(stock_code)
                    
                    # 將 base64 圖片數據解碼並保存為文件
                    image_data = base64.b64decode(image_base64)
                    filename = f"chart_{stock_code}.png"
                    file_path = os.path.join(TEMP_DIR, filename)
                    with open(file_path, "wb") as f:
                        f.write(image_data)
                    
                    # 構建圖片 URL
                    image_url = f"https://{request.host}/image/{filename}"
                    
                    line_bot_api.reply_message(
                        event.reply_token,
                        ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
                    )
                    return
                else:
                    user_profile = get_user_profile(user_id)
                    reply_text = f"您的訊息是：{user_message}\n\n用戶資訊：\n用戶ID：{user_id}\n名稱：{user_profile.display_name}\n狀態消息：{user_profile.status_message}\n個人頭像URL：{user_profile.picture_url}"
                    
        except Exception as e:
            print(f"資料庫查詢錯誤: {e}")
            reply_text = "查詢失敗，請稍後再試。"
    
    message = TextSendMessage(text=reply_text)
    line_bot_api.reply_message(event.reply_token, message)

def get_user_profile(user_id):
    try:
        return line_bot_api.get_profile(user_id)
    except LineBotApiError as e:
        logger.error(f"獲取用戶資料失敗: {str(e)}")
        raise

def get_or_create_member(user_id, display_name):
    member = member_system.get_member(user_id)
    if not member:
        member_system.register_member(user_id, display_name)
        logger.info(f"新會員註冊: {display_name}")
        member = member_system.get_member(user_id)
    else:
        member_system.update_last_interaction(user_id)
    return member

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)