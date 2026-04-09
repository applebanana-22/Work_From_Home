import customtkinter as ctk
from database import Database
from tkcalendar import DateEntry
from datetime import datetime

class MemberAttendance(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color=("white", "#1A1A1A"))
        self.db = Database()
        self.user = user
        self.LATE_TIME = "09:00:00" 
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="🚪 Attendance & Work Summary", 
                     font=("Arial", 22, "bold")).pack(side="left")

        # --- FILTER & SUMMARY CARDS ---
        filter_frame = ctk.CTkFrame(self, corner_radius=15)
        filter_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(filter_frame, text="Select Month:").grid(row=0, column=0, padx=(20, 5), pady=20)
        self.month_picker = DateEntry(filter_frame, width=12, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.month_picker.grid(row=0, column=1, padx=5, pady=20)
        
        ctk.CTkButton(filter_frame, text="📊 View Data", fg_color="#3498DB", width=100,
                      command=self.load_data).grid(row=0, column=2, padx=20, pady=20)

        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=30, pady=5)
        
        self.working_lbl = self.create_stat_card("Working Days", "0", "#27AE60")
        self.leave_lbl = self.create_stat_card("Leave Days", "0", "#3498DB")
        self.late_lbl = self.create_stat_card("Late Days", "0", "#E67E22")

        # --- TABLE HEADER ---
        t_header = ctk.CTkFrame(self, fg_color=("#E0E0E0", "#2B2B2B"), height=40)
        t_header.pack(fill="x", padx=30, pady=(10, 0))
        
        ctk.CTkLabel(t_header, text="Date", width=120, font=("Arial", 12, "bold")).pack(side="left", padx=20)
        ctk.CTkLabel(t_header, text="Check-In", width=100, font=("Arial", 12, "bold")).pack(side="left", padx=30)
        ctk.CTkLabel(t_header, text="Check-Out", width=100, font=("Arial", 12, "bold")).pack(side="left", padx=30)
        ctk.CTkLabel(t_header, text="Remark", width=120, font=("Arial", 12, "bold")).pack(side="right", padx=20)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        self.load_data()

    def create_stat_card(self, title, value, color):
        card = ctk.CTkFrame(self.stats_container, corner_radius=10, width=180)
        card.pack(side="left", padx=10, fill="y")
        ctk.CTkLabel(card, text=title, font=("Arial", 11)).pack(pady=(5, 0))
        val_lbl = ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold"), text_color=color)
        val_lbl.pack(pady=(0, 5))
        return val_lbl

    def load_data(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        sel_date = self.month_picker.get_date()
        user_id = self.user.get('id')
        
        # Attendance Query
        att_query = """SELECT attendance_date, check_in, check_out FROM attendance 
                       WHERE user_id = %s AND YEAR(attendance_date) = %s AND MONTH(attendance_date) = %s
                       ORDER BY attendance_date DESC"""
        
        # စုစုပေါင်း ခွင့်ရက်အရေအတွက် (total_days) ကို ပေါင်းရန် SUM() ကို သုံးထားသည်
        leave_query = """SELECT SUM(total_days) as total_sum FROM leave_requests 
                         WHERE user_id = %s AND status = 'Approved' 
                         AND (MONTH(start_date) = %s OR MONTH(end_date) = %s)"""

        try:
            # 1. Attendance Data လုပ်ဆောင်ချက်
            self.db.cursor.execute(att_query, (user_id, sel_date.year, sel_date.month))
            att_rows = self.db.cursor.fetchall()
            
            late_count = 0
            for r in att_rows:
                check_in_val = r['check_in']
                is_late = check_in_val and str(check_in_val) > self.LATE_TIME
                if is_late: late_count += 1
                
                row = ctk.CTkFrame(self.scroll, fg_color="transparent")
                row.pack(fill="x", pady=2)
                ctk.CTkFrame(self.scroll, height=1, fg_color=("#DBDBDB", "#333333")).pack(fill="x", padx=10)

                remark = "LATE" if is_late else "ON TIME"
                remark_clr = "#E67E22" if is_late else "#27AE60"

                ctk.CTkLabel(row, text=f"{r['attendance_date']}", width=120).pack(side="left", padx=20, pady=10)
                ctk.CTkLabel(row, text=str(check_in_val) if check_in_val else "--:--", width=100).pack(side="left", padx=30)
                ctk.CTkLabel(row, text=str(r['check_out']) if r['check_out'] else "--:--", width=100).pack(side="left", padx=30)
                ctk.CTkLabel(row, text=remark, width=120, text_color=remark_clr, font=("Arial", 11, "bold")).pack(side="right", padx=20)

            # 2. Leave Summary ကို တွက်ချက်ခြင်း
            self.db.cursor.execute(leave_query, (user_id, sel_date.month, sel_date.month))
            leave_result = self.db.cursor.fetchone()
            
            # total_sum သည် NULL ဖြစ်နေနိုင်ပါက 0 ဟု သတ်မှတ်သည်
            total_leave_days = leave_result['total_sum'] if leave_result['total_sum'] is not None else 0.0

            # UI Update လုပ်ခြင်း
            self.working_lbl.configure(text=str(len(att_rows)))
            self.leave_lbl.configure(text=f"{total_leave_days:g}") # :g သုံးခြင်းက 1.50 ကို 1.5 ဟု ပြစေသည်
            self.late_lbl.configure(text=str(late_count))

        except Exception as e:
            print(f"Error loading attendance: {e}")