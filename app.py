import os
from venv import logger
import pytz
from datetime import datetime
import requests
import psycopg2
from oms_functions import get_stores, get_store_products, add_to_cart, get_cart_contents, add_store, add_product, get_product
from flask import Flask, json, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, ImageSendMessage
from line_member_system import LineMemberSystem
from flex_message_library import create_bubble, create_carousel, create_receipt_flex_message, create_shopping_list_flex_message, create_stock_flex_message, create_ticket_flex_message, create_transit_flex_message
from stock_api import TWStockAPI  
import os
import google.generativeai as genai
import logging
import tempfile
import base64

# 設置 Gemini API
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# 用戶狀態管理
user_states = {}
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
                if user_message.lower().strip() == "podcast":
                    from notes import check_notion_connection, get_latest_podcast_summary
                    if check_notion_connection():
                        latest_summary = get_latest_podcast_summary()
                        if latest_summary:
                            reply_text = "最新播客摘要：\n\n"
                            reply_text += f"標題：{latest_summary['title']}\n"
                            reply_text += f"鏈接：{latest_summary['link']}\n"
                            reply_text += f"摘要：{latest_summary['summary'][:50]}...\n"
                        else:
                            reply_text = "目前沒有可用的播客摘要。"
                    else:
                        reply_text = "無法連接到Notion。請稍後再試。"
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
                    conn = get_connection()
                    stores = get_stores(conn)
                    conn.close()
                    flex_message = create_shopping_list_flex_message(stores, is_store_list=True)
                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage(alt_text="店家列表", contents=flex_message)
                    )
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
                    flex_message = FlexSendMessage(alt_text=f"股票 {stock_code} 信息", contents=create_stock_flex_message(stock_info))
                    line_bot_api.reply_message(event.reply_token, flex_message) 
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
                elif user_message.lower() in ["我的資訊", "member"]:
                    reply = process_user_message(user_message, member, profile.display_name, user_id)
                    line_bot_api.reply_message(event.reply_token, reply)
                    return
                elif user_message.lower() == "members":
                    reply = process_user_message(user_message, member, profile.display_name, user_id)
                    line_bot_api.reply_message(event.reply_token, reply)
                    return
                elif user_message.lower().startswith("broadcast "):
                    reply = broadcast_message(user_message, member, profile.display_name, user_id)
                    line_bot_api.reply_message(event.reply_token, reply)
                elif user_message.lower().startswith("gemini "):
                    query = user_message[7:]  # 去掉 "gemini " 前綴
                    if len(query) > 500:  # 假設我們限制查詢最多500個字符
                        return TextSendMessage(text="抱歉，您的查詢太長了。請將查詢限制在500個字符以內。")
                    try:
                        response = model.generate_content(query)
                        return TextSendMessage(text=response.text)
                    except Exception as e:
                        logger.error(f"使用 Gemini API 時發生錯誤: {str(e)}")
                        return TextSendMessage(text="抱歉，處理您的請求時發生錯誤。請稍後再試。")
                elif user_message == "Add store":
                    user_states[user_id] = {"state": "waiting_for_store_name"}
                    reply_text = "請輸入新店家的名稱:"
                elif user_message.startswith("選擇店家"):
                    store_id = user_message.split()[-1]
                    conn = get_connection()
                    products = get_store_products(conn, store_id)
                    conn.close()
                    if products:
                        flex_message = create_shopping_list_flex_message(products, is_store_list=False)
                        line_bot_api.reply_message(
                            event.reply_token,
                            FlexSendMessage(alt_text="商品列表", contents=flex_message)
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="該店家目前沒有商品。")
                        )
                elif user_message == "批量添加商品":
                    user_states[user_id] = {"state": "waiting_for_store_id_bulk"}
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="請輸入要添加商品的店家ID:")
                    )
                elif user_message.startswith("添加商品"):
                    try:
                        _, product_id, quantity = user_message.split()
                        product_id = int(product_id)
                        quantity = int(quantity)
                        
                        conn = get_connection()
                        product = get_product(conn, product_id)
                        if not product:
                            raise ValueError("商品不存在")
                        
                        if quantity <= 0:
                            raise ValueError("數量必須大於0")
                        
                        if quantity > product['stock_quantity']:
                            raise ValueError("庫存不足")
                        
                        add_to_cart(conn, user_id, product_id, quantity)
                        conn.close()
                        
                        reply_text = f"已將 {quantity} 個 {product['name']} 添加到購物車"
                    except ValueError as e:
                        reply_text = f"添加失敗: {str(e)}"
                    except Exception as e:
                        reply_text = "添加失敗,請稍後再試"
                    
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)
                    )

                elif user_message.lower() == "查看購物車":
                    conn = get_connection()
                    cart_items = get_cart_contents(conn, user_id)
                    conn.close()
                    if not cart_items:
                        reply_text = "您的購物車是空的"
                    else:
                        total = sum(item['subtotal'] for item in cart_items)
                        flex_message = create_receipt_flex_message(
                            store_name="您的購物車",
                            address="",
                            items=cart_items,
                            total=total,
                            cash=0,
                            change=0,
                            payment_id=""
                        )
                        line_bot_api.reply_message(
                            event.reply_token,
                            FlexSendMessage(alt_text="購物車內容", contents=flex_message)
                        )
                    
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=reply_text)
                    )
                elif user_message.lower() == "clear":
                    del user_states[user_id]  # 清除用戶狀態
                elif user_id in user_states:
                    state = user_states[user_id]["state"]
                    if state == "waiting_for_store_name":
                        user_states[user_id]["store_name"] = user_message
                        user_states[user_id]["state"] = "waiting_for_store_description"
                        reply_text = "請輸入店家的描述:"
                    elif state == "waiting_for_store_description":
                        store_name = user_states[user_id]["store_name"]
                        store_description = user_message
                        conn = get_connection()
                        new_store = add_store(conn, store_name, store_description)
                        conn.close()
                        reply_text = f"已成功添加新店家:\n名稱: {new_store['name']}\n描述: {store_description}\nID: {new_store['id']}"
                        del user_states[user_id]  # 清除用戶狀態
                    elif state == "waiting_for_store_id_bulk":
                        user_states[user_id]["store_id"] = user_message
                        user_states[user_id]["state"] = "waiting_for_bulk_products"
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="請輸入商品信息,格式為:\n商品名稱,描述,價格,庫存數量;商品名稱2,描述2,價格2,庫存數量2;...")
                        )
                    elif state == "waiting_for_bulk_products":
                        store_id = user_states[user_id]["store_id"]
                        products = user_message.split(";")
                        added_products = []
                        skipped_products = []
                        for product in products:
                            try:
                                name, description, price, quantity = product.split(",")
                                name = name.strip()
                                if not name:  # 如果名稱是空白的則跳過
                                    continue
                                description = description.strip()
                                price = float(price)
                                quantity = int(quantity)
                                new_product = add_product(conn, store_id, name, description, price, quantity)
                                if new_product:
                                    added_products.append(new_product)
                                else:
                                    skipped_products.append(name)
                            except (ValueError, IndexError):
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text=f"添加商品 '{product}' 時出錯,請檢查格式是否正確。")
                                )
                                return
                        del user_states[user_id]
                        reply_text = "操作結果:\n"
                        if added_products:
                            reply_text += "成功添加以下商品:\n"
                            for product in added_products:
                                reply_text += f"名稱: {product['name']}, 價格: {product['price']}, 庫存: {product['stock_quantity']}\n"
                        if skipped_products:
                            reply_text += "\n以下商品已存在,已跳過:\n"
                            for name in skipped_products:
                                reply_text += f"{name}\n"
                        
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=reply_text)
                        )
                    else:
                        reply_text = "發生錯誤,請重新開始添加店家流程。"
                        del user_states[user_id]  # 清除用戶狀態
                else:
                    reply_text = f"{user_message}"
                    
        except Exception as e:
            print(f"資料庫查詢錯誤: {e}")
            del user_states[user_id]  # 清除用戶狀態
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
    tw_tz = pytz.timezone('Asia/Taipei')
    current_time = datetime.now(tw_tz)
    
    if not member:
        member_system.register_member(user_id, display_name, current_time)
        logger.info(f"新會員註冊: {display_name}")
        member = member_system.get_member(user_id)
    else:
        member_system.update_last_interaction(user_id, current_time)
    return member

