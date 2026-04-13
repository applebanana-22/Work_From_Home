import mysql.connector
from datetime import datetime
from tkinter import messagebox

class Database:
    def __init__(self, host="localhost"): 
        try:
            # XAMPP/MySQL နှင့် ချိတ်ဆက်ခြင်း
            self.conn = mysql.connector.connect(
                host=host, 
                user="root",
                password="",  
                database="wfh_system",
                autocommit=True
            )
            # dictionary=True သည် result များကို key-value format ဖြင့် ရရှိစေပါသည်
            self.cursor = self.conn.cursor(dictionary=True, buffered=True)
            print(f"✅ Successfully connected to XAMPP Database at {host}")
            
        except mysql.connector.Error as err:
            print(f"❌ Database Connection Error: {err}")
            # Messagebox သည် Main Thread မှသာ အလုပ်လုပ်နိုင်သဖြင့် error log ကိုသာ ဦးစားပေးဖော်ပြပါသည်
            # messagebox.showerror("Database Error", f"Connection failed: {err}")

    # --- Authentication ---
    def authenticate(self, username, password):
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print(f"Authentication Error: {e}")
            return None

    # --- Attendance ---
    def check_in_user(self, user_id, location):
        """Attendance table တွင် data သစ်သွင်းပြီး Users table တွင် mode ကို update လုပ်သည်"""
        today = datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.now().strftime('%H:%M:%S')
        try:
            # ၁။ Attendance record သစ်သွင်းခြင်း
            sql_att = "INSERT INTO attendance (user_id, attendance_date, check_in, location_type) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql_att, (user_id, today, now_time, location))
            
            # ၂။ User ၏ current mode (Office/WFH) ကို update လုပ်ခြင်း
            sql_user = "UPDATE users SET current_status = %s WHERE id = %s"
            self.cursor.execute(sql_user, (location, user_id))
            return True
        except Exception as e:
            print(f"Check-in Error: {e}")
            return False

    def check_out_user(self, user_id):
        """နောက်ဆုံးဝင်ထားသော record တွင် Check-out အချိန်ကို update လုပ်သည်"""
        today = datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.now().strftime('%H:%M:%S')
        try:
            # ၁။ Check-out အချိန်ကို နောက်ဆုံး record တွင် update လုပ်ခြင်း
            sql_att = """
                UPDATE attendance SET check_out = %s 
                WHERE user_id = %s AND attendance_date = %s AND check_out IS NULL
                ORDER BY id DESC LIMIT 1
            """
            self.cursor.execute(sql_att, (now_time, user_id, today))
            
            # ၂။ User ၏ current mode ကို ရှင်းထုတ်ခြင်း
            sql_user = "UPDATE users SET current_status = NULL WHERE id = %s"
            self.cursor.execute(sql_user, (user_id,))
            return True
        except Exception as e:
            print(f"Check-out Error: {e}")
            return False

    # --- Live Tracking Update ---
    def update_live_status(self, user_id, status):
        """Member ၏ Live status (ACTIVE, AWAY, OFFLINE) ကို Database တွင် update လုပ်ရန်"""
        try:
            # သင့် database structure အရ status column သည် live tracking အတွက်ဖြစ်ပါသည်
            query = "UPDATE users SET status = %s WHERE id = %s"
            self.cursor.execute(query, (status, user_id))
            return True
        except Exception as e:
            print(f"Live Status Update Error: {e}")
            return False

    def close(self):
        """Database ချိတ်ဆက်မှုကို စနစ်တကျပိတ်သိမ်းခြင်း"""
        try:
            if hasattr(self, 'conn') and self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("🔌 Database connection closed.")
        except Exception as e:
            print(f"Error closing database: {e}")