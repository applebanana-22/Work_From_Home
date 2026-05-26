import datetime
from tkinter import messagebox
import customtkinter as ctk

class AttendanceManager:
    def __init__(self, parent, db, user_id, user_role):
        self.parent = parent
        self.db = db
        self.user_id = user_id
        self.user_role = user_role.lower()
        self.last_sync_date = datetime.date.today() # Sync date for midnight reset
        self.is_checked_in = False
        self.load_session()

    def check_midnight_reset(self):
        """This method checks if the date has changed since the last sync. If it has, it resets the check-in status for the new day."""
        current_date = datetime.date.today()
        if current_date > self.last_sync_date:
            self.last_sync_date = current_date
            self.is_checked_in = False # Reset check-in status for the new day
            return True
        return False

    def load_session(self):
        """On app start, check if the user has an active session for today. This ensures that if the app is closed and reopened, the check-in status is retained correctly."""
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
        # 🔥 Always check whether the date has changed before taking action.
        if self.check_midnight_reset():
            callback(False) # Reset UI to reflect new day status

        if not self.is_checked_in:
            # Check if already completed for the CURRENT date
            if self.check_if_already_completed():
                self._show_message("Limit for Today,You have already checked in/out for today and cannot do it again.","warning")
                return

            if messagebox.askyesno("Check-in", f"Confirm Check-in at {location}?"):
                try:
                    self.db.check_in_user(self.user_id, location)
                    self.is_checked_in = True
                    callback(True)
                    self._show_message("Check-in Successful!", "success")
                except Exception as e:
                    self._show_message("Check-in Failed!", "error")
        else:
            # Check-out logic stays same
            if messagebox.askyesno("Check-out", "Confirm Check-out?"):
                try:
                    self.db.check_out_user(self.user_id)
                    self.is_checked_in = False
                    callback(False)
                    self._show_message("Check-out Successful!", "success")
                except Exception as e:
                    self._show_message("Check-out Failed!", "error")

    def check_if_already_completed(self):
        today = datetime.date.today().strftime('%Y-%m-%d')
        try:
            query = "SELECT id FROM attendance WHERE user_id = %s AND attendance_date = %s AND check_out IS NOT NULL"
            self.db.cursor.execute(query, (self.user_id, today))
            return True if self.db.cursor.fetchone() else False
        except:
            return False

    def _show_message(self, message, message_type="info", duration=3000):
        if message_type == "error":
            bg_color = "#E74C3C"
        elif message_type == "warning":
            bg_color = "#F39C12"
        elif message_type == "success":
            bg_color = "#27AE60"
        else:
            bg_color = "#3498DB"
 
        message_frame = ctk.CTkFrame(
            self.parent.winfo_toplevel(),
            fg_color=bg_color,
            corner_radius=10
        )
        # Placed below the 65px header for better visibility
        message_frame.place(relx=1.0, rely=0, x=-20, y=20, anchor="ne")
 
        ctk.CTkLabel(
            message_frame,
            text=message,
            text_color="white",
            font=("Segoe UI", 13, "bold"),
            wraplength=280
        ).pack(padx=20, pady=12)
 
        self.parent.after(duration, message_frame.destroy)