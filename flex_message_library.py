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