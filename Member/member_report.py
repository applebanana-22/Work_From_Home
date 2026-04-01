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
        
        # State Management
        self.now = datetime.now()
        self.cur_year = self.now.year
        self.cur_month = self.now.month
        self.selected_date_str = self.now.strftime('%Y-%m-%d')
        self.cal_visible = False
        self.report_rows = []  # Stores dicts: {'container', 'cat_var', 'hour_var', 'desc_txt'}

        self.show_history_view()

    def clear_view(self):
        for widget in self.winfo_children():
            widget.destroy()

    def get_db_categories(self):
        try:
            self.db.cursor.execute("SELECT name FROM report_categories ORDER BY name ASC")
            results = self.db.cursor.fetchall()
            return [row['name'] for row in results] if results else ["General"]
        except:
            return ["General"]

    # --- 1. HISTORY VIEW (Grouped by Day) ---
    def show_history_view(self):
        self.clear_view()
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Daily Report History", font=("Arial", 24, "bold"), text_color="#00fbff").pack(side="left")
        ctk.CTkButton(header, text="+ Add Daily Report", fg_color="#1f538d", height=35, command=self.show_form_view).pack(side="right")

        list_header = ctk.CTkFrame(self, fg_color="#2b2b2b", height=40)
        list_header.pack(fill="x", padx=30, pady=(10, 0))
        ctk.CTkLabel(list_header, text="Date", width=120).pack(side="left", padx=10)
        ctk.CTkLabel(list_header, text="Total Hrs", width=100).pack(side="left", padx=10)
        ctk.CTkLabel(list_header, text="Work Summary").pack(side="left", padx=20)

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=25, pady=10)

        try:
            # SQL groups entries by date so history is clean
            query = """
                SELECT report_date, SUM(hours) as total_h, 
                GROUP_CONCAT(CONCAT('[', category, '] ', tasks) SEPARATOR ' | ') as summary 
                FROM daily_reports WHERE user_id = %s 
                GROUP BY report_date ORDER BY report_date DESC
            """
            self.db.cursor.execute(query, (self.user['id'],))
            reports = self.db.cursor.fetchall()
            for r in reports:
                row = ctk.CTkFrame(scroll, fg_color="#1e1e1e", height=45)
                row.pack(fill="x", pady=2)
                
                ctk.CTkLabel(row, text=str(r['report_date']), width=120, text_color="gray70").pack(side="left", padx=10)
                
                # Hour highlighting (Green if 8+ hours)
                h_val = float(r['total_h'])
                h_color = "#10B981" if h_val >= 8 else "#F1C40F"
                ctk.CTkLabel(row, text=f"{h_val}h", width=100, text_color=h_color, font=("Arial", 12, "bold")).pack(side="left", padx=10)
                
                txt = (r['summary'][:75] + '..') if len(r['summary']) > 75 else r['summary']
                ctk.CTkLabel(row, text=txt, anchor="w", text_color="gray60").pack(side="left", padx=20, fill="x")
        except Exception as e:
            print(f"History Error: {e}")

    # --- 2. ENTRY FORM (With Hours & Progress) ---
    def show_form_view(self):
        self.clear_view()
        self.report_rows = []
        
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=30, pady=20)
        ctk.CTkButton(top_bar, text="← Back", width=80, fg_color="#333333", command=self.show_history_view).pack(side="left")
        
        # Stats Display
        self.stats_lbl = ctk.CTkLabel(top_bar, text="Total: 0 / 8 Hours", font=("Arial", 16, "bold"), text_color="#F1C40F")
        self.stats_lbl.pack(side="right", padx=20)
        
        self.progress = ctk.CTkProgressBar(self, width=400, height=10, progress_color="#10B981")
        self.progress.set(0)
        self.progress.pack(pady=(0, 10))

        self.date_btn = ctk.CTkButton(self, text=f"📅 {self.selected_date_str}", fg_color="#2b2b2b", command=self.toggle_calendar)
        self.date_btn.pack(fill="x", padx=40, pady=5)

        self.cal_frame = ctk.CTkFrame(self, fg_color="#252525", corner_radius=15)
        self.setup_calendar_ui()

        self.form_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", height=380)
        self.form_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.add_item_row() # Initial Row

        ctk.CTkButton(self, text="＋ Add Category Section", fg_color="transparent", 
                      border_width=1, border_color="#10B981", text_color="#10B981", 
                      command=self.add_item_row).pack(pady=5)

        btn_f = ctk.CTkFrame(self, fg_color="transparent")
        btn_f.pack(fill="x", padx=40, pady=20)
        ctk.CTkButton(btn_f, text="Save & Submit Report", fg_color="#1f538d", height=45, command=self.save_all_reports).pack(fill="x")

    def update_total_hours(self, *args):
        total = 0
        for row in self.report_rows:
            try:
                val = float(row["hour_var"].get()) if row["hour_var"].get() else 0
                total += val
            except: pass
        self.stats_lbl.configure(text=f"Total: {total} / 8 Hours")
        self.progress.set(min(total / 8, 1.0))
        self.stats_lbl.configure(text_color="#10B981" if total >= 8 else "#F1C40F")

    def add_item_row(self):
        container = ctk.CTkFrame(self.form_scroll, fg_color="#252525", corner_radius=10)
        container.pack(fill="x", pady=8, padx=5)
        
        top = ctk.CTkFrame(container, fg_color="transparent")
        top.pack(fill="x", padx=15, pady=(10, 5))

        cat_var = ctk.StringVar(value="General")
        ctk.CTkOptionMenu(top, values=self.get_db_categories(), variable=cat_var, width=220, fg_color="#1e1e26", button_color="#10B981").pack(side="left")
        
        ctk.CTkLabel(top, text="Hrs:").pack(side="left", padx=(15, 5))
        hour_var = ctk.StringVar(value="0")
        hour_var.trace_add("write", self.update_total_hours)
        ctk.CTkEntry(top, textvariable=hour_var, width=55, justify="center").pack(side="left")

        # The Delete Button
        row_data = {"hour_var": hour_var, "cat_var": cat_var}
        ctk.CTkButton(top, text="✕", width=30, height=30, fg_color="#E74C3C", hover_color="#C0392B",
                      command=lambda: self.remove_item_row(container, row_data)).pack(side="right", padx=5)
        
        desc = ctk.CTkTextbox(container, height=80, fg_color="#1e1e26", border_width=1, border_color="#333333")
        desc.pack(fill="x", padx=15, pady=(5, 15))
        
        row_data["desc_txt"] = desc
        self.report_rows.append(row_data)
        self.update_total_hours()

    def remove_item_row(self, container, data):
        if len(self.report_rows) > 1:
            container.destroy()
            self.report_rows.remove(data)
            self.update_total_hours()
        else:
            messagebox.showwarning("Warning", "You need at least one report section.")

    # --- 3. SAVE TO DATABASE ---
    def save_all_reports(self):
        try:
            saved_count = 0
            for row in self.report_rows:
                tasks = row["desc_txt"].get("1.0", "end-1c").strip()
                hours = row["hour_var"].get()
                cat = row["cat_var"].get()

                if tasks and float(hours or 0) > 0:
                    q = "INSERT INTO daily_reports (user_id, report_date, tasks, category, hours) VALUES (%s, %s, %s, %s, %s)"
                    self.db.cursor.execute(q, (self.user['id'], self.selected_date_str, tasks, cat, hours))
                    saved_count += 1
            
            if saved_count > 0:
                self.db.conn.commit() # <--- THIS MUST RUN AFTER THE LOOP
                messagebox.showinfo("Success", f"Saved {saved_count} sections!")
                self.show_history_view()
            else:
                messagebox.showwarning("Empty", "Nothing to save. Check hours and tasks.")
                
        except Exception as e:
            self.db.conn.rollback() # Undo changes if there's an error
            messagebox.showerror("Database Error", f"Error: {e}")

    # --- CALENDAR METHODS ---
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