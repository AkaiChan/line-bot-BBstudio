from datetime import datetime

class LineMemberSystem:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def get_member(self, line_user_id):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM line_members WHERE line_user_id = %s", (line_user_id,))
                return cur.fetchone()

    def register_member(self, line_user_id, display_name):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                INSERT INTO line_members (line_user_id, display_name)
                VALUES (%s, %s)
                ON CONFLICT (line_user_id) DO UPDATE
                SET display_name = EXCLUDED.display_name,
                    last_interaction = CURRENT_TIMESTAMP
                ''', (line_user_id, display_name))
            conn.commit()

    def update_last_interaction(self, line_user_id):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                UPDATE line_members
                SET last_interaction = CURRENT_TIMESTAMP
                WHERE line_user_id = %s
                ''', (line_user_id,))
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

