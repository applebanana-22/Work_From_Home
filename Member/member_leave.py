import customtkinter as ctk
from database import Database
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

class MemberLeave(ctk.CTkFrame):
    def __init__(self, master, user, sidebar_ref=None):
        # Using a tuple for dynamic background color
        super().__init__(master, fg_color=["#F2F2F2", "#121212"])
        self.db = Database()
        self.user = user
        self.sidebar_ref = sidebar_ref
        
        # Centralized theme colors for easy maintenance
        self.theme = {
            "card_bg": ["#FFFFFF", "#1E1E1E"],
            "card_border": ["#E0E0E0", "#2D2D2D"],
            "text_title": ["#1A1A1A", "#FFFFFF"],
            "text_sub": ["#666666", "#888888"],
            "input_bg": ["#EBEBEB", "#252525"],
            "accent": "#6264A7"
        }
        
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
            ctk.CTkButton(left_side, text="←", width=35, height=35, 
                          fg_color=self.theme["card_border"], 
                          text_color=self.theme["text_title"],
                          hover_color=["#D0D0D0", "#3D3D3D"], 
                          command=self.show_list_view).pack(side="left", padx=(0, 15))
            
        ctk.CTkLabel(left_side, text=title, font=("Segoe UI", 32, "bold"), 
                     text_color=self.theme["text_title"]).pack(anchor="w")
        ctk.CTkLabel(left_side, text=subtitle, font=("Segoe UI", 14), 
                     text_color=self.theme["text_sub"]).pack(anchor="w")

        if not show_back:
            ctk.CTkButton(header, text="+ New Request", font=("Segoe UI", 14, "bold"), 
                          fg_color=self.theme["accent"], hover_color="#4F5191", 
                          height=45, corner_radius=10, command=self.show_form_view).pack(side="right")

    def show_list_view(self):
        self.clear_view()
        self.create_header("Leave Dashboard", "Track your applications and response history")
        
        self.list_f = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.list_f.pack(fill="both", expand=True)
        self.refresh_list()

    def refresh_list(self):
        """Feature: Retrieve and Display Applied & Responded Times"""
        for w in self.list_f.winfo_children(): w.destroy()
        try:
            self.db.cursor.execute("""
                SELECT *, created_at, updated_at 
                FROM leave_requests 
                WHERE user_id = %s 
                ORDER BY id DESC
            """, (self.user['id'],))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(self.list_f, text="No leave requests found.", 
                             font=("Segoe UI", 14), text_color=self.theme["text_sub"]).pack(pady=60)
                return

            for r in rows:
                status = r['status']
                status_color = {"Approved": "#27AE60", "Pending": "#F39C12", "Rejected": "#E74C3C"}.get(status, "#555555")
                
                card = ctk.CTkFrame(self.list_f, fg_color=self.theme["card_bg"], 
                                   corner_radius=15, border_width=1, border_color=self.theme["card_border"])
                card.pack(fill="x", pady=8, padx=5)
                
                inner = ctk.CTkFrame(card, fg_color="transparent")
                inner.pack(fill="x", padx=20, pady=15)
                
                # --- Left Side: Leave Info ---
                info_f = ctk.CTkFrame(inner, fg_color="transparent")
                info_f.pack(side="left")
                
                ctk.CTkLabel(info_f, text=f"{r['start_date']} — {r['end_date']}", 
                             font=("Segoe UI", 16, "bold"), text_color=self.theme["text_title"]).pack(anchor="w")
                ctk.CTkLabel(info_f, text=f"{r['leave_type']} • {r['total_days']} Days ({r['shift_type']})", 
                             font=("Segoe UI", 13), text_color=self.theme["text_sub"]).pack(anchor="w")
                
                req_t = r['created_at'].strftime("%b %d, %I:%M %p") if r['created_at'] else "N/A"
                ctk.CTkLabel(info_f, text=f"🕒 Applied: {req_t}", font=("Segoe UI", 11), 
                             text_color=self.theme["text_sub"]).pack(anchor="w", pady=(5, 0))

                # --- Right Side: Status & Response Time ---
                right_f = ctk.CTkFrame(inner, fg_color="transparent")
                right_f.pack(side="right", anchor="e")

                badge = ctk.CTkFrame(right_f, fg_color=status_color, corner_radius=8)
                badge.pack(side="top", anchor="e")
                ctk.CTkLabel(badge, text=status.upper(), font=("Segoe UI", 10, "bold"), text_color="white", padx=12, pady=4).pack()

                if status != "Pending" and r.get('updated_at'):
                    res_t = r['updated_at'].strftime("%b %d, %I:%M %p")
                    ctk.CTkLabel(right_f, text=f"Responded: {res_t}", font=("Segoe UI", 11), 
                                 text_color=self.theme["text_sub"]).pack(pady=(5, 0), anchor="e")
                
        except Exception as e: print(f"List Error: {e}")

    def show_form_view(self):
        self.clear_view()
        self.create_header("Leave Request", "GIC Myanmar", show_back=True)

        form_scroll = ctk.CTkScrollableFrame(self.container, fg_color=self.theme["card_bg"], 
                                            corner_radius=20, border_width=1, border_color=self.theme["card_border"])
        form_scroll.pack(pady=10, fill="both", expand=True)

        inner = ctk.CTkFrame(form_scroll, fg_color="transparent")
        inner.pack(padx=40, pady=30, fill="x")

        # Leave Type
        ctk.CTkLabel(inner, text="SELECT LEAVE TYPE", font=("Segoe UI", 12, "bold"), text_color=self.theme["accent"]).pack(anchor="w")
        self.type_var = ctk.StringVar(value="Casual Leave")
        type_menu = ctk.CTkOptionMenu(
            inner, variable=self.type_var, 
            values=["Sick Leave", "Casual Leave", "Vacation", "Personal"], 
            fg_color=self.theme["input_bg"], 
            text_color=self.theme["text_title"],
            button_color=self.theme["accent"], 
            button_hover_color="#4F5191",
            font=("Segoe UI", 16, "bold"), height=50, corner_radius=10
        )
        type_menu.pack(fill="x", pady=(8, 25))

        # Date Selection Grid
        date_grid = ctk.CTkFrame(inner, fg_color="transparent")
        date_grid.pack(fill="x", pady=10)

        # Start Date Box
        s_box = ctk.CTkFrame(date_grid, fg_color=self.theme["input_bg"], corner_radius=12, border_width=1, border_color=self.theme["card_border"])
        s_box.pack(side="left", expand=True, fill="x", padx=(0, 10))
        s_inner = ctk.CTkFrame(s_box, fg_color="transparent")
        s_inner.pack(padx=15, pady=15, fill="both")
        ctk.CTkLabel(s_inner, text="START DATE", font=("Segoe UI", 10, "bold"), text_color=self.theme["text_sub"]).pack(anchor="w")
        
        # tkcalendar.DateEntry is not a ctk widget, so we use a fixed color or theme-dependent background
        self.start_cal = DateEntry(s_inner, background='#6264A7', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', font=("Segoe UI", 11))
        self.start_cal.pack(pady=8, fill="x")
        
        self.start_shift = ctk.CTkSegmentedButton(s_inner, values=["Full Day", "Morning", "Evening"], 
                                                  selected_color=self.theme["accent"],
                                                  command=lambda v: self.validate_and_calc())
        self.start_shift.set("Full Day")
        self.start_shift.pack(fill="x")

        # End Date Box
        e_box = ctk.CTkFrame(date_grid, fg_color=self.theme["input_bg"], corner_radius=12, border_width=1, border_color=self.theme["card_border"])
        e_box.pack(side="left", expand=True, fill="x", padx=(10, 0))
        e_inner = ctk.CTkFrame(e_box, fg_color="transparent")
        e_inner.pack(padx=15, pady=15, fill="both")
        ctk.CTkLabel(e_inner, text="END DATE", font=("Segoe UI", 10, "bold"), text_color=self.theme["text_sub"]).pack(anchor="w")
        
        self.end_cal = DateEntry(e_inner, background='#6264A7', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', font=("Segoe UI", 11))
        self.end_cal.pack(pady=8, fill="x")
        
        self.end_shift = ctk.CTkSegmentedButton(e_inner, values=["Full Day", "Morning", "Evening"], 
                                                selected_color=self.theme["accent"],
                                                command=lambda v: self.validate_and_calc())
        self.end_shift.set("Full Day")
        self.end_shift.pack(fill="x")

        self.sum_box = ctk.CTkFrame(inner, fg_color=["#F9F9F9", "#121212"], corner_radius=15, border_width=2, border_color=self.theme["accent"])
        self.sum_box.pack(fill="x", pady=25)
        self.sum_lbl = ctk.CTkLabel(self.sum_box, text="Total Duration: 0.0 Day(s)", font=("Segoe UI", 18, "bold"), text_color="#27AE60")
        self.sum_lbl.pack(pady=20)

        ctk.CTkLabel(inner, text="REASON FOR LEAVE", font=("Segoe UI", 12, "bold"), text_color=self.theme["accent"]).pack(anchor="w")
        self.reason_txt = ctk.CTkTextbox(inner, height=120, fg_color=self.theme["input_bg"], 
                                        text_color=self.theme["text_title"],
                                        border_width=1, border_color=self.theme["card_border"], 
                                        font=("Segoe UI", 15), corner_radius=10)
        self.reason_txt.pack(fill="x", pady=(8, 30))

        self.submit_btn = ctk.CTkButton(inner, text="SUBMIT LEAVE APPLICATION", fg_color="#1A73E8", height=55, font=("Segoe UI", 16, "bold"), corner_radius=12, command=self.handle_submit)
        self.submit_btn.pack(fill="x")

        self.start_cal.bind("<<DateEntrySelected>>", lambda e: self.validate_and_calc())
        self.end_cal.bind("<<DateEntrySelected>>", lambda e: self.validate_and_calc())
        self.validate_and_calc()

    # --- Backend Logic (UNCHANGED) ---
    def validate_and_calc(self):
        try:
            s_date, e_date = self.start_cal.get_date(), self.end_cal.get_date()
            s_shift, e_shift = self.start_shift.get(), self.end_shift.get()
            
            if s_date > e_date:
                self.sum_lbl.configure(text="❌ Error: Start Date is after End Date", text_color="#E74C3C")
                self.submit_btn.configure(state="disabled", fg_color="#333333")
                return

            delta_days = (e_date - s_date).days + 1
            total_days = float(delta_days)
            desc_detail = ""

            if s_date == e_date:
                if s_shift == "Full Day":
                    total_days = 1.0
                    desc_detail = "Full Day"
                elif s_shift == e_shift and s_shift != "Full Day":
                    total_days = 0.5
                    desc_detail = f"Half Day ({s_shift})"
                elif s_shift == "Morning" and e_shift == "Evening":
                    total_days = 1.0
                    desc_detail = "Full Day"
                else:
                    total_days = 0.5
                    desc_detail = f"Partial Day"
            else:
                if s_shift == "Evening": total_days -= 0.5
                if e_shift == "Morning": total_days -= 0.5
                desc_detail = f"{s_shift} to {e_shift}"

            self.sum_lbl.configure(text=f"Duration: {total_days} Day(s) ({desc_detail})", text_color="#27AE60")
            self.submit_btn.configure(state="normal", fg_color="#6264A7")
            self.final_days, self.final_shift = total_days, desc_detail
        except: pass

    def handle_submit(self):
        reason = self.reason_txt.get("1.0", "end-1c").strip()
        if not reason: return messagebox.showwarning("Warning", "Please provide a reason.")
        
        try:
            sql = """INSERT INTO leave_requests 
                     (user_id, leave_type, shift_type, start_date, end_date, total_days, reason, status, created_at, updated_at) 
                     VALUES (%s,%s,%s,%s,%s,%s,%s,'Pending', NOW(), NOW())"""
            
            self.db.cursor.execute(sql, (
                self.user['id'], self.type_var.get(), self.final_shift, 
                self.start_cal.get_date(), self.end_cal.get_date(), 
                self.final_days, reason
            ))
            req_id = self.db.cursor.lastrowid
            
            msg = f"{self.user.get('full_name', 'Employee')} requested {self.final_days} days leave."
            self.db.cursor.execute("""INSERT INTO notifications 
                                     (user_id, request_id, message, is_read, created_at) 
                                     SELECT id, %s, %s, 0, NOW() FROM users 
                                     WHERE role = 'leader' AND team_id = %s""", 
                                     (req_id, msg, self.user.get('team_id')))
            
            self.db.conn.commit()
            messagebox.showinfo("Success", "Application submitted.")
            self.show_list_view()
            if self.sidebar_ref: self.sidebar_ref.refresh_sidebar_badge()
        except Exception as e: messagebox.showerror("Error", str(e))