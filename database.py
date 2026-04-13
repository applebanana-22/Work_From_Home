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
                autocommit=True # SQL အပြောင်းအလဲများကို ချက်ချင်းတည်မြဲစေရန်
            )
            # buffered=True သည် query တစ်ခုထက်မက တစ်ပြိုင်တည်း run လျှင် error မတက်အောင် ကာကွယ်ပေးပါသည်
            self.cursor = self.conn.cursor(dictionary=True, buffered=True)
            print(f"✅ Successfully connected to XAMPP Database at {host}")
            
        except mysql.connector.Error as err:
            print(f"❌ Database Connection Error: {err}")
            messagebox.showerror("Database Error", f"Connection failed: {err}\nCheck if XAMPP and MySQL are running.")

    # --- Authentication ---
    def authenticate(self, username, password):
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Authentication Error: {e}")
            return None

    # --- Attendance ---
    def check_in_user(self, user_id, location):
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

    def check_out_user(self, user_id):
        today = datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.now().strftime('%H:%M:%S')
        try:
            sql_att = """
                UPDATE attendance SET check_out = %s 
                WHERE user_id = %s AND attendance_date = %s AND check_out IS NULL
                ORDER BY id DESC LIMIT 1
            """
            self.cursor.execute(sql_att, (now_time, user_id, today))
            sql_user = "UPDATE users SET current_status = NULL WHERE id = %s"
            self.cursor.execute(sql_user, (user_id,))
            return True
        except Exception as e:
            print(f"Check-out Error: {e}")
            return False

    # --- Live Tracking Update ---
    def update_live_status(self, user_id, status):
        """Member ၏ Live status (active, away, offline) ကို Database တွင် update လုပ်ရန်"""
        try:
            query = "UPDATE users SET status = %s WHERE id = %s"
            self.cursor.execute(query, (status, user_id))
            return True
        except Exception as e:
            print(f"Live Status Update Error: {e}")
            return False

    def close(self):
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("🔌 Database connection closed.")