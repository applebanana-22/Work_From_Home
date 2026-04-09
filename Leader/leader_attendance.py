import customtkinter as ctk
from database import Database
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import datetime

class LeaderAttendance(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user  
        self.LATE_TIME = "09:00:00"
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(header, text="📊 Team Attendance Dashboard", 
                     font=("Arial", 24, "bold")).pack(side="left")

        # Month Filter (စာရင်းကို လအလိုက် ကြည့်နိုင်ရန်)
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", padx=30)
        
        ctk.CTkLabel(filter_frame, text="Filter Month:").pack(side="left", padx=5)
        self.month_picker = DateEntry(filter_frame, width=12, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.month_picker.pack(side="left", padx=10)
        
        ctk.CTkButton(filter_frame, text="Refresh Data", width=100, fg_color="#3498DB", 
                      command=self.load_all_members_data).pack(side="left", padx=5)

        # --- TABLE HEADER ---
        t_header = ctk.CTkFrame(self, fg_color=("#D1D1D1", "#2B2B2B"), height=40)
        t_header.pack(fill="x", padx=30, pady=(20, 0))
        
        headers = [("Member Name", 150), ("Work Days", 100), ("Leave Days", 100), ("Late Count", 100), ("Status", 120)]
        for text, width in headers:
            ctk.CTkLabel(t_header, text=text, width=width, font=("Arial", 13, "bold")).pack(side="left", padx=15)

        # --- SCROLLABLE TABLE CONTENT ---
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # ဖွင့်လိုက်တာနဲ့ Data တွေ တန်းပြရန်
        self.load_all_members_data()

    def load_all_members_data(self):
        """Team Member အားလုံးရဲ့ data ကို တစ်ခါတည်း ဆွဲထုတ်ပြီး Table ထဲပြခြင်း"""
        for child in self.scroll.winfo_children():
            child.destroy()

        sel_date = self.month_picker.get_date()
        
        # 1. ပထမဦးစွာ Team Member အားလုံးကို အရင်ယူသည်
        try:
            # Note: ဤနေရာတွင် Team ID ရှိပါက Filter လုပ်နိုင်သည်
            member_query = "SELECT id, username FROM users WHERE role = 'Member'"
            self.db.cursor.execute(member_query)
            members = self.db.cursor.fetchall()

            for member in members:
                m_id = member['id']
                m_name = member['username']

                # 2. Attendance & Late Count Query
                att_query = """SELECT COUNT(*) as work_days, 
                               SUM(CASE WHEN check_in > %s THEN 1 ELSE 0 END) as late_count 
                               FROM attendance 
                               WHERE user_id = %s AND MONTH(attendance_date) = %s AND YEAR(attendance_date) = %s"""
                
                # 3. Leave Summary Query (total_days column သစ်ကို သုံးထားသည်)
                leave_query = """SELECT SUM(total_days) as leave_sum FROM leave_requests 
                                 WHERE user_id = %s AND status = 'Approved' 
                                 AND (MONTH(start_date) = %s OR MONTH(end_date) = %s)"""

                self.db.cursor.execute(att_query, (self.LATE_TIME, m_id, sel_date.month, sel_date.year))
                att_res = self.db.cursor.fetchone()
                
                self.db.cursor.execute(leave_query, (m_id, sel_date.month, sel_date.month))
                leave_res = self.db.cursor.fetchone()

                # Data Formatting
                work_days = att_res['work_days'] or 0
                late_count = att_res['late_count'] or 0
                leave_days = leave_res['leave_sum'] if leave_res['leave_sum'] else 0.0
                
                # Table Row တစ်ခုချင်းစီ ဖန်တီးခြင်း
                row = ctk.CTkFrame(self.scroll, fg_color=("#F9F9F9", "#252525"), corner_radius=0)
                row.pack(fill="x", pady=1)

                ctk.CTkLabel(row, text=m_name, width=150, anchor="w").pack(side="left", padx=15, pady=10)
                ctk.CTkLabel(row, text=str(work_days), width=100).pack(side="left", padx=15)
                ctk.CTkLabel(row, text=f"{leave_days:g}", width=100, text_color="#3498DB").pack(side="left", padx=15)
                ctk.CTkLabel(row, text=str(late_count), width=100, text_color="#E67E22").pack(side="left", padx=15)
                
                # Simple Status Indicator
                status_text = "Active" if work_days > 0 else "No Records"
                status_clr = "#27AE60" if work_days > 0 else "gray"
                ctk.CTkLabel(row, text=status_text, width=120, text_color=status_clr, font=("Arial", 11, "bold")).pack(side="left", padx=15)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to auto-load team data: {e}")