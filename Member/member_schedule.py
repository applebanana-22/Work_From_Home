import customtkinter as ctk
from database import Database
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

class MemberSchedule(ctk.CTkFrame):
    def __init__(self, master, user):
        # Error Fix: Console မှာ error မတက်အောင် transparent အစား theme color ကို သုံးထားပါတယ်
        super().__init__(master, fg_color=("white", "#1A1A1A"))
        self.db = Database()
        self.user = user  # Contains member's id, team_id, and full_name
        self.setup_ui()
        
        # Auto Sync function ကို စတင်ခေါ်ယူခြင်း
        self.auto_refresh()

    def setup_ui(self):
        # Header (Old Design အတိုင်း "My WFH/Office Schedule")
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(header, text="My WFH/Office Schedule", 
                     font=("Arial", 22, "bold")).pack(side="left")

        # --- FILTER SECTION (Old Design) ---
        filter_frame = ctk.CTkFrame(self, corner_radius=10)
        filter_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(filter_frame, text="From:").grid(row=0, column=0, padx=(20, 5), pady=15)
        self.start_cal = DateEntry(filter_frame, width=12, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.start_cal.grid(row=0, column=1, padx=5, pady=15)

        ctk.CTkLabel(filter_frame, text="To:").grid(row=0, column=2, padx=(20, 5), pady=15)
        self.end_cal = DateEntry(filter_frame, width=12, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.end_cal.grid(row=0, column=3, padx=5, pady=15)

        # Filter Button
        ctk.CTkButton(filter_frame, text="🔍 Check My Dates", fg_color="#3498DB", width=140,
                      command=self.refresh_view).grid(row=0, column=4, padx=(30, 10), pady=15)

        # --- DISPLAY AREA ---
        self.scroll = ctk.CTkScrollableFrame(self, label_text="Scheduled Assignments")
        self.scroll.pack(fill="both", expand=True, padx=30, pady=10)
        
        self.refresh_view()

    def refresh_view(self):
        # Clear previous entries
        for child in self.scroll.winfo_children():
            child.destroy()
        
        user_id = self.user.get('id')
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()

        # Database Query
        query = """SELECT schedule_date, status 
                   FROM wfh_schedules 
                   WHERE user_id = %s AND schedule_date BETWEEN %s AND %s
                   ORDER BY schedule_date ASC"""
        
        try:
            self.db.cursor.execute(query, (user_id, start, end))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(self.scroll, text="No schedule assigned for this period.", 
                             text_color="gray").pack(pady=20)
                return

            for r in rows:
                # Old Version Design အတိုင်း Card Layout
                card = ctk.CTkFrame(self.scroll, fg_color=("#F0F0F0", "#252525"))
                card.pack(fill="x", pady=3, padx=10)
                
                date_str = r['schedule_date'].strftime('%Y-%m-%d')
                day_name = r['schedule_date'].strftime('%A')
                status = r['status']
                status_color = "#27AE60" if status == 'Office' else "#3498DB"
                
                ctk.CTkLabel(card, text=f"{date_str} ({day_name})", 
                             font=("Arial", 13)).pack(side="left", padx=20, pady=10)
                
                ctk.CTkLabel(card, text=status.upper(), text_color=status_color, 
                             font=("Arial", 13, "bold")).pack(side="right", padx=20)
                             
        except Exception as e:
            # Sync error ကို terminal မှာပဲ ပြစေခြင်းဖြင့် UI မှာ error box တွေ ခဏခဏမတက်အောင် ကာကွယ်ထားပါတယ်
            print(f"Sync error: {e}")

    def auto_refresh(self):
        """Leader ပြင်လိုက်တာနဲ့ Member ဘက်မှာ အလိုအလျောက် Update ဖြစ်စေရန်"""
        if self.winfo_exists():
            self.refresh_view()
            # စက္ကန့် ၃၀ တစ်ခါ refresh လုပ်ပါမည်
            self.after(30000, self.auto_refresh)