def process_user_message(user_message, member, display_name, user_id):
    logger.debug(f"收到用戶消息: {user_message}")
    
    if user_message.lower() in ["我的資訊", "member"]:
        flex_content = member_system.get_member_info_flex_message(member)
        return FlexSendMessage(alt_text="會員資訊", contents=flex_content)
    elif user_message.lower() == "加分":
        member_system.add_points(member[1], 10)  # 使用 line_user_id
        return TextSendMessage(text=f"恭喜獲得 10 積分！\nUser ID: {user_id}\n顯示名稱: {display_name}")
    elif user_message.lower() == "hi":
        return TextSendMessage(text=f"你好，{display_name}！有什麼我可以幫助你的嗎？\nUser ID: {user_id}\n顯示名稱: {display_name}")
    elif user_message.lower() == "members":
        if not member_system.is_admin(user_id):
            return TextSendMessage(text="抱歉，只有管理員可以查看所有會員信息。")
        
        all_members = member_system.get_all_members()
        flex_content = member_system.create_members_flex_message(all_members)
        return FlexSendMessage(alt_text="所有會員信息", contents=flex_content)
    else:
        return TextSendMessage(text=f"您說: {user_message}\nUser ID: {user_id}\n顯示名稱: {display_name}\n\n您可以輸入「我的資訊」或「member」來查看會員資訊，「加分」來獲得積分，或者只是說「hi」來打個招呼。")
    
def broadcast_message(user_message, member, display_name, user_id):
    logger.debug(f"收到用戶消息: {user_message}")
    
    if user_message.lower().startswith("broadcast "):
        if member[3] != 'admin':  # 假設會員資料的第四個欄位是狀態，只有管理員可以發送廣播
            return TextSendMessage(text="抱歉，您沒有權限發送廣播訊息。")
        
        broadcast_message = user_message[10:]  # 去掉 "broadcast " 前綴
        member_ids = member_system.get_all_member_ids()
        
        try:
            line_bot_api.multicast(member_ids, TextSendMessage(text=broadcast_message))
            return TextSendMessage(text=f"廣播訊息已發送給 {len(member_ids)} 位會員。")
        except LineBotApiError as e:
            logger.error(f"發送廣播訊息時發生錯誤: {str(e)}")
            return TextSendMessage(text="發送廣播訊息時發生錯誤，請稍後再試。")
 
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)