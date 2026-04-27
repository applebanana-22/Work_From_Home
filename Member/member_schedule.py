import customtkinter as ctk
from database import Database
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import tkinter as tk
from datetime import datetime
import calendar

class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None):
        super().__init__(master, fg_color="transparent")
        self._date = initial_date or datetime.today().date()
        self._open = False
        self._callback = None

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Calendar",
            background="#1A1A1E",
            foreground="white",
            headersbackground="#16213E",
            headersforeground="#4FC3F7",
            selectbackground="#3498DB",
            selectforeground="white",
            normalbackground="#1A1A1E",
            normalforeground="#CCCCCC",
            weekendbackground="#1A1A1E",
            weekendforeground="#F39C12",
            othermonthforeground="#555555",
            bordercolor="#2A2A4A",
            relief="flat"
        )

        self.btn = ctk.CTkButton(
            self,
            text=self._fmt(),
            width=170,
            height=36,
            corner_radius=10,
            fg_color="#1E2A3A",
            hover_color="#2C3E50",
            border_width=1,
            border_color="#3D5166",
            anchor="w",
            command=self.toggle
        )
        self.btn.pack()

        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color="#141E2B",
            corner_radius=12,
            border_width=1,
            border_color="#2A3A4A"
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
            cursor="hand2"
        )
        self.cal.pack(padx=8, pady=8)
        self.cal.bind("<<CalendarSelected>>", self._select)

    def _fmt(self):
        return f"  📅  {self._date.strftime('%Y-%m-%d')}"

    def toggle(self):
        if self._open:
            self.panel.place_forget()
        else:
            self.panel.lift()
            self.panel.place(
                in_=self,
                x=0,
                y=self.btn.winfo_height() + 2
            )
        self._open = not self._open

    def _select(self, event):
        selected = self.cal.get_date()
        self._date = datetime.strptime(selected, "%Y-%m-%d").date()
        self.btn.configure(text=self._fmt())
        self.toggle()
        if self._callback:
            self._callback(self._date)

    def get_date(self):
        return self._date

    def set_date(self, d):
        self._date = d
        self.cal.selection_set(d)
        self.btn.configure(text=self._fmt())

    def on_change(self, callback):
        self._callback = callback


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
        # Main wrapper with the same page edge padding as Leader schedule
        self.wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self.wrapper.pack(fill="both", expand=True, padx=80, pady=5)

        # Header
        title_row = ctk.CTkFrame(self.wrapper, fg_color="transparent")
        title_row.pack(fill="x", padx=10, pady=(14, 4))
        ctk.CTkLabel(
            title_row,
            text="🗓  My WFH/Office Schedule",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(side="left")

        # Filter card
        filter_card = ctk.CTkFrame(
            self.wrapper,
            corner_radius=14,
            fg_color="#141E2B",
            border_width=1,
            border_color="#253545"
        )
        filter_card.pack(fill="x", padx=10, pady=(4, 10))

        inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)

        def _lbl(parent, text):
            ctk.CTkLabel(parent, text=text,
                         font=("Arial", 11),
                         text_color="#8899AA").pack(side="left", padx=(0, 4))

        _lbl(inner, "From")
        self.start_cal = DatePickerButton(inner, initial_date=datetime.today().date())
        self.start_cal.pack(side="left", padx=(0, 16))
        self.start_cal.on_change(lambda _: self.refresh_view())

        _lbl(inner, "To")
        self.end_cal = DatePickerButton(inner, initial_date=datetime.today().date())
        self.end_cal.pack(side="left", padx=(0, 24))
        self.end_cal.on_change(lambda _: self.refresh_view())

        ctk.CTkButton(
            inner,
            text="🔍 Check My Dates",
            fg_color="#2471A3",
            hover_color="#1A5276",
            width=140,
            corner_radius=9,
            font=("Arial", 12, "bold"),
            command=self.refresh_view
        ).pack(side="left", padx=(0, 4))

        # Display header
        list_header = ctk.CTkFrame(self.wrapper, fg_color="transparent")
        list_header.pack(fill="x", padx=10, pady=(4, 2))
        ctk.CTkLabel(list_header,
                     text="Scheduled Assignments",
                     font=("Arial", 14, "bold"),
                     text_color="#AABBCC").pack(side="left", padx=4)

        self.scroll = ctk.CTkScrollableFrame(
            self.wrapper,
            fg_color="#0D1117",
            corner_radius=14,
            border_width=1,
            border_color="#1E2A3A"
        )
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

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

            header_row = ctk.CTkFrame(self.scroll, fg_color=("#141E1D", "#1E2731"), corner_radius=12)
            header_row.pack(fill="x", padx=15, pady=(0, 8))
            ctk.CTkLabel(header_row, text="Date", font=("Arial", 12, "bold"), text_color="#AABBCD").pack(side="left", padx=20, pady=12)
            ctk.CTkLabel(header_row, text="Status", font=("Arial", 12, "bold"), text_color="#AABBCD").pack(side="right", padx=20, pady=12)

            for r in rows:
                date_obj = r['schedule_date']
                date_str = date_obj.strftime('%Y-%m-%d')
                day_name = date_obj.strftime('%A')
                status = r['status']
                status_color = "#27AE60" if status == 'Office' else "#3498DB"
                row_bg = ("#13181F", "#1B2430")

                row_frame = ctk.CTkFrame(self.scroll, fg_color=row_bg, corner_radius=14, border_width=1, border_color="#26313F")
                row_frame.pack(fill="x", pady=6, padx=15)

                left_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                left_frame.pack(side="left", fill="x", expand=True, padx=18, pady=14)
                ctk.CTkLabel(left_frame, text=date_str, font=("Arial", 13, "bold"), text_color="white", anchor="w").pack(fill="x")
                ctk.CTkLabel(left_frame, text=day_name, font=("Arial", 11), text_color="#AABBCD", anchor="w").pack(fill="x", pady=(4, 0))

                status_badge = ctk.CTkLabel(row_frame, text=status.upper(), fg_color=status_color, text_color="white", corner_radius=10, font=("Arial", 11, "bold"))
                status_badge.pack(side="right", padx=18, pady=16)
        except Exception as e:
            # Sync error ကို terminal မှာပဲ ပြစေခြင်းဖြင့် UI မှာ error box တွေ ခဏခဏမတက်အောင် ကာကွယ်ထားပါတယ်
            print(f"Sync error: {e}")

    def auto_refresh(self):
        """Leader ပြင်လိုက်တာနဲ့ Member ဘက်မှာ အလိုအလျောက် Update ဖြစ်စေရန်"""
        if self.winfo_exists():
            self.refresh_view()
            # စက္ကန့် ၃၀ တစ်ခါ refresh လုပ်ပါမည်
            self.after(30000, self.auto_refresh)