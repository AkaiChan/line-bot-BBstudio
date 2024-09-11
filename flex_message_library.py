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

def create_shopping_list_flex_message(items):
    carousel_contents = [create_item_bubble(item) for item in items]
    carousel_contents.append(create_see_more_bubble())
    
    return {
        "type": "carousel",
        "contents": carousel_contents
    }

def create_item_bubble(item):
    return {
        "type": "bubble",
        "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": item["image_url"]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": item["name"],
                    "wrap": True,
                    "weight": "bold",
                    "size": "xl"
                },
                create_price_box(item["price"]),
                *([create_out_of_stock_text()] if item.get("out_of_stock") else [])
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                create_button("Add to Cart", "primary", item.get("out_of_stock")),
                create_button("Add to wishlist")
            ]
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

def create_stock_flex_message(stock_info):
    # Parse stock information
    lines = stock_info.split('\n')
    stock_code = lines[0].split(' ')[1]
    date = lines[1].split('：')[1]
    
    # Function to format numbers to two decimal places
    def format_number(value):
        try:
            return f"{float(value):.2f}"
        except ValueError:
            return value

    # Parse and format values
    current_price = format_number(lines[2].split('：')[1].split(' ')[0])
    change = lines[3].split('：')[1]
    change_value, change_percent = change.split(' ')
    change_value = format_number(change_value)
    change_percent = change_percent.strip('()')
    open_price = format_number(lines[4].split('：')[1].split(' ')[0])
    high_price = format_number(lines[5].split('：')[1].split(' ')[0])
    low_price = format_number(lines[6].split('：')[1].split(' ')[0])
    volume = format_number(lines[7].split('：')[1].split(' ')[0])
    prev_close = format_number(lines[8].split('：')[1].split(' ')[0])

    # Determine color based on price change
    color = "#FF0000" if float(change_value) >= 0 else "#00FF00"

    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"Stock Code {stock_code}",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1DB446"
                },
                {
                    "type": "text",
                    "text": date,
                    "size": "sm",
                    "color": "#aaaaaa",
                    "wrap": True
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Current Price",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"${current_price}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Change",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"${change_value} ({change_percent})",
                                    "size": "sm",
                                    "color": color,
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Open",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"${open_price}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "High",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"${high_price}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Low",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"${low_price}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Volume",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"{volume}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Previous Close",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"${prev_close}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }