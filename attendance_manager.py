import datetime
from tkinter import messagebox

class AttendanceManager:
    def __init__(self, db, user_id):
        self.db = db
        self.user_id = user_id
        self.is_checked_in = False
        self.load_session()

    def load_session(self):
        """Database ထဲမှာ check_out မလုပ်ရသေးတဲ့ ဒီနေ့အတွက် record ကို ရှာမယ်"""
        today = datetime.date.today().strftime('%Y-%m-%d')
        try:
            query = """
                SELECT id FROM attendance 
                WHERE user_id = %s AND attendance_date = %s AND check_out IS NULL 
                LIMIT 1
            """
            self.db.cursor.execute(query, (self.user_id, today))
            result = self.db.cursor.fetchone()
            self.is_checked_in = True if result else False
        except Exception as e:
            print(f"Session Sync Error: {e}")

    def handle_toggle(self, location, callback):
        if not self.is_checked_in:
            if messagebox.askyesno("Check-in", f"Confirm Check-in at {location}?"):
                try:
                    self.db.check_in_user(self.user_id, location)
                    self.is_checked_in = True
                    callback(True)
                    messagebox.showinfo("Success", "Check-in Successful!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            if messagebox.askyesno("Check-out", "Confirm Check-out?"):
                try:
                    self.db.check_out_user(self.user_id)
                    self.is_checked_in = False
                    callback(False)
                    messagebox.showinfo("Success", "Check-out Successful!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))