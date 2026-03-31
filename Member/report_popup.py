import customtkinter as ctk
import calendar
from datetime import datetime
from database import Database
from tkinter import messagebox

class ReportPopup(ctk.CTkToplevel):
    def __init__(self, user, on_save_callback, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.on_save_callback = on_save_callback
        self.db = Database()
        
        # Date Logic
        self.now = datetime.now()
        self.cur_year = self.now.year
        self.cur_month = self.now.month
        self.selected_date_str = self.now.strftime('%Y-%m-%d')

        self.title("New Daily Report")
        self.geometry("600x850")
        self.attributes("-topmost", True)
        self.configure(fg_color="#181818")

        # --- Header ---
        ctk.CTkLabel(self, text="Submit Daily Progress", font=("Arial", 20, "bold"), text_color="#00fbff").pack(pady=15)

        # --- Date Selection Header ---
        self.date_btn = ctk.CTkButton(
            self, text=f"📅 {self.selected_date_str}", font=("Arial", 14, "bold"),
            fg_color="#2b2b2b", hover_color="#3d3d3d", height=40,
            command=self.toggle_calendar
        )
        self.date_btn.pack(fill="x", padx=40, pady=5)

        # --- Custom Modern Calendar Frame (Hidden by default) ---
        self.cal_frame = ctk.CTkFrame(self, fg_color="#252525", corner_radius=15)
        # Internal Calendar UI
        self.setup_calendar_ui()

        # --- Dynamic Rows Container ---
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent", height=400)
        self.scroll_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.report_rows = [] 
        self.add_item_row()

        # Controls
        self.add_btn = ctk.CTkButton(
            self, text="＋ Add New Category Section", 
            fg_color="transparent", border_width=1, border_color="#10B981",
            text_color="#10B981", command=self.add_item_row
        )
        self.add_btn.pack(pady=5)

        btn_f = ctk.CTkFrame(self, fg_color="transparent")
        btn_f.pack(fill="x", padx=40, pady=15)

        ctk.CTkButton(btn_f, text="Cancel", fg_color="#E74C3C", command=self.destroy).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(btn_f, text="Save All", fg_color="#1f538d", command=self.save_all_reports).pack(side="right", padx=5, expand=True, fill="x")

        self.cal_visible = False

    def setup_calendar_ui(self):
        """Creates the grid for the custom calendar"""
        # Month/Year Navigation
        nav_f = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        nav_f.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(nav_f, text="<", width=30, command=self.prev_month).pack(side="left")
        self.month_label = ctk.CTkLabel(nav_f, text="", font=("Arial", 13, "bold"))
        self.month_label.pack(side="left", expand=True)
        ctk.CTkButton(nav_f, text=">", width=30, command=self.next_month).pack(side="right")

        # Weekdays Header
        days_f = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        days_f.pack(fill="x", padx=10)
        for d in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            ctk.CTkLabel(days_f, text=d, width=35, font=("Arial", 10), text_color="gray").pack(side="left", expand=True)

        # Days Grid
        self.grid_frame = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))
        self.render_calendar()

    def render_calendar(self):
        """Draws the actual day buttons"""
        for w in self.grid_frame.winfo_children(): w.destroy()
        
        self.month_label.configure(text=f"{calendar.month_name[self.cur_month]} {self.cur_year}")
        
        cal = calendar.monthcalendar(self.cur_year, self.cur_month)
        for row_idx, week in enumerate(cal):
            for col_idx, day in enumerate(week):
                if day != 0:
                    btn = ctk.CTkButton(
                        self.grid_frame, text=str(day), width=35, height=35,
                        fg_color="transparent", hover_color="#00fbff",
                        text_color="white",
                        command=lambda d=day: self.select_day(d)
                    )
                    # Highlight Today
                    if day == self.now.day and self.cur_month == self.now.month and self.cur_year == self.now.year:
                        btn.configure(border_width=1, border_color="#00fbff")
                    
                    btn.grid(row=row_idx, column=col_idx, padx=2, pady=2)

    def select_day(self, day):
        self.selected_date_str = f"{self.cur_year}-{self.cur_month:02d}-{day:02d}"
        self.date_btn.configure(text=f"📅 {self.selected_date_str}")
        self.toggle_calendar()

    def prev_month(self):
        self.cur_month -= 1
        if self.cur_month == 0:
            self.cur_month = 12
            self.cur_year -= 1
        self.render_calendar()

    def next_month(self):
        self.cur_month += 1
        if self.cur_month == 13:
            self.cur_month = 1
            self.cur_year += 1
        self.render_calendar()

    def toggle_calendar(self):
        if not self.cal_visible:
            self.cal_frame.pack(after=self.date_btn, pady=10, padx=40)
            self.cal_visible = True
        else:
            self.cal_frame.pack_forget()
            self.cal_visible = False

    def add_item_row(self):
        row_frame = ctk.CTkFrame(self.scroll_container, fg_color="#252525", corner_radius=10)
        row_frame.pack(fill="x", pady=8, padx=5)
        cat_entry = ctk.CTkEntry(row_frame, placeholder_text="Category...", height=35)
        cat_entry.pack(fill="x", padx=15, pady=(15, 5))
        desc_text = ctk.CTkTextbox(row_frame, height=80, fg_color="#1e1e26")
        desc_text.pack(fill="x", padx=15, pady=(5, 15))
        self.report_rows.append((cat_entry, desc_text))

    def save_all_reports(self):
        report_date = self.selected_date_str
        try:
            for cat_ent, desc_txt in self.report_rows:
                category = cat_ent.get().strip()
                description = desc_txt.get("1.0", "end-current").strip()
                if category and description:
                    query = "INSERT INTO daily_reports (user_id, report_date, tasks, category) VALUES (%s, %s, %s, %s)"
                    self.db.cursor.execute(query, (self.user['id'], report_date, description, category))
            self.db.conn.commit()
            messagebox.showinfo("Success", "Reports saved!")
            self.on_save_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))