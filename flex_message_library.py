def create_ticket_flex_message(title, rating, date, place, seats, image_url, qr_code_url):
    return {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "https://line.me/"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "wrap": True,
                    "weight": "bold",
                    "gravity": "center",
                    "size": "xl"
                },
                create_rating_box(rating),
                create_info_box("Date", date),
                create_info_box("Place", place),
                create_info_box("Seats", seats),
                create_qr_code_box(qr_code_url)
            ]
        }
    }

def create_rating_box(rating):
    stars = int(float(rating))
    return {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
            *[{
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
            } for _ in range(stars)],
            *[{
                "type": "icon",
                "size": "sm",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
            } for _ in range(5 - stars)],
            {
                "type": "text",
                "text": str(rating),
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0
            }
        ]
    }

def create_info_box(label, value):
    return {
        "type": "box",
        "layout": "baseline",
        "spacing": "sm",
        "contents": [
            {
                "type": "text",
                "text": label,
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
            },
            {
                "type": "text",
                "text": value,
                "wrap": True,
                "size": "sm",
                "color": "#666666",
                "flex": 4
            }
        ]
    }

def create_qr_code_box(qr_code_url):
    return {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "contents": [
            {
                "type": "image",
                "url": qr_code_url,
                "aspectMode": "cover",
                "size": "xl",
                "margin": "md"
            },
            {
                "type": "text",
                "text": "You can enter the theater by using this code instead of a ticket",
                "color": "#aaaaaa",
                "wrap": True,
                "margin": "xxl",
                "size": "xs"
            }
        ]
    }
def create_bubble(status, percentage, task, color):
    return {
        "type": "bubble",
        "size": "nano",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": status,
                    "color": "#ffffff",
                    "align": "start",
                    "size": "md",
                    "gravity": "center"
                },
                {
                    "type": "text",
                    "text": f"{percentage}%",
                    "color": "#ffffff",
                    "align": "start",
                    "size": "xs",
                    "gravity": "center",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [{"type": "filler"}],
                            "width": f"{percentage}%",
                            "backgroundColor": color["bar"],
                            "height": "6px"
                        }
                    ],
                    "backgroundColor": "#9FD8E36E",
                    "height": "6px",
                    "margin": "sm"
                }
            ],
            "backgroundColor": color["background"],
            "paddingTop": "19px",
            "paddingAll": "12px",
            "paddingBottom": "16px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": task,
                            "color": "#8C8C8C",
                            "size": "sm",
                            "wrap": True
                        }
                    ],
                    "flex": 1
                }
            ],
            "spacing": "md",
            "paddingAll": "12px"
        },
        "styles": {
            "footer": {
                "separator": False
            }
        }
    }

def create_carousel(bubbles):
    return {
        "type": "carousel",
        "contents": bubbles
    }

def create_shopping_list_flex_message(items, is_store_list=False):
    carousel_contents = []
    for item in items:
        if is_store_list:
            # 為店家列表創建內容
            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": item['name'],
                            "size": "md",
                            "weight": "bold",
                            "color": "#555555"
                        },
                        {
                            "type": "text",
                            "text": item.get('description', '暫無描述'),
                            "size": "xs",
                            "color": "#888888",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"ID: {item['id']}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "flex": 1
                                },
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                        "type": "message",
                                        "label": "選擇",
                                        "text": f"選擇店家 {item['id']}"
                                    },
                                    "flex": 1
                                }
                            ],
                            "margin": "md"
                        }
                    ],
                    "paddingBottom": "10px"
                }
            }
        else:
            # 使用原有的create_item_bubble函數創建商品氣泡
            bubble = create_item_bubble(item)
        
        carousel_contents.append(bubble)
    
    if not is_store_list:
        # 只有在顯示商品列表時才添加"查看更多"氣泡
        carousel_contents.append(create_see_more_bubble())
    
    return {
        "type": "carousel",
        "contents": carousel_contents
    }

def create_item_bubble(item):
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": item['name'],
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "描述",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": item['description'],
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "價格",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": f"${item['price']}",
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "庫存",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": str(item['stock_quantity']),
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "添加到購物車",
                        "text": f"添加商品 {item['id']} 1"  # 默認添加1個
                    }
                }
            ],
            "flex": 0
        }
    }

def create_price_box(price):
    dollars, cents = str(price).split(".")
    return {
        "type": "box",
        "layout": "baseline",
        "contents": [
            {
                "type": "text",
                "text": f"${dollars}",
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "flex": 0
            },
            {
                "type": "text",
                "text": f".{cents}",
                "wrap": True,
                "weight": "bold",
                "size": "sm",
                "flex": 0
            }
        ]
    }

def create_out_of_stock_text():
    return {
        "type": "text",
        "text": "Temporarily out of stock",
        "wrap": True,
        "size": "xxs",
        "margin": "md",
        "color": "#ff5551",
        "flex": 0
    }

def create_button(label, style="default", out_of_stock=False):
    button = {
        "type": "button",
        "action": {
            "type": "uri",
            "label": label,
            "uri": "https://line.me/"
        }
    }
    if style == "primary":
        button["style"] = "primary"
    if out_of_stock:
        button["color"] = "#aaaaaa"
    return button

def create_see_more_bubble():
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "flex": 1,
                    "gravity": "center",
                    "action": {
                        "type": "uri",
                        "label": "See more",
                        "uri": "https://line.me/"
                    }
                }
            ]
        }
    }

def create_transit_flex_message(from_station, to_station, total_time, route):
    return {
        "type": "bubble",
        "size": "mega",
        "header": create_header(from_station, to_station),
        "body": create_body(total_time, route)
    }

