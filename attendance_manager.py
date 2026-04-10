import datetime
from tkinter import messagebox

class AttendanceManager:
    def __init__(self, db, user_id, user_role):
        self.db = db
        self.user_id = user_id
        self.user_role = user_role.lower()
        self.last_sync_date = datetime.date.today() # လက်ရှိရက်စွဲကို မှတ်ထားမည်
        self.is_checked_in = False
        self.load_session()

    def check_midnight_reset(self):
        """ရက်စွဲပြောင်းသွားခြင်း ရှိမရှိ စစ်ဆေးပြီး လိုအပ်ပါက status reset လုပ်သည်"""
        current_date = datetime.date.today()
        if current_date > self.last_sync_date:
            self.last_sync_date = current_date
            self.is_checked_in = False # ရက်သစ်ကူးသဖြင့် status ကို reset ချသည်
            return True
        return False

    def load_session(self):
        """App ဖွင့်ချိန်တွင် ယနေ့အတွက် session ရှိမရှိ စစ်သည်"""
        today = datetime.date.today().strftime('%Y-%m-%d')
        try:
            query = """
                SELECT id FROM attendance 
                WHERE user_id = %s AND attendance_date = %s AND check_out IS NULL 
                ORDER BY id DESC LIMIT 1
            """
            self.db.cursor.execute(query, (self.user_id, today))
            result = self.db.cursor.fetchone()
            self.is_checked_in = True if result else False
        except Exception as e:
            print(f"Session Sync Error: {e}")

    def handle_toggle(self, location, callback):
        # 🔥 Action မလုပ်ခင် ရက်စွဲပြောင်းသွားသလား အမြဲစစ်မည်
        if self.check_midnight_reset():
            callback(False) # UI ကို Check-in button ပြန်ပြောင်းခိုင်းမည်

        if not self.is_checked_in:
            # Check if already completed for the CURRENT date
            if self.check_if_already_completed():
                messagebox.showwarning("ယနေ့အတွက် ကန့်သတ်ချက်", 
                    "ယနေ့အတွက် တစ်ကြိမ် Check-in/out လုပ်ပြီးဖြစ်၍ နောက်တစ်ကြိမ် ထပ်မံလုပ်ဆောင်၍ မရနိုင်ပါ။")
                return

            if messagebox.askyesno("Check-in", f"Confirm Check-in at {location}?"):
                try:
                    self.db.check_in_user(self.user_id, location)
                    self.is_checked_in = True
                    callback(True)
                    messagebox.showinfo("Success", "Check-in Successful!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            # Check-out logic stays same
            if messagebox.askyesno("Check-out", "Confirm Check-out?"):
                try:
                    self.db.check_out_user(self.user_id)
                    self.is_checked_in = False
                    callback(False)
                    messagebox.showinfo("Success", "Check-out Successful!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def check_if_already_completed(self):
        today = datetime.date.today().strftime('%Y-%m-%d')
        try:
            query = "SELECT id FROM attendance WHERE user_id = %s AND attendance_date = %s AND check_out IS NOT NULL"
            self.db.cursor.execute(query, (self.user_id, today))
            return True if self.db.cursor.fetchone() else False
        except:
            return False