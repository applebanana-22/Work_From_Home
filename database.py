import mysql.connector
from datetime import datetime
from tkinter import messagebox

class Database:
    def __init__(self):
        try:
            # သင်၏ Database ချိတ်ဆက်မှု အချက်အလက်များအား ပြင်ဆင်ရန်
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",  # password ရှိလျှင် ထည့်ပါ
                database="wfh_system"
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Database Connection Error: {err}")
            messagebox.showerror("Database Error", f"Connection failed: {err}")

    # --- Authentication Feature ---
    def authenticate(self, username, password):
        """User login ကို စစ်ဆေးပြီး user data ကို return ပြန်ပေးသည်"""
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()
            return user 
        except Exception as e:
            print(f"Authentication Error: {e}")
            return None

    # --- Attendance Features ---
    def check_in_user(self, user_id, location):
        today = datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.now().strftime('%H:%M:%S')
        try:
            sql_att = "INSERT INTO attendance (user_id, attendance_date, check_in, location_type) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql_att, (user_id, today, now_time, location))
            
            sql_user = "UPDATE users SET current_status = %s WHERE id = %s"
            self.cursor.execute(sql_user, (location, user_id))
            
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            # Manager ဆီကို error ပြန်ပို့လိုက်မယ်
            raise e

    def check_out_user(self, user_id):
        """နောက်ဆုံးဖွင့်ထားသော (Check-out NULL ဖြစ်နေသော) record ကို ပိတ်သည်"""
        today = datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.now().strftime('%H:%M:%S')
        
        try:
            # လက်ရှိ Session ကို ပိတ်ခြင်း
            sql_att = """
                UPDATE attendance 
                SET check_out = %s 
                WHERE user_id = %s AND attendance_date = %s AND check_out IS NULL
                ORDER BY id DESC LIMIT 1
            """
            self.cursor.execute(sql_att, (now_time, user_id, today))
            
            # User ရဲ့ status ကို reset ပြန်လုပ်ခြင်း
            sql_user = "UPDATE users SET current_status = NULL WHERE id = %s"
            self.cursor.execute(sql_user, (user_id,))
            
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Check-out DB Error: {e}")
            raise e

    # --- Dashboard Utilities ---
    def get_status_counts(self):
        """Dashboard Header အတွက် Office နှင့် WFH ရောက်နေသူ အရေအတွက်တွက်ခြင်း"""
        try:
            # Office Count
            self.cursor.execute("SELECT COUNT(*) as count FROM users WHERE current_status = 'Office'")
            off_res = self.cursor.fetchone()
            off_count = off_res['count'] if off_res else 0
            
            # WFH Count
            self.cursor.execute("SELECT COUNT(*) as count FROM users WHERE current_status = 'WFH'")
            wfh_res = self.cursor.fetchone()
            wfh_count = wfh_res['count'] if wfh_res else 0
            
            return off_count, wfh_count
        except Exception as e:
            print(f"Counter Error: {e}")
            return 0, 0

    def close(self):
        """Database connection ကို ပိတ်သည်"""
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()