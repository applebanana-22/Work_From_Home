import mysql.connector
from datetime import datetime

class Database:
    def __init__(self, host="192.168.100.83"):
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
        
    def get_all_teams(self):
        """Team အားလုံးကို database ထဲမှ ဆွဲထုတ်ရန်"""
        try:
            self.cursor.execute("SELECT * FROM teams")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching teams: {e}")
            return []
    
    def get_status_counts(self):
        try:
            self.cursor.execute("SELECT COUNT(*) as count FROM users WHERE current_status = 'Office'")
            office_count = self.cursor.fetchone()['count']
 
            self.cursor.execute("SELECT COUNT(*) as count FROM users WHERE current_status = 'WFH'")
            wfh_count = self.cursor.fetchone()['count']
 
            return office_count, wfh_count
        except Exception as e:
            print(f"Error counting status: {e}")
            return 0, 0
        
    def check_out_user(self, user_id):
        """Attendance table တွင် check_out အချိန်ကို update လုပ်ပြီး 
           users table တွင် live status ကို offline ပြောင်းရန်"""
        try:
            self.ensure_connection()
            
            # ၁။ Attendance Table ကို Update လုပ်ခြင်း (ယနေ့အတွက်)
            query_attendance = """
                UPDATE attendance 
                SET check_out = CURTIME() 
                WHERE user_id = %s AND attendance_date = CURDATE() 
                AND check_out IS NULL
            """
            self.cursor.execute(query_attendance, (user_id,))
            
            # ၂။ Users Table ရှိ live status ကို offline ပြောင်းခြင်း
            query_user = "UPDATE users SET status = 'offline' WHERE id = %s"
            self.cursor.execute(query_user, (user_id,))
            
            self.conn.commit()
            print(f"✅ User ID {user_id} checked out successfully.")
            return True
        except Exception as e:
            print(f"❌ Check-out Error: {e}")
            if self.conn:
                self.conn.rollback()
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
            
    def insert_reply(self, announcement_id, user, message):
        """
        Insert a reply into the announcement_replies table.
        """
        try:
            query = """
                INSERT INTO announcement_replies
                (announcement_id, message, created_by, created_at)
                VALUES (%s, %s, %s, NOW())
            """
            self.cursor.execute(
                query,
                (announcement_id, message, user['full_name'])
            )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
            
    def close(self):
        try:
            if self.conn and self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("🔌 Database connection closed.")
        except Exception as e:
            print(f"Error closing database: {e}")