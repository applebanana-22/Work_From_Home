import customtkinter as ctk
from database import Database
from tkinter import messagebox
from datetime import datetime
import calendar

class LeaderReportView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.db = Database()
        self.configure(fg_color="transparent")

        # --- Filter & Calendar State ---
        self.now = datetime.now()
        self.cur_year = self.now.year
        self.cur_month = self.now.month
        self.filter_date_str = self.now.strftime('%Y-%m-%d')
        self.cal_visible = False

        # Main Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Create Calendar Frame here so it's a child of the main view, not the header
        self.cal_frame = ctk.CTkFrame(self, fg_color="#252525", corner_radius=15, border_width=2, border_color="#333333")

        self.show_reports_list()

    def clear_container(self):
        """Clears UI for switching views"""
        for widget in self.container.winfo_children():
            widget.destroy()
        if self.cal_visible:
            self.toggle_filter_calendar()

    # --- VIEW 1: GROUPED REPORT LIST ---
    def show_reports_list(self):
        self.clear_container()

        # Header Section
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(header, text="Team Daily Progress", 
                     font=("Arial", 24, "bold"), text_color="#00fbff").pack(side="left")

        # Date Filter Button
        self.date_btn = ctk.CTkButton(header, text=f"📅 {self.filter_date_str}", 
                                      fg_color="#2b2b2b", width=150, height=35,
                                      command=self.toggle_filter_calendar)
        self.date_btn.pack(side="right", padx=10)

        ctk.CTkButton(header, text="⚙️ Categories", fg_color="#10B981", 
                      width=120, height=35, command=self.show_category_ui).pack(side="right")

        # Table Headers
        list_header = ctk.CTkFrame(self.container, fg_color="#2b2b2b", height=40)
        list_header.pack(fill="x", padx=30, pady=(10, 0))
        
        ctk.CTkLabel(list_header, text="Team Member", width=180, font=("Arial", 12, "bold")).pack(side="left", padx=20)
        ctk.CTkLabel(list_header, text="Total Hrs", width=80, font=("Arial", 12, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(list_header, text="Daily Summary", font=("Arial", 12, "bold")).pack(side="left", padx=20)

        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=25, pady=10)

        try:
            # SQL: Groups all tasks per user for the selected date
            query = """
                SELECT u.full_name, SUM(dr.hours) as total_h, 
                GROUP_CONCAT(CONCAT('• [', dr.category, '] ', dr.tasks) SEPARATOR '\n') as daily_summary
                FROM users u
                JOIN daily_reports dr ON u.id = dr.user_id
                WHERE dr.report_date = %s
                GROUP BY u.id
                ORDER BY u.full_name ASC
            """
            self.db.cursor.execute(query, (self.filter_date_str,))
            reports = self.db.cursor.fetchall()

            if not reports:
                ctk.CTkLabel(scroll, text=f"No reports submitted for {self.filter_date_str}", 
                             text_color="gray70", font=("Arial", 14)).pack(pady=50)

            for r in reports:
                card = ctk.CTkFrame(scroll, fg_color="#1e1e1e", corner_radius=10)
                card.pack(fill="x", pady=5, padx=5)
                
                ctk.CTkLabel(card, text=r['full_name'], width=180, font=("Arial", 14, "bold"), 
                             text_color="#00fbff", anchor="w").pack(side="left", padx=20, pady=15)
                
                h_val = float(r['total_h'] or 0)
                h_color = "#10B981" if h_val >= 8 else "#F1C40F"
                ctk.CTkLabel(card, text=f"{h_val}h", width=80, text_color=h_color, 
                             font=("Arial", 15, "bold")).pack(side="left", padx=10)

                ctk.CTkLabel(card, text=r['daily_summary'], justify="left", anchor="w", 
                             text_color="gray85", wraplength=600).pack(side="left", padx=20, pady=10)

        except Exception as e:
            print(f"Fetch Error: {e}")

    # --- CALENDAR DROPDOWN LOGIC ---
    def toggle_filter_calendar(self):
        if not self.cal_visible:
            self.setup_calendar_ui()
            
            # --- USE RELATIVE POSITIONING ---
            # relx=0.5 and rely=0.5 puts the anchor in the exact middle of the screen.
            # anchor="center" ensures the MIDDLE of the calendar is at that spot.
            self.cal_frame.place(relx=0.5, rely=0.5, anchor="center")
            
            # Ensure it stays on top of the member cards
            self.cal_frame.lift()
            
            # Optional: Change button color to show it's active
            self.date_btn.configure(fg_color="#10B981")
        else:
            # Hide the calendar
            self.cal_frame.place_forget()
            self.date_btn.configure(fg_color="#2b2b2b")
        
        self.cal_visible = not self.cal_visible
        
    def setup_calendar_ui(self):
        for w in self.cal_frame.winfo_children(): w.destroy()
        
        nav = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        nav.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(nav, text="<", width=30, fg_color="#333333", command=self.prev_month).pack(side="left")
        self.month_lbl = ctk.CTkLabel(nav, text=f"{calendar.month_name[self.cur_month]} {self.cur_year}",
                                      font=("Arial", 13, "bold"), text_color="#00fbff")
        self.month_lbl.pack(side="left", expand=True)
        ctk.CTkButton(nav, text=">", width=30, fg_color="#333333", command=self.next_month).pack(side="right")

        grid = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        grid.pack(padx=10, pady=(5, 15))

        days = calendar.monthcalendar(self.cur_year, self.cur_month)
        for r, week in enumerate(days):
            for c, day in enumerate(week):
                if day != 0:
                    is_selected = f"{self.cur_year}-{self.cur_month:02d}-{day:02d}" == self.filter_date_str
                    btn_color = "#10B981" if is_selected else "transparent"
                    
                    ctk.CTkButton(grid, text=str(day), width=35, height=35, 
                                  fg_color=btn_color, hover_color="#1f538d",
                                  command=lambda d=day: self.select_date(d)).grid(row=r, column=c, padx=1, pady=1)

    def select_date(self, day):
        self.filter_date_str = f"{self.cur_year}-{self.cur_month:02d}-{day:02d}"
        self.toggle_filter_calendar()
        self.show_reports_list()

    def prev_month(self):
        self.cur_month = 12 if self.cur_month == 1 else self.cur_month - 1
        if self.cur_month == 12: self.cur_year -= 1
        self.setup_calendar_ui()

    def next_month(self):
        self.cur_month = 1 if self.cur_month == 12 else self.cur_month + 1
        if self.cur_month == 1: self.cur_year += 1
        self.setup_calendar_ui()

    # --- VIEW 2: CATEGORY MANAGEMENT ---
    def show_category_ui(self):
        self.clear_container()
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkButton(header, text="← Back", width=100, command=self.show_reports_list).pack(side="left")
        ctk.CTkLabel(header, text="Manage Categories", font=("Arial", 22, "bold"), text_color="#10B981").pack(side="left", padx=20)

        input_f = ctk.CTkFrame(self.container, fg_color="#1e1e1e", corner_radius=12)
        input_f.pack(fill="x", padx=30, pady=10)
        self.cat_entry = ctk.CTkEntry(input_f, placeholder_text="New category name...", width=300)
        self.cat_entry.pack(side="left", padx=20, pady=20)
        ctk.CTkButton(input_f, text="Add", width=100, command=self.add_category).pack(side="left")

        self.cat_scroll = ctk.CTkScrollableFrame(self.container, label_text="Current Categories", fg_color="transparent")
        self.cat_scroll.pack(fill="both", expand=True, padx=30, pady=10)
        self.refresh_categories()

    def add_category(self):
        name = self.cat_entry.get().strip()
        if name:
            try:
                self.db.cursor.execute("INSERT INTO report_categories (name) VALUES (%s)", (name,))
                self.db.conn.commit()
                self.cat_entry.delete(0, 'end')
                self.refresh_categories()
            except:
                messagebox.showerror("Error", "Category already exists.")

    def refresh_categories(self):
        for w in self.cat_scroll.winfo_children(): w.destroy()
        self.db.cursor.execute("SELECT * FROM report_categories ORDER BY name ASC")
        for cat in self.db.cursor.fetchall():
            row = ctk.CTkFrame(self.cat_scroll, fg_color="#2b2b2b")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=cat['name']).pack(side="left", padx=20, pady=10)
            ctk.CTkButton(row, text="Delete", width=70, fg_color="#E74C3C", 
                          command=lambda cid=cat['id']: self.delete_category(cid)).pack(side="right", padx=10)

    def delete_category(self, cat_id):
        if messagebox.askyesno("Confirm", "Delete this category?"):
            self.db.cursor.execute("DELETE FROM report_categories WHERE id = %s", (cat_id,))
            self.db.conn.commit()
            self.refresh_categories()