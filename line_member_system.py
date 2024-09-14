from datetime import datetime

import psycopg2
from database_utils import get_connection # type: ignore

class LineMemberSystem:
    def __init__(self):
        self.create_table()

    def create_table(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS line_members (
            id SERIAL PRIMARY KEY,
            line_user_id TEXT UNIQUE,
            display_name TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP,
            last_interaction TIMESTAMP,
            points INTEGER DEFAULT 0
        )
        ''')
        conn.commit()
        cur.close()
        conn.close()

    def register_member(self, line_user_id, display_name):
        conn = get_connection()
        cur = conn.cursor()
        now = datetime.now()
        try:
            cur.execute('''
            INSERT INTO line_members (line_user_id, display_name, created_at, last_interaction)
            VALUES (%s, %s, %s, %s)
            ''', (line_user_id, display_name, now, now))
            conn.commit()
            success = True
        except psycopg2.IntegrityError:
            conn.rollback()
            success = False
        finally:
            cur.close()
            conn.close()
        return success

    def get_member(self, line_user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM line_members WHERE line_user_id = %s', (line_user_id,))
        member = cur.fetchone()
        cur.close()
        conn.close()
        return member

    def update_last_interaction(self, line_user_id):
        conn = get_connection()
        cur = conn.cursor()
        now = datetime.now()
        cur.execute('''
        UPDATE line_members SET last_interaction = %s WHERE line_user_id = %s
        ''', (now, line_user_id))
        conn.commit()
        cur.close()
        conn.close()

    def add_points(self, line_user_id, points):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
        UPDATE line_members SET points = points + %s WHERE line_user_id = %s
        ''', (points, line_user_id))
        conn.commit()
        cur.close()
        conn.close()

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

