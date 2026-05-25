import customtkinter as ctk
import calendar
from datetime import datetime, timedelta
from database import Database
from tkinter import messagebox, ttk
from tkcalendar import Calendar
# --- CUSTOM MODERN DATE PICKER COMPONENT (COMPACT OPTIMIZED) ---
class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None, command=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._date = initial_date or datetime.today().date()
        self._open = False
        self._callback = command
        self.apply_calendar_style()
        self.btn = ctk.CTkButton(
            self,
            text=self._fmt(),
            width=120,
            height=32,
            corner_radius=6,
            hover_color=("#EBEBEB", "#2A2A2A"),
            border_width=1,
            fg_color=("#F9F9F9", "#1E1E1E"),
            border_color=("#DBDBDB", "#2C2C2C"),
            text_color=("black", "white"),
            anchor="w",
            font=("Segoe UI", 12),
            command=self.toggle
 
        )
 
        self.btn.pack(fill="x", expand=True)
        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color=("#FFFFFF", "#141E2B"),
            corner_radius=12,
            border_width=1,
 
            border_color=("#ABB2B9", "#2A3A4A")
 
        )
        self.cal = Calendar(
            self.panel,
            style="Custom.Calendar",
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            year=self._date.year,
            month=self._date.month,
            day=self._date.day,
            showweeknumbers=False,
            firstweekday="monday",
 
            font=("Arial", 11),
 
            cursor="hand2",
 
        )
 
        self.cal.pack(padx=8, pady=8)
        self.cal.bind("<<CalendarSelected>>", self._select)
        self.bind("<Expose>", lambda e: self.apply_calendar_style())
    def apply_calendar_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg = "#1A1A2E" if is_dark else "#FFFFFF"
        fg = "white" if is_dark else "black"
        h_bg = "#16213E" if is_dark else "#EAECEE"
        h_fg = "#4FC3F7" if is_dark else "#2471A3"
        style.configure("Custom.Calendar",
 
                        background=bg, foreground=fg,
 
                        headersbackground=h_bg, headersforeground=h_fg,
 
                        selectbackground="#3498DB", selectforeground="white",
 
                        normalbackground=bg, normalforeground=fg,
 
                        weekendbackground=bg, weekendforeground="#F39C12",
 
                        bordercolor=h_bg, relief="flat")
        if hasattr(self, 'cal'):
            try:
                self.cal.configure(style="Custom.Calendar")
            except Exception:
                pass
 
    def toggle(self):
        if self._open:
            self.panel.place_forget()
        else:
            self.panel.lift()
            self.panel.place(in_=self, x=0, y=self.btn.winfo_height() + 2)
        self._open = not self._open
    def _select(self, event):
        try:
            selected = self.cal.get_date()
            self._date = datetime.strptime(selected, "%Y-%m-%d").date()
            self.btn.configure(text=self._fmt())
            self.toggle()
            if self._callback:
                self._callback()
        except Exception as e:
            print(f"Calendar Extraction Error: {e}")
    def get_date(self):
        return self._date
    def set_date(self, d):
 
        self._date = d
 
        self.cal.selection_set(d)
 
        self.btn.configure(text=self._fmt())
 
 
 
    def _fmt(self):
 
        return f"  📅  {self._date.strftime('%Y-%m-%d')}"
 
# --- LEAVE DETAIL POPUP WINDOW CLASS ---
 
class LeaveDetailWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, request_id, leave_type, total_days, date_range, start_date, end_date, start_shift, end_shift, leader_reason=None):
 
        super().__init__(parent)
        self.title("Leave Application Detail")
        self.geometry("460x540")  
        self.resizable(False, False)
        self.update_idletasks()
 
        x = (self.winfo_screenwidth() // 2) - (460 // 2)
 
        y = (self.winfo_screenheight() // 2) - (540 // 2)
        self.geometry(f"+{x}+{y}")
        self.attributes("-topmost", True)
        self.grab_set()  
        self.db = db
        self.protocol("WM_DELETE_WINDOW", self.safe_close)
        title_lbl = ctk.CTkLabel(self, text="📋 Leave Day-by-Day Status", font=("Segoe UI", 16, "bold"))
        title_lbl.pack(pady=12)
        info_frame = ctk.CTkFrame(self, fg_color=["#EAEAEA", "#1E293B"], corner_radius=10)
        info_frame.pack(fill="x", padx=20, pady=5)
        day_word = "Day" if float(total_days) <= 1.0 else "Days"
        ctk.CTkLabel(info_frame, text=f"Type: {leave_type}", font=("Segoe UI", 13, "bold")).pack(pady=(6, 2))
        ctk.CTkLabel(info_frame, text=f"Date: {date_range}", font=("Segoe UI", 12)).pack(pady=2)
        ctk.CTkLabel(info_frame, text=f"Total: {total_days} {day_word}", font=("Segoe UI", 14, "bold"), text_color="#27AE60").pack(pady=(2, 6))
        if leader_reason and leader_reason.strip():
 
            reason_frame = ctk.CTkFrame(self, fg_color=["#FADBD8", "#78281F"], corner_radius=8, border_width=1, border_color="#E74C3C")
            reason_frame.pack(fill="x", padx=20, pady=(8, 0))
            ctk.CTkLabel(reason_frame, text=f"❌ Rejection Note: {leader_reason}",
 
                         font=("Segoe UI", 12, "italic"), text_color=["#C0392B", "#FADBD8"],
 
                         wraplength=380, justify="left").pack(padx=12, pady=6, anchor="w")
 
 
 
        self.list_frame = ctk.CTkScrollableFrame(self, width=400, height=220, label_text="Detailed Breakdown")
 
        self.list_frame.pack(padx=20, pady=12, fill="both", expand=True)
        self.load_day_details(request_id)
        close_btn = ctk.CTkButton(self, text="Close", fg_color="#E74C3C", hover_color="#C0392B",
 
                                font=("Segoe UI", 13, "bold"), height=36, command=self.safe_close)
        close_btn.pack(pady=(0, 12))
    def load_day_details(self, request_id):
        try:
            for widget in self.list_frame.winfo_children():
                widget.destroy()
            sql = "SELECT leave_date, shift_status FROM leave_details WHERE request_id = %s ORDER BY leave_date ASC"
            self.db.cursor.execute(sql, (request_id,))
            rows = self.db.cursor.fetchall()
            if not rows:
                no_data_lbl = ctk.CTkLabel(self.list_frame, text="No detailed date breakdown found.", font=("Segoe UI", 12, "italic"))
                no_data_lbl.pack(pady=20)
                return
            for row in rows:
                l_date = row['leave_date']
                date_str = l_date.strftime("%Y-%m-%d") if hasattr(l_date, 'strftime') else str(l_date)
                shift = row['shift_status']
                row_frame = ctk.CTkFrame(self.list_frame, fg_color=["#FFFFFF", "#121212"], height=38, corner_radius=6,
 
                                         border_width=1, border_color=["#E0E0E0", "#2D2D2D"])
 
                row_frame.pack(fill="x", pady=3, padx=5)
                if shift == "Morning":
 
                    icon = "☀️"
 
                    text_color = "#F39C12"
 
                elif shift == "Evening":
 
                    icon = "🌙"
 
                    text_color = "#9B59B6"
 
                else:
 
                    icon = "📅"
 
                    text_color = "#3498DB"
 
               
 
                date_lbl = ctk.CTkLabel(row_frame, text=f"  {icon}  {date_str}", font=("Segoe UI", 12, "bold"))
 
                date_lbl.pack(side="left", padx=8, pady=5)
 
               
 
                shift_lbl = ctk.CTkLabel(row_frame, text=shift, font=("Segoe UI", 11, "bold"), text_color=text_color)
 
                shift_lbl.pack(side="right", padx=12, pady=5)
 
               
 
        except Exception as e:
 
            print(f"Error loading details: {e}")
 
 
 
    def safe_close(self):
 
        self.grab_release()
 
        self.withdraw()
 
        self.after(100, self.destroy)
 
 
 
 
 
# --- MAIN MEMBER LEAVE DASHBOARD CLASS ---
 
class MemberLeave(ctk.CTkFrame):
 
    def __init__(self, master, user, sidebar_ref=None):
 
        super().__init__(master, fg_color=["#F2F2F2", "#121212"])
 
        self.db = Database()
 
        self.user = user
 
        self.sidebar_ref = sidebar_ref
 
       
 
        self.theme = {
 
            "card_bg": ["#FFFFFF", "#1E1E1E"],
 
            "card_border": ["#E0E0E0", "#2D2D2D"],
 
            "text_title": ["#1A1A1A", "#FFFFFF"],
 
            "text_sub": ["#666666", "#888888"],
 
            "input_bg": ["#EBEBEB", "#252525"],
 
            "accent1": "#2ECC71" ,
            "accent": "#3498DB"
 
        }
 
 
 
        self.leave_limits = {
 
            "Sick Leave": 7.0,
 
            "Casual Leave": 5.0,
 
            "Vacation": 10.0,
 
            "Personal": 3.0
 
        }
 
       
 
        self.container = ctk.CTkFrame(self, fg_color="transparent")
 
        self.container.pack(fill="both", expand=True, padx=120, pady=20)
 
       
 
        self.show_list_view()
 
 
 
    def clear_view(self):
 
        for widget in self.container.winfo_children():
 
            widget.destroy()
 
    def create_header(self, title, subtitle="", show_back=False):
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        if show_back:
            ctk.CTkButton(
                header,
                text="← Back",
                width=80,
                height=36,
                fg_color=("#DBDBDB", "#333333"),
                text_color=("black", "white"),
                hover_color=("#CFCFCF", "#444444"),
                font=("Arial", 12, "bold"),
                corner_radius=8,
                command=self.show_list_view
            ).pack(side="left", padx=(0, 20))

        text_f = ctk.CTkFrame(header, fg_color="transparent")
        text_f.pack(side="left", fill="y")

        ctk.CTkLabel(text_f, text=title, font=("Arial", 22, "bold"), 
                     text_color=self.theme["text_title"]).pack(anchor="w")
        
        if subtitle:
            ctk.CTkLabel(text_f, text=subtitle, font=("Arial", 12), 
                         text_color=self.theme["text_sub"]).pack(anchor="w", pady=(1, 0))

        if not show_back:
            ctk.CTkButton(
                header, 
                text="+ New Request", 
                font=("Arial", 12, "bold"),
                fg_color="#10B981", 
                hover_color="#0E9769",
                height=40, 
                corner_radius=10, 
                command=self.show_form_view
            ).pack(side="right")
 
 
 
    def show_list_view(self):
 
        self.clear_view()
 
        self.create_header("Leave Dashboard", "Track your applications and response history")
 
        self.list_f = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
 
        self.list_f.pack(fill="both", expand=True)
 
        self.refresh_list()
 
 
 
    def refresh_list(self):
 
        for w in self.list_f.winfo_children(): w.destroy()
 
        try:
 
            self.db.cursor.execute("""
 
                SELECT id, leave_type, start_date, end_date, start_shift, end_shift,
 
                       total_days, status, created_at, updated_at, leader_reason
 
                FROM leave_requests
 
                WHERE user_id = %s
 
                ORDER BY id DESC
 
            """, (self.user['id'],))
 
            rows = self.db.cursor.fetchall()
 
 
 
            if not rows:
 
                ctk.CTkLabel(self.list_f, text="No leave requests found.",
 
                             font=("Segoe UI", 13), text_color=self.theme["text_sub"]).pack(pady=40)
 
                return
 
 
 
            for r in rows:
 
                status = r['status']
 
                status_color = {"Approved": "#27AE60", "Pending": "#F39C12", "Rejected": "#E74C3C"}.get(status, "#555555")
 
               
 
                card = ctk.CTkFrame(self.list_f, fg_color=self.theme["card_bg"],
 
                                    corner_radius=12, border_width=1, border_color=self.theme["card_border"])
 
                card.pack(fill="x", pady=6, padx=5)
 
                card.configure(cursor="hand2")
 
               
 
                inner = ctk.CTkFrame(card, fg_color="transparent")
 
                inner.pack(fill="x", padx=15, pady=10)
 
               
 
                info_f = ctk.CTkFrame(inner, fg_color="transparent")
 
                info_f.pack(side="left", fill="x", expand=True)
 
               
 
                date_range_str = f"{r['start_date']} — {r['end_date']}"
 
                ctk.CTkLabel(info_f, text=date_range_str,
 
                             font=("Segoe UI", 14, "bold"), text_color=self.theme["text_title"]).pack(anchor="w")
 
               
 
                display_day_word = "Day" if float(r['total_days']) <= 1.0 else "Days"
 
                shift_display = f"{r['start_shift']} to {r['end_shift']}" if r['start_shift'] != r['end_shift'] else r['start_shift']
 
               
 
                ctk.CTkLabel(info_f, text=f"{r['leave_type']} • {r['total_days']} {display_day_word} ({shift_display})",
 
                             font=("Segoe UI", 12), text_color=self.theme["text_sub"]).pack(anchor="w")
 
               
 
                if status == "Rejected" and r.get('leader_reason'):
 
                    ctk.CTkLabel(info_f, text=f"❌ Reason: {r['leader_reason']}",
 
                                 font=("Segoe UI", 11, "bold", "italic"), text_color="#E74C3C",
 
                                 wraplength=450, justify="left").pack(anchor="w", pady=(2, 0))
 
               
 
                req_t = r['created_at'].strftime("%b %d, %I:%M %p") if r['created_at'] else "N/A"
 
                ctk.CTkLabel(info_f, text=f"🕒 Applied: {req_t}", font=("Segoe UI", 11),
 
                             text_color=self.theme["text_sub"]).pack(anchor="w", pady=(4, 0))
 
 
 
                right_f = ctk.CTkFrame(inner, fg_color="transparent")
 
                right_f.pack(side="right", anchor="e")
 
 
 
                badge = ctk.CTkFrame(right_f, fg_color=status_color, corner_radius=6)
 
                badge.pack(side="top", anchor="e")
 
                ctk.CTkLabel(badge, text=status.upper(), font=("Segoe UI", 9, "bold"), text_color="white", padx=10, pady=3).pack()
 
 
 
                if status != "Pending" and r.get('updated_at'):
 
                    res_t = r['updated_at'].strftime("%b %d, %I:%M %p")
 
                    ctk.CTkLabel(right_f, text=f"Responded: {res_t}", font=("Segoe UI", 11),
 
                                 text_color=self.theme["text_sub"]).pack(pady=(4, 0), anchor="e")
 
               
 
                for widget in [card, inner, info_f]:
 
                    widget.bind("<Button-1>", lambda event, arg_id=r['id'], l_type=r['leave_type'], t_days=r['total_days'],
 
                                                   d_range=date_range_str, s_d=r['start_date'], e_d=r['end_date'],
 
                                                   s_s=r['start_shift'], e_s=r['end_shift'], r_reason=r['leader_reason']:
 
                                self.open_detail_window(arg_id, l_type, t_days, d_range, s_d, e_d, s_s, e_s, r_reason))
 
               
 
        except Exception as e:
 
            print(f"List Refresh Error: {e}")
 
 
 
    def open_detail_window(self, request_id, leave_type, total_days, date_range, start_date, end_date, start_shift, end_shift, leader_reason=None):
 
        LeaveDetailWindow(self, self.db, request_id, leave_type, total_days, date_range, start_date, end_date, start_shift, end_shift, leader_reason)
 
 
 
    # 🛠️ REWRITE: Form Design ကို ကျစ်လျစ်သိပ်သည်းပြီး နေရာချွေတာနိုင်မည့် Modern Responsive အဖြစ် ပြောင်းလဲထားသော အပိုင်း
 
    # 🛠️ REWRITE: Form Design ကို ကျစ်လျစ်သိပ်သည်းပြီး နေရာချွေတာနိုင်မည့် Modern Responsive အဖြစ် ပြောင်းလဲထားသော အပိုင်း
 
    def show_form_view(self):
        self.clear_view()
        self.create_header("Leave Request", "", show_back=True)
        # Outer Base Frame
        form_scroll = ctk.CTkFrame(self.container, fg_color=self.theme["card_bg"],
 
                                   corner_radius=16, border_width=1, border_color=self.theme["card_border"])
        form_scroll.pack(pady=5, fill="both", expand=True)
        inner = ctk.CTkFrame(form_scroll, fg_color="transparent")
 
        inner.pack(padx=25, pady=15, fill="both", expand=True) # Padding ကို ပိုကျစ်အောင် ၂၀ မှ ၁၅ သို့ လျှော့ချထားသည်
     
        # 1. Row - Leave Type Section (Modern Compact OptionMenu)
        ctk.CTkLabel(inner, text="SELECT LEAVE TYPE", font=("Segoe UI", 10, "bold"), text_color=self.theme["accent"]).pack(anchor="w")
        self.type_var = ctk.StringVar(value="Casual Leave")
        type_menu = ctk.CTkOptionMenu(
            inner,
            variable=self.type_var,
            values=["Sick Leave", "Casual Leave", "Vacation", "Personal"],
            fg_color=self.theme["input_bg"],
            height=32,
            text_color=self.theme["text_title"],
            button_color=self.theme["input_bg"],
            button_hover_color=self.theme["card_border"],
            dropdown_fg_color=self.theme["input_bg"],
            dropdown_text_color=self.theme["text_title"],
            dropdown_hover_color=self.theme["accent"],
            font=("Segoe UI", 12),                     # Compact ဖြစ်စေရန် Font size ကို ၁၂ သို့ လျှော့ချထားသည်                              # Small Button တည်ဆောက်ပုံစံအတိုင်း အမြင့် ၃၂ သို့ ညှိထားသည်
            corner_radius=6
 
        )
 
        type_menu.pack(fill="x", pady=(2,12))  
       
        # 2. Row - TWO COLUMN RESPONSIVE GRID (ဘေးချင်းယှဉ် Date Fields)
        date_grid = ctk.CTkFrame(inner, fg_color="transparent")
        date_grid.pack(fill="x", pady=0)
        # --- LEFT COLUMN: FromE BLOCK ---
        s_box = ctk.CTkFrame(date_grid, fg_color=self.theme["input_bg"], corner_radius=10, border_width=1, border_color=self.theme["card_border"])
        s_box.pack(side="left", expand=True, fill="x", padx=(0, 6))
        s_inner = ctk.CTkFrame(s_box, fg_color="transparent")
        s_inner.pack(padx=10, pady=10, fill="both")
        ctk.CTkLabel(s_inner, text="From", font=("Segoe UI", 10, "bold"), text_color=self.theme["text_sub"]).pack(anchor="w")
 
        self.start_cal = DatePickerButton(s_inner, command=self.validate_and_calc)
 
        self.start_cal.pack(pady=5, fill="x")
 
       
 
        self.start_shift = ctk.CTkSegmentedButton(s_inner, values=["Full Day", "Morning", "Evening"],
 
                                                  font=("Segoe UI", 11), height=28,
 
                                                  selected_color=self.theme["accent"],
 
                                                  command=lambda v: self.validate_and_calc())
 
        self.start_shift.set("Full Day")
 
        self.start_shift.pack(fill="x")
 
 
 
        # --- RIGHT COLUMN: To BLOCK ---
 
        e_box = ctk.CTkFrame(date_grid, fg_color=self.theme["input_bg"], corner_radius=10, border_width=1, border_color=self.theme["card_border"])
 
        e_box.pack(side="left", expand=True, fill="x", padx=(6, 0))
 
       
 
        e_inner = ctk.CTkFrame(e_box, fg_color="transparent")
 
        e_inner.pack(padx=10, pady=10, fill="both")
 
       
 
        ctk.CTkLabel(e_inner, text="To", font=("Segoe UI", 10, "bold"), text_color=self.theme["text_sub"]).pack(anchor="w")
 
        self.end_cal = DatePickerButton(e_inner, command=self.validate_and_calc)
 
        self.end_cal.pack(pady=5, fill="x")
 
       
 
        self.end_shift = ctk.CTkSegmentedButton(e_inner, values=["Full Day", "Morning", "Evening"],
 
                                                font=("Segoe UI", 11), height=28,
 
                                                selected_color=self.theme["accent"],
 
                                                command=lambda v: self.validate_and_calc())
 
        self.end_shift.set("Full Day")
 
        self.end_shift.pack(fill="x")
 
 
 
        # 3. Row - Reason For Leave Section (Optimized Compact Textbox)
 
        ctk.CTkLabel(inner, text="REASON FOR LEAVE", font=("Segoe UI", 10, "bold"), text_color=self.theme["accent"]).pack(anchor="w", pady=(12, 0))
 
        self.reason_txt = ctk.CTkTextbox(inner,
 
                                         height=55,                            # စာကြောင်းရေ ၂ ကြောင်း/၃ ကြောင်းစာ ကွက်တိဖြစ်မည့် Compact အမြင့်
 
                                         fg_color=self.theme["input_bg"],
 
                                         text_color=self.theme["text_title"],
 
                                         border_width=1,
 
                                         border_color=self.theme["card_border"],
 
                                         font=("Segoe UI", 12),                # OptionMenu စာသားစိုက်အတိုင်း ညှိထားသည်
 
                                         corner_radius=6)
 
        self.reason_txt.pack(fill="x", pady=(2, 12))
 
 
 
        # 4. Row - Total Duration Summary Box
 
        self.sum_box = ctk.CTkFrame(inner, fg_color=["#F9F9F9", "#121212"], corner_radius=10, border_width=1, border_color=self.theme["accent"])
 
        self.sum_box.pack(fill="x", pady=(0, 12))
 
        self.sum_lbl = ctk.CTkLabel(self.sum_box, text="Total Duration: 0.0 Day(s)", font=("Segoe UI", 13, "bold"), text_color="#27AE60")
 
        self.sum_lbl.pack(pady=8)
 
 
 
        # 5. Row - ✨ MODERN COMPACT SUBMIT BUTTON AREA (Small Size Design)
 
        btn_container = ctk.CTkFrame(inner, fg_color="transparent")
 
        btn_container.pack(fill="x", pady=(2, 0))
 
 
 
        self.submit_btn = ctk.CTkButton(
 
            btn_container,
 
            text="SUBMIT",
 
            fg_color="#0078D4",
 
            hover_color="#005A9E",        
 
            width=140,                           # ပိုမိုကျစ်လျစ်သွားစေရန် width ကို ၁၆၀ မှ ၁၄၀ သို့ လျှော့ချထားသည်
 
            height=32,                           # အခြား Field များနည်းတူ Small Height ၃၂ သို့ သတ်မှတ်ထားသည်
 
            font=("Segoe UI", 11, "bold"),       # စာသားမကြီးလွန်းအောင် Font size ၁၁ ထားရှိပါသည်
 
            corner_radius=6,                     # တူညီသော corner roundness ကို သုံးထားသည်
 
            command=self.handle_submit,
 
            text_color="white"
 
        )
 
        self.submit_btn.pack(side="right")       # ညာဘက်သို့ ကပ်ရပ်နေရာချထားသည်
 
 
 
        self.validate_and_calc()
 
 
 
    def validate_and_calc(self):
 
        try:
 
            s_date = self.start_cal.get_date()
 
            e_date = self.end_cal.get_date()
 
            s_shift = self.start_shift.get()
 
            e_shift = self.end_shift.get()
 
            selected_type = self.type_var.get()
 
            today = datetime.now().date()
 
 
 
            if s_date < today:
 
                self.sum_lbl.configure(text="❌ Error: Cannot request past dates", text_color="#E74C3C")
 
                self.submit_btn.configure(state="disabled", fg_color="#333333")
 
                return
 
            if s_date > e_date:
 
                self.sum_lbl.configure(text="❌ Error: Frome after To", text_color="#E74C3C")
 
                self.submit_btn.configure(state="disabled", fg_color="#333333")
 
                return
 
            if s_date == e_date and s_shift == "Evening" and e_shift == "Morning":
 
                self.sum_lbl.configure(text="❌ Invalid: Evening to Morning on same day", text_color="#E74C3C")
 
                self.submit_btn.configure(state="disabled", fg_color="#333333")
 
                return
 
 
 
            sql = """SELECT id FROM leave_requests
 
                    WHERE user_id = %s AND status != 'Rejected'
 
                    AND (start_date <= %s AND end_date >= %s)"""
 
            self.db.cursor.execute(sql, (self.user['id'], e_date, s_date))
 
            if self.db.cursor.fetchone():
 
                self.sum_lbl.configure(text="❌ Error: Date overlap found", text_color="#E74C3C")
 
                self.submit_btn.configure(state="disabled", fg_color="#333333")
 
                return
 
 
 
            official_holidays = ["2026-01-01", "2026-05-01", "2026-07-19", "2026-12-25"]
 
           
 
            self.working_days_list = []
 
            self.day_breakdown_logic = {}  
 
           
 
            loop_date = s_date
 
            while loop_date <= e_date:
 
                is_weekend = loop_date.weekday() in [5, 6]
 
                is_holiday = loop_date.strftime("%Y-%m-%d") in official_holidays
 
               
 
                if not is_weekend and not is_holiday:
 
                    self.working_days_list.append(loop_date)
 
                    self.day_breakdown_logic[loop_date] = "Full Day"
 
                loop_date += timedelta(days=1)
 
 
 
            if not self.working_days_list:
 
                self.sum_lbl.configure(text="❌ Error: Selected dates are Weekends/Holidays", text_color="#E74C3C")
 
                self.submit_btn.configure(state="disabled", fg_color="#333333")
 
                return
 
 
 
            total_days = float(len(self.working_days_list))
 
 
 
            if s_date == e_date:
 
                if s_shift == "Full Day":
 
                    total_days = 1.0
 
                    shift_status = "Full Day"
 
                elif s_shift == e_shift:
 
                    total_days = 0.5
 
                    shift_status = s_shift
 
                else:
 
                    total_days = 1.0
 
                    shift_status = "Full Day"
 
                self.day_breakdown_logic[s_date] = shift_status
 
            else:
 
                if s_date in self.working_days_list:
 
                    if s_shift == "Evening":
 
                        total_days -= 0.5
 
                        self.day_breakdown_logic[s_date] = "Evening"
 
                    elif s_shift == "Morning":
 
                        self.day_breakdown_logic[s_date] = "Full Day"
 
                if e_date in self.working_days_list:
 
                    if e_shift == "Morning":
 
                        total_days -= 0.5
 
                        self.day_breakdown_logic[e_date] = "Morning"
 
                    elif e_shift == "Evening":
 
                        self.day_breakdown_logic[e_date] = "Full Day"
 
 
 
            if total_days <= 0:
 
                self.sum_lbl.configure(text="❌ Error: Total leave days cannot be 0", text_color="#E74C3C")
 
                self.submit_btn.configure(state="disabled", fg_color="#333333")
 
                return
 
 
 
            self.final_days = total_days
 
 
 
            sql_reject_check = """SELECT start_date, end_date, total_days FROM leave_requests
 
                                  WHERE user_id = %s AND status = 'Rejected'
 
                                  AND (start_date <= %s AND end_date >= %s)"""
 
            self.db.cursor.execute(sql_reject_check, (self.user['id'], e_date, s_date))
 
            rejected_record = self.db.cursor.fetchone()
 
 
 
            if rejected_record:
 
                if total_days >= float(rejected_record['total_days']):
 
                    self.sum_lbl.configure(text="❌ Error: This duration was previously Rejected. Cannot re-apply.", text_color="#E74C3C")
 
                    self.submit_btn.configure(state="disabled", fg_color="#333333")
 
                    return
 
                else:
 
                    warning_msg = f"⚠️ Reduced days from previously rejected period."
 
                    self.sum_lbl.configure(text=warning_msg, text_color="#E67E22")
 
                    self.submit_btn.configure(state="normal", fg_color="#E67E22")
 
                    self.is_exceeded = True
 
                    return
 
 
 
            day_word = "Day" if total_days <= 1.0 else "Days"
 
            max_limit = self.leave_limits.get(selected_type, 30.0)
 
           
 
            if total_days > max_limit:
 
                warning_msg = f"⚠️ Warning: {selected_type} exceeds limit! (Max: {int(max_limit)} {day_word})"
 
                self.sum_lbl.configure(text=warning_msg, text_color="#E67E22")
 
                self.submit_btn.configure(state="normal", fg_color="#E67E22")
 
                self.is_exceeded = True
 
            else:
 
                self.sum_lbl.configure(text=f"Duration: {total_days} {day_word} [Valid]", text_color="#27AE60")
 
                self.submit_btn.configure(state="normal", fg_color="#0078D4")
 
                self.is_exceeded = False
 
 
 
        except Exception as e:
 
            print(f"Calc Error: {e}")
 
 
 
    def handle_submit(self):
        reason = self.reason_txt.get("1.0", "end-1c").strip()
        if not reason:
            self._show_message("Please provide a reason.", message_type="warning")
            return
 
        if getattr(self, 'is_exceeded', False):
            # Kept standard askyesno since notifications don't handle user choice input
            confirm = messagebox.askyesno(
                "Confirm Special Request",
                "Your requested days exceed the standard limit or contain special conditions. Do you still want to submit?"
            )
            if not confirm:
                return
 
        try:
            sql = """INSERT INTO leave_requests
                    (user_id, leave_type, start_shift, end_shift, start_date, end_date,
                    total_days, reason, status, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending', NOW(), NOW())"""
           
            self.db.cursor.execute(sql, (
                self.user['id'], self.type_var.get(),
                self.start_shift.get(), self.end_shift.get(),
                self.start_cal.get_date(), self.end_cal.get_date(),
                self.final_days, reason
            ))
           
            req_id = self.db.cursor.lastrowid
           
            detail_sql = "INSERT INTO leave_details (request_id, leave_date, shift_status) VALUES (%s, %s, %s)"
            for l_date, shift_status in self.day_breakdown_logic.items():
                self.db.cursor.execute(detail_sql, (req_id, l_date, shift_status))
           
            display_day_word = "day" if self.final_days <= 1.0 else "days"
            if getattr(self, 'is_exceeded', False):
                msg = f"⚠️ [EXCEEDED LIMIT] {self.user.get('full_name')} requested {self.final_days} {display_day_word} of {self.type_var.get()}."
            else:
                msg = f"📅 {self.user.get('full_name')} requested {self.final_days} {display_day_word} leave."
               
            self.db.cursor.execute("""INSERT INTO notifications
                                    (user_id, request_id, message, is_read, created_at)
                                    SELECT id, %s, %s, 0, NOW() FROM users
                                    WHERE role = 'leader' AND team_id = %s""",
                                (req_id, msg, self.user.get('team_id')))
           
            self.db.conn.commit()
            self.day_breakdown_logic.clear()
           
            # Success condition integrated here
            self._show_message("Member Leave Request Submitted Successfully.", message_type="success")
           
            self.show_list_view()
            if self.sidebar_ref:
                self.sidebar_ref.refresh_sidebar_badge()
               
        except Exception as e:
            self._show_message(f"Submission Error: {e}", message_type="error")
 
 
 
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
            self.winfo_toplevel(),
            fg_color=bg_color,
            corner_radius=8
        )
        message_frame.place(relx=1.0, rely=0, x=-20, y=20, anchor="ne")
 
        ctk.CTkLabel(
            message_frame,
            text=message,
            text_color="white",
            font=("Arial", 12, "bold"),
            wraplength=250
        ).pack(padx=15, pady=10)
 
        self.after(duration, message_frame.destroy)
           
# --- MEMBER REPORT MANAGEMENT FRAME CLASS ---
 
class MemberReportFrame(ctk.CTkFrame):
 
    def __init__(self, master, user, **kwargs):
 
        super().__init__(master, **kwargs)
 
        self.user = user
 
        self.db = Database()
 
        self.configure(fg_color="transparent")
 
       
 
        self.now = datetime.now()
 
        self.report_rows = []
 
 
 
        today = datetime.today().date()
 
        self.start_date = datetime(today.year, today.month, 1).date()
 
        self.end_date = today
 
 
 
        self.COLOR_CARD_BG = ("#FFFFFF", "#1E1E1E")
 
        self.COLOR_BORDER = ("#DBDBDB", "#2C2C2C")
 
        self.COLOR_TEXT_MAIN = ("#1A1A1A", "#E8EDF2")
 
        self.COLOR_TEXT_SEC = ("#555555", "#AAB7C4")
 
        self.COLOR_TEXT_TER = ("#777777", "#718096")
 
        self.COLOR_SCROLL_BG = ("#F5F5F5", "#1A1A1A")
 
        self.COLOR_CONTAINER_BG = ("#F0F0F0", "#252525")
 
 
 
        self.show_history_view()
 
 
 
    def clear_view(self):
 
        for widget in self.winfo_children():
 
            widget.destroy()
 
 
 
    def get_db_categories(self):
 
        try:
 
            self.db.cursor.execute("SELECT name FROM report_categories ORDER BY name ASC")
 
            results = self.db.cursor.fetchall()
 
            return [row['name'] for row in results] if results else ["General"]
 
        except Exception as e:
 
            print(f"Error fetching categories: {e}")
 
            return ["General"]
    def show_history_view(self):
 
        self.clear_view()