def create_header(from_station, to_station):
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            create_station_box("FROM", from_station),
            create_station_box("TO", to_station)
        ],
        "paddingAll": "20px",
        "backgroundColor": "#0367D3",
        "spacing": "md",
        "height": "154px",
        "paddingTop": "22px"
    }

def create_station_box(label, station):
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": label,
                "color": "#ffffff66",
                "size": "sm"
            },
            {
                "type": "text",
                "text": station,
                "color": "#ffffff",
                "size": "xl",
                "flex": 4,
                "weight": "bold"
            }
        ]
    }

def create_body(total_time, route):
    contents = [
        {
            "type": "text",
            "text": f"Total: {total_time}",
            "color": "#b7b7b7",
            "size": "xs"
        }
    ]
    for i, step in enumerate(route):
        contents.append(create_station_step(step))
        if i < len(route) - 1:
            contents.append(create_transit_step(route[i], route[i+1]))
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": contents
    }

def create_station_step(step):
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": step["time"],
                "size": "sm",
                "gravity": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "cornerRadius": "30px",
                        "height": "12px",
                        "width": "12px",
                        "borderColor": step["color"],
                        "borderWidth": "2px"
                    },
                    {
                        "type": "filler"
                    }
                ],
                "flex": 0
            },
            {
                "type": "text",
                "text": step["station"],
                "gravity": "center",
                "flex": 4,
                "size": "sm"
            }
        ],
        "spacing": "lg",
        "cornerRadius": "30px",
        "margin": "xl"
    }

def create_transit_step(from_step, to_step):
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "box",
                "layout": "baseline",
                "contents": [{"type": "filler"}],
                "flex": 1
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "filler"},
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "width": "2px",
                                "backgroundColor": to_step["color"]
                            },
                            {"type": "filler"}
                        ],
                        "flex": 1
                    }
                ],
                "width": "12px"
            },
            {
                "type": "text",
                "text": from_step["transit"],
                "gravity": "center",
                "flex": 4,
                "size": "xs",
                "color": "#8c8c8c"
            }
        ],
        "spacing": "lg",
        "height": "64px"
    }

def create_receipt_flex_message(store_name, address, items, total, cash, change, payment_id):
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "RECEIPT",
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": store_name,
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": address,
                    "size": "xs",
                    "color": "#aaaaaa",
                    "wrap": True
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                create_item_list(items),
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                create_summary(len(items), total, cash, change),
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                create_payment_info(payment_id)
            ]
        },
        "styles": {
            "footer": {
                "separator": True
            }
        }
    }

def create_item_list(items):
    contents = [create_item_box(item["name"], item["price"]) for item in items]
    return {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm",
        "contents": contents
    }

def create_item_box(name, price):
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": name,
                "size": "sm",
                "color": "#555555",
                "flex": 0
            },
            {
                "type": "text",
                "text": f"${price:.2f}",
                "size": "sm",
                "color": "#111111",
                "align": "end"
            }
        ]
    }

def create_summary(item_count, total, cash, change):
    return {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm",
        "contents": [
            create_summary_row("ITEMS", str(item_count)),
            create_summary_row("TOTAL", f"${total:.2f}"),
            create_summary_row("CASH", f"${cash:.2f}"),
            create_summary_row("CHANGE", f"${change:.2f}")
        ]
    }

def create_summary_row(label, value):
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": label,
                "size": "sm",
                "color": "#555555"
            },
            {
                "type": "text",
                "text": value,
                "size": "sm",
                "color": "#111111",
                "align": "end"
            }
        ]
    }

def create_payment_info(payment_id):
    return {
        "type": "box",
        "layout": "horizontal",
        "margin": "md",
        "contents": [
            {
                "type": "text",
                "text": "PAYMENT ID",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0
            },
            {
                "type": "text",
                "text": payment_id,
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
            }
        ]
    }

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_stock_flex_message(stock_info):
    # 計算漲跌幅
    try:
        change = round(float(stock_info['收盤價']) - float(stock_info['昨日收盤價']), 2)
        change_percent = round((change / float(stock_info['昨日收盤價'])) * 100, 2)
        change_color = "#FF0000" if change >= 0 else "#00FF00"
    except ValueError:
        change = 0
        change_percent = 0
        change_color = "#888888"

    def format_number(number, width=8):
        return f"{float(number):>{width}.2f}"

    def create_data_row(label, value, color="#111111"):
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": label,
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": value,
                    "size": "sm",
                    "color": color,
                    "align": "end",
                    "wrap": False
                }
            ]
        }

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"{stock_info['股票名稱']} ({stock_info['股票代碼']})",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1DB446"
                },
                {
                    "type": "text",
                    "text": stock_info['日期'],
                    "size": "sm",
                    "color": "#888888"
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xxl",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                create_data_row("Close", format_number(stock_info['收盤價'])),
                                create_data_row("Open", format_number(stock_info['開盤價'])),
                                create_data_row("High", format_number(stock_info['最高價']))
                            ],
                            "flex": 1
                        },
                        {
                            "type": "separator",
                            "margin": "sm"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                create_data_row("Change", format_number(change), change_color),
                                create_data_row("Change%", f"{change_percent:>7.2f}%", change_color),
                                create_data_row("Low", format_number(stock_info['最低價']))
                            ],
                            "flex": 1
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                create_data_row("Volume", f"{int(stock_info['成交股數']):,}"),
                *([create_data_row("樂活五線譜", stock_info['happy_5_lines'])] if 'happy_5_lines' in stock_info else [])
            ]
        }
    }
    return bubble