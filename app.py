import os
import requests
import psycopg2
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from flex_message_library import create_ticket_flex_message
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