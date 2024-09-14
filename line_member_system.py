import sqlite3
from datetime import datetime
from flex_message_library import create_member_info_flex_message

class LineMemberSystem:
    def __init__(self, db_name='line_members.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS line_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            line_user_id TEXT UNIQUE,
            display_name TEXT,
            status TEXT,
            created_at DATETIME,
            last_interaction DATETIME,
            points INTEGER DEFAULT 0
        )
        ''')
        self.conn.commit()

    def register_member(self, line_user_id, display_name):
        created_at = datetime.now()
        
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO line_members (line_user_id, display_name, status, created_at, last_interaction)
            VALUES (?, ?, ?, ?, ?)
            ''', (line_user_id, display_name, 'active', created_at, created_at))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_member(self, line_user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM line_members WHERE line_user_id = ?', (line_user_id,))
        return cursor.fetchone()

    def update_member(self, line_user_id, **kwargs):
        allowed_fields = ['display_name', 'status', 'points']
        update_fields = []
        values = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                update_fields.append(f"{key} = ?")
                values.append(value)
        
        if not update_fields:
            return False
        
        values.append(line_user_id)
        
        cursor = self.conn.cursor()
        cursor.execute(f'''
        UPDATE line_members SET {', '.join(update_fields)}
        WHERE line_user_id = ?
        ''', tuple(values))
        self.conn.commit()
        return True

    def update_last_interaction(self, line_user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE line_members SET last_interaction = ? WHERE line_user_id = ?
        ''', (datetime.now(), line_user_id))
        self.conn.commit()

    def add_points(self, line_user_id, points):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE line_members SET points = points + ? WHERE line_user_id = ?
        ''', (points, line_user_id))
        self.conn.commit()

    def get_all_members(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM line_members')
        return cursor.fetchall()

    def delete_member(self, line_user_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM line_members WHERE line_user_id = ?', (line_user_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def close(self):
        self.conn.close()

    def format_member_info(self, member):
        if not member:
            return "您還不是會員。"
        
        id, line_user_id, display_name, status, created_at, last_interaction, points = member
        created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")
        last_interaction = datetime.strptime(last_interaction, "%Y-%m-%d %H:%M:%S.%f")
        
        return {
            "display_name": display_name,
            "status": status,
            "created_at": created_at.strftime('%Y-%m-%d'),
            "last_interaction": last_interaction.strftime('%Y-%m-%d %H:%M'),
            "points": points
        }

    def get_member_info_flex_message(self, member):
        member_info = self.format_member_info(member)
        return create_member_info_flex_message(member_info)
