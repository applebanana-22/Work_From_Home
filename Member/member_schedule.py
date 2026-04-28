import customtkinter as ctk
from database import Database
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import tkinter as tk
from datetime import datetime
import calendar

# ── Reusable modern date-picker ──────────────────────────────────────────────
class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None):
        super().__init__(master, fg_color="transparent")
        self._date = initial_date or datetime.today().date()
        self._open = False
        self._callback = None

        # Apply the initial TTK style for the legacy calendar
        self.apply_calendar_style()

        self.btn = ctk.CTkButton(
            self,
            text=self._fmt(),
            width=170,
            height=36,
            corner_radius=10,
            fg_color=("#EAECEE", "#1E2A3A"),
            hover_color=("#D5D8DC", "#2C3E50"),
            border_width=1,
            border_color=("#ABB2B9", "#3D5166"),
            text_color=("#1A1A1A", "#FFFFFF"),
            anchor="w",
            command=self.toggle
        )
        self.btn.pack()

        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color=("#FFFFFF", "#141E2B"),
            corner_radius=12,
            border_width=1,
            border_color=("#ABB2B9", "#2A3A4A")
        )

        # Initialize calendar with the style name string
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
            cursor="hand2"
        )
        self.cal.pack(padx=8, pady=8)
        self.cal.bind("<<CalendarSelected>>", self._select)

        # Re-apply style whenever the widget is rendered to handle theme changes
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
        
        # Safely configure the calendar if it exists
        if hasattr(self, 'cal'):
            self.cal.configure(style="Custom.Calendar")

    def _fmt(self): return f"   📅   {self._date.strftime('%Y-%m-%d')}"

    def toggle(self):
        if self._open:
            self.panel.place_forget()
        else:
            self.panel.lift()
            self.panel.place(in_=self, x=0, y=self.btn.winfo_height() + 2)
        self._open = not self._open

    def _select(self, event):
        selected = self.cal.get_date()
        self._date = datetime.strptime(selected, "%Y-%m-%d").date()
        self.btn.configure(text=self._fmt())
        self.toggle()
        if self._callback: self._callback(self._date)

    def get_date(self): return self._date
    def set_date(self, d):
        self._date = d
        self.cal.selection_set(d)
        self.btn.configure(text=self._fmt())
    def on_change(self, callback): self._callback = callback


class MemberSchedule(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color=("white", "#1A1A1A"))
        self.db = Database()
        self.user = user
        self.setup_ui()
        self.auto_refresh()

    def setup_ui(self):
        self.wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self.wrapper.pack(fill="both", expand=True, padx=80, pady=5)

        title_row = ctk.CTkFrame(self.wrapper, fg_color="transparent")
        title_row.pack(fill="x", padx=10, pady=(14, 4))
        ctk.CTkLabel(title_row, text="🗓   My WFH/Office Schedule", font=("Arial", 22, "bold"),
                     text_color=("#1A1A1A", "#FFFFFF")).pack(side="left")

        filter_card = ctk.CTkFrame(self.wrapper, corner_radius=14, fg_color=("#F2F4F4", "#141E2B"),
                                   border_width=1, border_color=("#D5D8DC", "#253545"))
        filter_card.pack(fill="x", padx=10, pady=(4, 10))

        inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)

        def _lbl(parent, text):
            ctk.CTkLabel(parent, text=text, font=("Arial", 11),
                         text_color=("#566573", "#8899AA")).pack(side="left", padx=(0, 4))

        _lbl(inner, "From")
        self.start_cal = DatePickerButton(inner, initial_date=datetime.today().date())
        self.start_cal.pack(side="left", padx=(0, 16))
        self.start_cal.on_change(lambda _: self.refresh_view())

        _lbl(inner, "To")
        self.end_cal = DatePickerButton(inner, initial_date=datetime.today().date())
        self.end_cal.pack(side="left", padx=(0, 24))
        self.end_cal.on_change(lambda _: self.refresh_view())

        ctk.CTkButton(inner, text="🔍 Check My Dates", fg_color="#2471A3", hover_color="#1A5276",
                      width=140, corner_radius=9, font=("Arial", 12, "bold"),
                      command=self.refresh_view).pack(side="left", padx=(0, 4))

        self.scroll = ctk.CTkScrollableFrame(self.wrapper, fg_color=("#FFFFFF", "#0D1117"),
                                             corner_radius=14, border_width=1, border_color=("#D5D8DC", "#1E2A3A"))
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.refresh_view()

    def refresh_view(self):
        for child in self.scroll.winfo_children(): child.destroy()
        user_id = self.user.get('id')
        start, end = self.start_cal.get_date(), self.end_cal.get_date()

        try:
            query = """SELECT schedule_date, status FROM wfh_schedules 
                       WHERE user_id = %s AND schedule_date BETWEEN %s AND %s ORDER BY schedule_date ASC"""
            self.db.cursor.execute(query, (user_id, start, end))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(self.scroll, text="No schedule assigned for this period.", text_color="gray").pack(pady=20)
                return

            header_row = ctk.CTkFrame(self.scroll, fg_color=("#EAECEE", "#1E2731"), corner_radius=12)
            header_row.pack(fill="x", padx=15, pady=(8, 8))
            ctk.CTkLabel(header_row, text="Date", font=("Arial", 12, "bold"), text_color=("#2C3E50", "#AABBCD")).pack(side="left", padx=20, pady=12)
            ctk.CTkLabel(header_row, text="Status", font=("Arial", 12, "bold"), text_color=("#2C3E50", "#AABBCD")).pack(side="right", padx=20, pady=12)

            for r in rows:
                status_color = "#27AE60" if r['status'] == 'Office' else "#3498DB"
                row_frame = ctk.CTkFrame(self.scroll, fg_color=("#F8F9F9", "#1B2430"), corner_radius=14, 
                                         border_width=1, border_color=("#EBEDEF", "#26313F"))
                row_frame.pack(fill="x", pady=6, padx=15)

                left = ctk.CTkFrame(row_frame, fg_color="transparent")
                left.pack(side="left", fill="x", expand=True, padx=18, pady=14)
                
                ctk.CTkLabel(left, text=r['schedule_date'].strftime('%Y-%m-%d'), font=("Arial", 13, "bold"), 
                             text_color=("#1A1A1A", "white"), anchor="w").pack(fill="x")
                ctk.CTkLabel(left, text=r['schedule_date'].strftime('%A'), font=("Arial", 11), 
                             text_color=("#566573", "#AABBCD"), anchor="w").pack(fill="x", pady=(4, 0))

                ctk.CTkLabel(row_frame, text=r['status'].upper(), fg_color=status_color, text_color="white", 
                             corner_radius=10, font=("Arial", 11, "bold"), height=26, width=80).pack(side="right", padx=18, pady=16)
        except Exception as e: print(f"Sync error: {e}")

    def auto_refresh(self):
        if self.winfo_exists():
            self.refresh_view()
            self.after(30000, self.auto_refresh)