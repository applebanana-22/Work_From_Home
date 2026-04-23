import customtkinter as ctk
from database import Database
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

class MemberLeave(ctk.CTkFrame):
    def __init__(self, master, user, sidebar_ref=None):
        super().__init__(master, fg_color="#121212")
        self.db = Database()
        self.user = user
        self.sidebar_ref = sidebar_ref
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=30)
        
        self.show_list_view()

    def clear_view(self):
        for widget in self.container.winfo_children(): 
            widget.destroy()

    def create_header(self, title, subtitle, show_back=False):
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        left_side = ctk.CTkFrame(header, fg_color="transparent")
        left_side.pack(side="left")
        
        if show_back:
            ctk.CTkButton(left_side, text="←", width=35, height=35, fg_color="#2D2D2D", 
                          hover_color="#3D3D3D", command=self.show_list_view).pack(side="left", padx=(0, 15))
            
        ctk.CTkLabel(left_side, text=title, font=("Segoe UI", 28, "bold"), text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(left_side, text=subtitle, font=("Segoe UI", 13), text_color="#888888").pack(anchor="w")

        if not show_back:
            ctk.CTkButton(header, text="+ New Request", font=("Segoe UI", 14, "bold"), 
                          fg_color="#6264A7", hover_color="#4F5191", height=45, 
                          corner_radius=10, command=self.show_form_view).pack(side="right")

    def show_list_view(self):
        self.clear_view()
        self.create_header("Leave Dashboard", "Manage your time-off and track status")
        
        self.list_f = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.list_f.pack(fill="both", expand=True)
        self.refresh_list()

    def refresh_list(self):
        for w in self.list_f.winfo_children(): w.destroy()
        try:
            self.db.cursor.execute("SELECT * FROM leave_requests WHERE user_id = %s ORDER BY id DESC", (self.user['id'],))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(self.list_f, text="No leave requests found.", font=("Segoe UI", 14), text_color="#555555").pack(pady=60)
                return

            for r in rows:
                status = r['status']
                status_color = {"Approved": "#27AE60", "Pending": "#F39C12", "Rejected": "#E74C3C"}.get(status, "#555555")
                card = ctk.CTkFrame(self.list_f, fg_color="#1E1E1E", corner_radius=15, border_width=1, border_color="#2D2D2D")
                card.pack(fill="x", pady=8, padx=5)
                inner = ctk.CTkFrame(card, fg_color="transparent")
                inner.pack(fill="x", padx=20, pady=15)
                
                info_f = ctk.CTkFrame(inner, fg_color="transparent")
                info_f.pack(side="left")
                ctk.CTkLabel(info_f, text=f"{r['start_date']} — {r['end_date']}", font=("Segoe UI", 16, "bold"), text_color="#FFFFFF").pack(anchor="w")
                ctk.CTkLabel(info_f, text=f"{r['leave_type']} • {r['total_days']} Days ({r['shift_type']})", 
                             font=("Segoe UI", 13), text_color="#888888").pack(anchor="w")
                
                badge = ctk.CTkFrame(inner, fg_color=status_color, corner_radius=8)
                badge.pack(side="right")
                ctk.CTkLabel(badge, text=status.upper(), font=("Segoe UI", 10, "bold"), text_color="white", padx=12, pady=4).pack()
        except Exception as e: print(f"List Error: {e}")

    def show_form_view(self):
        self.clear_view()
        self.create_header("New Request", "Select dates for your leave application", show_back=True)

        # Form Scrollable ဖြစ်စေဖို့ container အသစ်သုံးပါတယ် (Screen သေးတဲ့ဖုန်း/laptop တွေမှာ အဆင်ပြေအောင်)
        form_scroll = ctk.CTkScrollableFrame(self.container, fg_color="#1E1E1E", corner_radius=20, border_width=1, border_color="#2D2D2D")
        form_scroll.pack(pady=10, fill="both", expand=True)

        inner = ctk.CTkFrame(form_scroll, fg_color="transparent")
        inner.pack(padx=30, pady=20, fill="x")

        # --- Grid for Dates ---
        grid = ctk.CTkFrame(inner, fg_color="transparent")
        grid.pack(fill="x", pady=10)

        # Start Date Section
        s_box = ctk.CTkFrame(grid, fg_color="transparent")
        s_box.pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkLabel(s_box, text="START DATE", font=("Segoe UI", 11, "bold"), text_color="#6264A7").pack(anchor="w")
        
        # Calendar ပေါ်မလာတဲ့ error အတွက် background/foreground ကို explicitly ပေးထားပါတယ်
        self.start_cal = DateEntry(s_box, background='#6264A7', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_cal.pack(pady=8, fill="x", ipady=5)
        
        self.start_shift = ctk.CTkSegmentedButton(s_box, values=["Full Day", "Evening"], command=lambda v: self.validate_and_calc())
        self.start_shift.set("Full Day")
        self.start_shift.pack(fill="x")

        # End Date Section
        e_box = ctk.CTkFrame(grid, fg_color="transparent")
        e_box.pack(side="left", expand=True, fill="x", padx=(10, 0))
        ctk.CTkLabel(e_box, text="END DATE", font=("Segoe UI", 11, "bold"), text_color="#6264A7").pack(anchor="w")
        
        self.end_cal = DateEntry(e_box, background='#6264A7', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_cal.pack(pady=8, fill="x", ipady=5)
        
        self.end_shift = ctk.CTkSegmentedButton(e_box, values=["Full Day", "Morning"], command=lambda v: self.validate_and_calc())
        self.end_shift.set("Full Day")
        self.end_shift.pack(fill="x")

        # Leave Type
        ctk.CTkLabel(inner, text="LEAVE TYPE", font=("Segoe UI", 11, "bold"), text_color="#6264A7").pack(anchor="w", pady=(20, 0))
        self.type_var = ctk.StringVar(value="Casual Leave")
        ctk.CTkOptionMenu(inner, variable=self.type_var, values=["Sick Leave", "Casual Leave", "Vacation", "Personal"], fg_color="#2D2D2D").pack(fill="x", pady=8)

        # Summary Box
        self.sum_box = ctk.CTkFrame(inner, fg_color="#121212", corner_radius=12, border_width=1, border_color="#333333")
        self.sum_box.pack(fill="x", pady=20)
        self.sum_lbl = ctk.CTkLabel(self.sum_box, text="Total Duration: 1.0 Day(s)", font=("Segoe UI", 15, "bold"))
        self.sum_lbl.pack(pady=15)

        # Reason
        ctk.CTkLabel(inner, text="REASON", font=("Segoe UI", 11, "bold"), text_color="#6264A7").pack(anchor="w")
        self.reason_txt = ctk.CTkTextbox(inner, height=100, fg_color="#121212", border_width=1, border_color="#2D2D2D")
        self.reason_txt.pack(fill="x", pady=8)

        self.submit_btn = ctk.CTkButton(inner, text="SUBMIT REQUEST", fg_color="#6264A7", height=50, font=("Segoe UI", 16, "bold"), command=self.handle_submit)
        self.submit_btn.pack(fill="x", pady=(10, 0))

        # Events
        self.start_cal.bind("<<DateEntrySelected>>", lambda e: self.validate_and_calc())
        self.end_cal.bind("<<DateEntrySelected>>", lambda e: self.validate_and_calc())
        
        # Initial calculation
        self.sidebar_ref.sidebar.after(100, self.validate_and_calc)

    def validate_and_calc(self):
        try:
            s_date = self.start_cal.get_date()
            e_date = self.end_cal.get_date()
            
            if s_date > e_date:
                self.sum_lbl.configure(text="❌ Invalid: Start Date is after End Date", text_color="#E74C3C")
                self.submit_btn.configure(state="disabled")
                return

            delta = (e_date - s_date).days + 1
            days = float(delta)
            desc_parts = []

            if s_date == e_date:
                if self.start_shift.get() == "Evening":
                    days = 0.5
                    desc_parts.append("Half Day (Evening)")
                else:
                    days = 1.0
                    desc_parts.append("Full Day")
            else:
                if self.start_shift.get() == "Evening":
                    days -= 0.5
                    desc_parts.append("Start Evening")
                if self.end_shift.get() == "Morning":
                    days -= 0.5
                    desc_parts.append("End Morning")
                
                if not desc_parts: desc_parts.append("Full Days")

            desc = f"{delta} Days" if not desc_parts else f"{delta} Days (" + ", ".join(desc_parts) + ")"
            self.sum_lbl.configure(text=f"Total Duration: {days} Day(s)\n{desc}", text_color="#27AE60")
            self.submit_btn.configure(state="normal")
            self.final_days = days
            self.final_shift = desc
        except Exception as e:
            print(f"Calc error: {e}")

    def handle_submit(self):
        reason = self.reason_txt.get("1.0", "end-1c").strip()
        if not reason: return messagebox.showwarning("Warning", "Please provide a reason.")
        
        try:
            sql = "INSERT INTO leave_requests (user_id, leave_type, shift_type, start_date, end_date, total_days, reason, status, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,'Pending', NOW())"
            self.db.cursor.execute(sql, (self.user['id'], self.type_var.get(), self.final_shift, self.start_cal.get_date(), self.end_cal.get_date(), self.final_days, reason))
            req_id = self.db.cursor.lastrowid
            
            # Leader notification
            msg = f"{self.user.get('full_name', 'Employee')} requested {self.final_days} days leave."
            self.db.cursor.execute("INSERT INTO notifications (user_id, request_id, message, is_read, created_at) SELECT id, %s, %s, 0, NOW() FROM users WHERE role = 'leader' AND team_id = %s", (req_id, msg, self.user.get('team_id')))
            
            self.db.conn.commit()
            messagebox.showinfo("Success", "Leave request submitted successfully!")
            self.show_list_view()
            
            if self.sidebar_ref:
                self.sidebar_ref.refresh_sidebar_badge()
                
        except Exception as e: messagebox.showerror("Error", str(e))