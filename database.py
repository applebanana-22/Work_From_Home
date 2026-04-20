import mysql.connector
from datetime import datetime

class Database:
    def __init__(self, host="192.168.1.4"):
        self.host = host
        self.connect()

    def connect(self):
        """Database ချိတ်ဆက်မှုကို စတင်ပြုလုပ်ခြင်း"""
        try:
            self.conn = mysql.connector.connect(
                host=self.host, 
                user="root",
                password="",  
                database="wfh_system",
                autocommit=True,
                connect_timeout=10 
            )
            self.cursor = self.conn.cursor(dictionary=True, buffered=True)
            print(f"✅ Successfully connected to XAMPP Database at {self.host}")
        except mysql.connector.Error as err:
            print(f"❌ Database Connection Error: {err}")
            self.conn = None

    def ensure_connection(self):
        """Connection ရှိမရှိ စစ်ဆေးပြီး ပြတ်နေပါက ပြန်ချိတ်ပေးမည် (အရေးကြီးဆုံးအပိုင်း)"""
        try:
            if self.conn and self.conn.is_connected():
                # reconnect=True ကို mysql-connector တွင် ဤသို့သုံးပါသည်
                self.conn.ping(reconnect=True, attempts=3, delay=1)
            else:
                print("🔄 Connection lost. Reconnecting...")
                self.connect()
        except Exception:
            self.connect()

    # --- Authentication ---
    def authenticate(self, username, password):
        self.ensure_connection() # Query မတိုင်ခင် အမြဲစစ်ပါ
        if not self.conn: return None
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Authentication Error: {e}")
            return None

    # --- Attendance ---
    def check_in_user(self, user_id, location):
        self.ensure_connection()
        if not self.conn: return False
        today = datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.now().strftime('%H:%M:%S')
        try:
            sql_att = "INSERT INTO attendance (user_id, attendance_date, check_in, location_type) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql_att, (user_id, today, now_time, location))
            
            sql_user = "UPDATE users SET current_status = %s WHERE id = %s"
            self.cursor.execute(sql_user, (location, user_id))
            return True
        except Exception as e:
            print(f"Check-in Error: {e}")
            return False

    # --- Live Tracking Update ---
    def update_live_status(self, user_id, status):
        """tracking_server မှ လှမ်းခေါ်သော function"""
        self.ensure_connection() # အမြဲစစ်ပေးခြင်းဖြင့် connection timeout ကို ကာကွယ်သည်
        if not self.conn: return
        try:
            query = "UPDATE users SET status = %s WHERE id = %s OR employee_id = %s"
            self.cursor.execute(query, (status, user_id, user_id))
            print(f"💾 DB Updated: {user_id} -> {status}")
        except Exception as e:
            print(f"DB Status Update Error: {e}")

    def close(self):
        try:
            if self.conn and self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("🔌 Database connection closed.")
        except Exception as e:
            print(f"Error closing database: {e}")