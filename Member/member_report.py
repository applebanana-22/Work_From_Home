import customtkinter as ctk
import calendar
from datetime import datetime
from database import Database
from tkinter import messagebox

class MemberReportFrame(ctk.CTkFrame):
    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.db = Database()
        self.configure(fg_color="transparent")
        
        # Calendar State
        self.now = datetime.now()
        self.cur_year = self.now.year
        self.cur_month = self.now.month
        self.selected_date_str = self.now.strftime('%Y-%m-%d')
        self.cal_visible = False
        self.report_rows = []

        # Start with the History View
        self.show_history_view()

    def clear_view(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- VIEW 1: HISTORY LIST ---
    def show_history_view(self):
        self.clear_view()
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(header, text="Daily Report History", 
                     font=("Arial", 24, "bold"), text_color="#00fbff").pack(side="left")

        ctk.CTkButton(header, text="+ Add Daily Report", fg_color="#1f538d", 
                      command=self.show_form_view).pack(side="right")

        # Table Header
        list_header = ctk.CTkFrame(self, fg_color="#2b2b2b", height=40)
        list_header.pack(fill="x", padx=30, pady=(10, 0))
        ctk.CTkLabel(list_header, text="Date", width=120).pack(side="left", padx=10)
        ctk.CTkLabel(list_header, text="Category", width=150).pack(side="left", padx=10)
        ctk.CTkLabel(list_header, text="Details").pack(side="left", padx=10)

        # Scrollable List
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=25, pady=10)

        try:
            query = "SELECT * FROM daily_reports WHERE user_id = %s ORDER BY report_date DESC"
            self.db.cursor.execute(query, (self.user['id'],))
            reports = self.db.cursor.fetchall()
            for r in reports:
                row = ctk.CTkFrame(scroll, fg_color="#1e1e1e", height=45)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=str(r['report_date']), width=120, text_color="gray70").pack(side="left", padx=10)
                ctk.CTkLabel(row, text=r.get('category', 'General'), width=150, text_color="#3498DB").pack(side="left", padx=10)
                desc = (r['tasks'][:70] + '..') if len(r['tasks']) > 70 else r['tasks']
                ctk.CTkLabel(row, text=desc, anchor="w").pack(side="left", padx=10, fill="x")
        except Exception as e:
            print(f"List Error: {e}")

    # --- VIEW 2: ENTRY FORM ---
    def show_form_view(self):
        self.clear_view()
        self.report_rows = []
        
        # Back Button & Title
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkButton(top_bar, text="← Back", width=80, fg_color="#333333", 
                      command=self.show_history_view).pack(side="left")
        ctk.CTkLabel(top_bar, text="New Daily Report", font=("Arial", 22, "bold"), 
                     text_color="#00fbff").pack(side="left", padx=20)

        # Date Selection
        self.date_btn = ctk.CTkButton(self, text=f"📅 {self.selected_date_str}", 
                                      fg_color="#2b2b2b", command=self.toggle_calendar)
        self.date_btn.pack(fill="x", padx=40, pady=5)

        self.cal_frame = ctk.CTkFrame(self, fg_color="#252525", corner_radius=15)
        self.setup_calendar_ui()

        # Dynamic Section
        self.form_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", height=400)
        self.form_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.add_item_row() # Add first row

        # Controls
        ctk.CTkButton(self, text="＋ Add Category Section", fg_color="transparent", 
                      border_width=1, border_color="#10B981", text_color="#10B981", 
                      command=self.add_item_row).pack(pady=5)

        btn_f = ctk.CTkFrame(self, fg_color="transparent")
        btn_f.pack(fill="x", padx=40, pady=20)
        ctk.CTkButton(btn_f, text="Save & Submit", fg_color="#1f538d", 
                      height=45, command=self.save_all_reports).pack(fill="x")

    # --- CALENDAR & ROW LOGIC ---
    def setup_calendar_ui(self):
        nav = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        nav.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(nav, text="<", width=30, command=self.prev_month).pack(side="left")
        self.month_label = ctk.CTkLabel(nav, text="", font=("Arial", 13, "bold"))
        self.month_label.pack(side="left", expand=True)
        ctk.CTkButton(nav, text=">", width=30, command=self.next_month).pack(side="right")
        self.grid_frame = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.render_calendar()

    def render_calendar(self):
        for w in self.grid_frame.winfo_children(): w.destroy()
        self.month_label.configure(text=f"{calendar.month_name[self.cur_month]} {self.cur_year}")
        cal = calendar.monthcalendar(self.cur_year, self.cur_month)
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day != 0:
                    btn = ctk.CTkButton(self.grid_frame, text=str(day), width=35, height=35,
                                        fg_color="transparent", command=lambda d=day: self.select_day(d))
                    btn.grid(row=r, column=c, padx=2, pady=2)

    def select_day(self, day):
        self.selected_date_str = f"{self.cur_year}-{self.cur_month:02d}-{day:02d}"
        self.date_btn.configure(text=f"📅 {self.selected_date_str}")
        self.toggle_calendar()

    def prev_month(self):
        self.cur_month = 12 if self.cur_month == 1 else self.cur_month - 1
        if self.cur_month == 12: self.cur_year -= 1
        self.render_calendar()

    def next_month(self):
        self.cur_month = 1 if self.cur_month == 12 else self.cur_month + 1
        if self.cur_month == 1: self.cur_year += 1
        self.render_calendar()

    def toggle_calendar(self):
        if not self.cal_visible:
            self.cal_frame.pack(after=self.date_btn, pady=10, padx=40)
        else:
            self.cal_frame.pack_forget()
        self.cal_visible = not self.cal_visible

    def add_item_row(self):
        f = ctk.CTkFrame(self.form_scroll, fg_color="#252525", corner_radius=10)
        f.pack(fill="x", pady=8, padx=5)
        cat = ctk.CTkEntry(f, placeholder_text="Category (e.g. Japanese Class)", height=35)
        cat.pack(fill="x", padx=15, pady=(15, 5))
        desc = ctk.CTkTextbox(f, height=80, fg_color="#1e1e26")
        desc.pack(fill="x", padx=15, pady=(5, 15))
        self.report_rows.append((cat, desc))

    def save_all_reports(self):
        try:
            for cat_ent, desc_txt in self.report_rows:
                c = cat_ent.get().strip()
                d = desc_txt.get("1.0", "end-current").strip()
                if c and d:
                    q = "INSERT INTO daily_reports (user_id, report_date, tasks, category) VALUES (%s, %s, %s, %s)"
                    self.db.cursor.execute(q, (self.user['id'], self.selected_date_str, d, c))
            self.db.conn.commit()
            messagebox.showinfo("Success", "Daily report submitted successfully!")
            self.show_history_view() # Switch back to history list
        except Exception as e:
            messagebox.showerror("Error", str(e))