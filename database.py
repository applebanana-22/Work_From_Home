import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="wfh_system"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def authenticate(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()
    
    def get_status_counts(self):
        """Office နှင့် WFH လူဦးရေကို Database မှ ရေတွက်ရန်"""
        try:
            # Office တက်နေသူများကို ရေတွက်ခြင်း
            self.cursor.execute("SELECT COUNT(*) as count FROM users WHERE current_status = 'Office'")
            office_count = self.cursor.fetchone()['count']

            # WFH လုပ်နေသူများကို ရေတွက်ခြင်း
            self.cursor.execute("SELECT COUNT(*) as count FROM users WHERE current_status = 'WFH'")
            wfh_count = self.cursor.fetchone()['count']

            return office_count, wfh_count
        except Exception as e:
            print(f"Error counting status: {e}")
            return 0, 0