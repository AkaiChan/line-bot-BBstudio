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
    if not is_store_list:
        # 只有在顯示商品列表時才添加"查看購物車"氣泡
        carousel_contents.append(create_view_cart_bubble())
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
    
    return {
        "type": "carousel",
        "contents": carousel_contents
    }
def create_view_cart_bubble():
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "查看購物車",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "點擊查看您的購物車內容",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "align": "center"
                        }
                    ]
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "message",
                        "label": "查看購物車",
                        "text": "查看購物車"
                    },
                    "margin": "md"
                }
            ]
        },
        "styles": {
            "body": {
                "backgroundColor": "#F0F8FF"
            }
        }
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

def create_receipt_flex_message(store_name, address, items, total, cash=None, change=None, payment_id=None):
    contents = [
        {
            "type": "text",
            "text": store_name,
            "weight": "bold",
            "size": "xxl",
            "margin": "md"
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
        create_summary(len(items), total, cash, change)
    ]

    if address:
        contents.insert(1, {
            "type": "text",
            "text": address,
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True
        })

    if payment_id:
        contents.extend([
            {
                "type": "separator",
                "margin": "xxl"
            },
            create_payment_info(payment_id)
        ])

    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents
        },
        "styles": {
            "footer": {
                "separator": True
            }
        }
    }

def create_item_list(items):
    contents = [create_item_box(item["name"], item["quantity"], item["price"], item["subtotal"]) for item in items]
    return {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm",
        "contents": contents
    }

def create_item_box(name, quantity, price, subtotal):
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": f"{name} x{quantity}",
                "size": "sm",
                "color": "#555555",
                "flex": 0
            },
            {
                "type": "text",
                "text": f"${subtotal:.2f}",
                "size": "sm",
                "color": "#111111",
                "align": "end"
            }
        ]
    }

def create_summary(item_count, total, cash=None, change=None):
    contents = [
        create_summary_row("商品數量", str(item_count)),
        create_summary_row("總計", f"${total:.2f}")
    ]
    if cash is not None:
        contents.append(create_summary_row("支付", f"${cash:.2f}"))
    if change is not None:
        contents.append(create_summary_row("找零", f"${change:.2f}"))
    return {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm",
        "contents": contents
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
    """
    創建股票資訊的 Flex Message
    """
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"{stock_info['name']} ({stock_info['code']})",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1DB446"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "現價",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": f"{stock_info['current_price']}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "flex": 2
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "漲跌",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": f"{stock_info['change']} ({stock_info['change_percent']}%)",
                                    "size": "sm",
                                    "color": f"{'#FF0000' if stock_info['change'] > 0 else '#00FF00' if stock_info['change'] < 0 else '#111111'}",
                                    "align": "end",
                                    "flex": 2
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "最高",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": f"{stock_info['high_price']}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "flex": 2
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "最低",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": f"{stock_info['low_price']}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "flex": 2
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "成交量",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": f"{stock_info['volume']}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end",
                                    "flex": 2
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xxl",
                    "contents": [
                        {
                            "type": "text",
                            "text": "建議",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": stock_info['recommendation'],
                            "size": "sm",
                            "color": "#111111",
                            "align": "end",
                            "flex": 2
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "更新時間",
                            "size": "xs",
                            "color": "#aaaaaa",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": stock_info['time'],
                            "size": "xs",
                            "color": "#aaaaaa",
                            "align": "end",
                            "flex": 2
                        }
                    ]
                }
            ]
        }
    }