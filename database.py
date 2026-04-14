import mysql.connector
from datetime import datetime

class Database:
    def __init__(self, host="172.19.135.113"): # Default host ကို ပြင်ဆင်ထားသည်
        try:
            # ချိတ်ဆက်မှု ပိုမြန်စေရန် connection timeout ထည့်ထားသည်
            self.conn = mysql.connector.connect(
                host=host, 
                user="root",
                password="",  
                database="wfh_system",
                autocommit=True,
                connect_timeout=10 
            )
            # buffered=True သည် cursor တစ်ခုတည်းဖြင့် query အများကြီး run ရန် အဆင်ပြေစေသည်
            self.cursor = self.conn.cursor(dictionary=True, buffered=True)
            print(f"✅ Successfully connected to XAMPP Database at {host}")
            
        except mysql.connector.Error as err:
            print(f"❌ Database Connection Error: {err}")
            self.conn = None

    # --- Authentication ---
    def authenticate(self, username, password):
        if not self.conn: return None
        try:
            # Password ကို plain text သုံးထားလျှင် ဤအတိုင်း သုံးနိုင်သည်
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Authentication Error: {e}")
            return None

    # --- Attendance ---
    def check_in_user(self, user_id, location):
        if not self.conn: return False
        today = datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.now().strftime('%H:%M:%S')
        try:
            # ၁။ Attendance record သစ်သွင်းခြင်း
            sql_att = "INSERT INTO attendance (user_id, attendance_date, check_in, location_type) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql_att, (user_id, today, now_time, location))
            
            # ၂။ User ၏ current status (Work Mode) ကို update လုပ်ခြင်း
            # သင့် Table အရ 'current_status' သည် Enum('Office','WFH') ဖြစ်၍ location နှင့် ကိုက်ညီရပါမည်
            sql_user = "UPDATE users SET current_status = %s WHERE id = %s"
            self.cursor.execute(sql_user, (location, user_id))
            return True
        except Exception as e:
            print(f"Check-in Error: {e}")
            return False

    def check_out_user(self, user_id):
        if not self.conn: return False
        today = datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.now().strftime('%H:%M:%S')
        try:
            sql_att = """
                UPDATE attendance SET check_out = %s 
                WHERE user_id = %s AND attendance_date = %s AND check_out IS NULL
                ORDER BY id DESC LIMIT 1
            """
            self.cursor.execute(sql_att, (now_time, user_id, today))
            
            # Check-out လုပ်လျှင် current_status ကို Office သို့မဟုတ် NULL ပြန်ထားနိုင်သည်
            sql_user = "UPDATE users SET current_status = 'Office' WHERE id = %s"
            self.cursor.execute(sql_user, (user_id,))
            return True
        except Exception as e:
            print(f"Check-out Error: {e}")
            return False

    # --- Live Tracking Update (အရေးကြီးဆုံးအပိုင်း) ---
    def update_live_status(self, user_id, status):
        """tracking_server မှ လှမ်းခေါ်သော function"""
        if not self.conn: return
        try:
            # သင့် Table အရ column အမည်မှာ 'status' ဖြစ်သည်
            query = "UPDATE users SET status = %s WHERE id = %s OR employee_id = %s"
            self.cursor.execute(query, (status, user_id, user_id))
            # Autocommit=True ပါသော်လည်း Real-time ဖြစ်၍ commit() ပေးခြင်းက ပိုစိတ်ချရသည်
            self.conn.commit()
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