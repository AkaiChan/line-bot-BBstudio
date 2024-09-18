from datetime import datetime
import pytz

class LineMemberSystem:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def get_member(self, line_user_id):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM line_members WHERE line_user_id = %s", (line_user_id,))
                return cur.fetchone()

    def register_member(self, line_user_id, display_name, current_time):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                INSERT INTO line_members (line_user_id, display_name, created_at, last_interaction)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (line_user_id) DO UPDATE
                SET display_name = EXCLUDED.display_name,
                    last_interaction = EXCLUDED.last_interaction
                ''', (line_user_id, display_name, current_time, current_time))
            conn.commit()

    def update_last_interaction(self, line_user_id, current_time):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                UPDATE line_members
                SET last_interaction = %s
                WHERE line_user_id = %s
                ''', (current_time, line_user_id))
            conn.commit()

    def add_points(self, line_user_id, points):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                UPDATE line_members
                SET points = points + %s
                WHERE line_user_id = %s
                ''', (points, line_user_id))
            conn.commit()

    def format_member_info(self, member):
        if not member:
            return "You are not a member yet."
        
        id, line_user_id, display_name, status, created_at, last_interaction, points = member
        
        return {
            "display_name": display_name,
            "status": status,
            "created_at": created_at.strftime('%Y-%m-%d'),
            "last_interaction": last_interaction.strftime('%Y-%m-%d %H:%M'),
            "points": points
        }

    def get_member_info_flex_message(self, member):
        if not member:
            return {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Not a member",
                            "weight": "bold",
                            "size": "xl"
                        }
                    ]
                }
            }

        id, line_user_id, display_name, status, created_at, last_interaction, points = member
        
        # 將時間轉換為台灣時區
        tw_tz = pytz.timezone('Asia/Taipei')
        created_at = created_at.replace(tzinfo=pytz.UTC).astimezone(tw_tz)
        last_interaction = last_interaction.replace(tzinfo=pytz.UTC).astimezone(tw_tz)
        
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Member Info",
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
                                        "text": "Name",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": display_name,
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
                                        "text": "Status",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": status,
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
                                        "text": "Reg Date",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": created_at.strftime('%Y-%m-%d'),
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
                                        "text": "Last Active",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": last_interaction.strftime('%Y-%m-%d %H:%M'),
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
                                        "text": "Points",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": str(points),
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
            }
        }

    def get_all_member_ids(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT line_user_id FROM line_members")
                return [row[0] for row in cur.fetchall()]
    def get_all_members(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM line_members ORDER BY created_at DESC")
                return cur.fetchall()

    def is_admin(self, line_user_id):
        member = self.get_member(line_user_id)
        return member and member[3].lower() == 'admin'  # 假設狀態是第四個欄位
    
    def create_members_flex_message(self, members):
        bubbles = []
        tw_tz = pytz.timezone('Asia/Taipei')
        for member in members:
            id, line_user_id, display_name, status, created_at, last_interaction, points = member
            
            # Convert to Taiwan time
            created_at = created_at.replace(tzinfo=pytz.UTC).astimezone(tw_tz)
            last_interaction = last_interaction.replace(tzinfo=pytz.UTC).astimezone(tw_tz)
            
            bubble = {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": display_name,
                            "weight": "bold",
                            "size": "xl"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Status",
                                    "weight": "bold",
                                    "margin": "sm",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": status,
                                    "size": "sm",
                                    "color": "#111111",
                                    "margin": "sm",
                                    "flex": 0
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Registration Date",
                                    "weight": "bold",
                                    "margin": "sm",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": created_at.strftime('%Y-%m-%d'),
                                    "size": "sm",
                                    "color": "#111111",
                                    "margin": "sm",
                                    "flex": 0
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Last Interaction",
                                    "weight": "bold",
                                    "margin": "sm",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": last_interaction.strftime('%Y-%m-%d %H:%M'),
                                    "size": "sm",
                                    "color": "#111111",
                                    "margin": "sm",
                                    "flex": 0
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Points",
                                    "weight": "bold",
                                    "margin": "sm",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(points),
                                    "size": "sm",
                                    "color": "#111111",
                                    "margin": "sm",
                                    "flex": 0
                                }
                            ]
                        }
                    ]
                }
            }
            bubbles.append(bubble)

        return {
            "type": "carousel",
            "contents": bubbles
        }