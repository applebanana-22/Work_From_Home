import customtkinter as ctk
from database import Database
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

class MemberSchedule(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user  # Contains member's id, team_id, and full_name
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(header, text="My WFH/Office Schedule", 
                     font=("Arial", 22, "bold")).pack(side="left")

        # --- FILTER SECTION ---
        filter_frame = ctk.CTkFrame(self, corner_radius=10)
        filter_frame.pack(fill="x", padx=30, pady=10)
        
        # Date Range Selection
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
        
        # Load schedule for current date range on startup
        self.refresh_view()

    def refresh_view(self):
        # Clear previous entries
        for child in self.scroll.winfo_children():
            child.destroy()
        
        user_id = self.user.get('id')
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()

        # Query only for THIS specific member
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
                # Create a card for each scheduled day
                card = ctk.CTkFrame(self.scroll, fg_color=("#F0F0F0", "#252525"))
                card.pack(fill="x", pady=3, padx=10)
                
                # Format Date and Day name
                date_str = r['schedule_date'].strftime('%Y-%m-%d')
                day_name = r['schedule_date'].strftime('%A')
                
                # Styling based on status
                status = r['status']
                status_color = "#27AE60" if status == 'Office' else "#3498DB"
                
                ctk.CTkLabel(card, text=f"{date_str} ({day_name})", 
                             font=("Arial", 13)).pack(side="left", padx=20, pady=10)
                
                ctk.CTkLabel(card, text=status.upper(), text_color=status_color, 
                             font=("Arial", 13, "bold")).pack(side="right", padx=20)
                             
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load schedule: {e}")