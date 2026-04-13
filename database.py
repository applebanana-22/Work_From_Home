import mysql.connector
from datetime import datetime
from tkinter import messagebox

class Database:
    def __init__(self):
        try:
            # XAMPP နဲ့ ချိတ်ဆက်ရန် (Password ကို Blank ထားထားပါတယ်)
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # XAMPP default သည် password မပါပါ။ ရှိလျှင် "root" ဟု ပြန်ပြင်ပါ။
                database="wfh_system"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Successfully connected to XAMPP Database")
            
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
        """ဝန်ထမ်း Check-in ဝင်ချိန်ကို မှတ်တမ်းတင်သည်"""
        today = datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.now().strftime('%H:%M:%S')
        try:
            # Attendance record ထည့်ခြင်း
            sql_att = "INSERT INTO attendance (user_id, attendance_date, check_in, location_type) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql_att, (user_id, today, now_time, location))
            
            # User ၏ current_status ကို Update လုပ်ခြင်း
            sql_user = "UPDATE users SET current_status = %s WHERE id = %s"
            self.cursor.execute(sql_user, (location, user_id))
            
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Check-in Error: {e}")
            raise e

    def check_out_user(self, user_id):
        """နောက်ဆုံးဖွင့်ထားသော record ကို Check-out လုပ်ပြီး ပိတ်သည်"""
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
            
            # User ရဲ့ status ကို reset ပြန်လုပ်ခြင်း (NULL)
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
            
    # database.py ထဲတွင် အောက်ပါ function ကို ထပ်ဖြည့်ပါ
def update_live_status(self, user_id, status):
    """Member ၏ Live status (active, away, offline) ကို Update လုပ်ရန်"""
    try:
        query = "UPDATE users SET status = %s, last_activity = CURRENT_TIMESTAMP WHERE id = %s"
        self.cursor.execute(query, (status, user_id))
        self.conn.commit()
        return True
    except Exception as e:
        self.conn.rollback()
        print(f"Live Status Error: {e}")
        return False