import customtkinter as ctk
from database import Database
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
import tkinter as tk
import calendar
from fpdf import FPDF
from tkcalendar import DateEntry, Calendar
from collections import defaultdict

# ── Reusable modern date-picker ──────────────────────────────────────────────
class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None):
        super().__init__(master, fg_color="transparent")

        self._date = initial_date or datetime.today().date()
        self._open = False

        # STYLE
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Custom.Calendar",
            background="#1A1A2E",
            foreground="white",
            headersbackground="#16213E",
            headersforeground="#4FC3F7",
            selectbackground="#3498DB",
            selectforeground="white",
            normalbackground="#1A1A2E",
            normalforeground="#CCCCCC",
            weekendbackground="#1A1A2E",
            weekendforeground="#F39C12",
            othermonthforeground="#555555",
            bordercolor="#2A2A4A",
            relief="flat"
        )

        # BUTTON
        self.btn = ctk.CTkButton(
            self,
            text=self._fmt(),
            width=140,
            height=36,
            corner_radius=8,
            fg_color="#1E1E1E",
            hover_color="#2A2A2A",
            border_width=1,
            border_color="#2C2C2C",
            anchor="w",
            command=self.toggle
        )
        self.btn.pack()

        # FLOATING PANEL
        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color="#141E2B",
            corner_radius=12,
            border_width=1,
            border_color="#2A3A4A"
        )

        # CALENDAR
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

        # AUTO SELECT
        self.cal.bind("<<CalendarSelected>>", self._select)

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

    def get_date(self):
        return self._date

    def set_date(self, d):
        self._date = d
        self.cal.selection_set(d)
        self.btn.configure(text=self._fmt())

    def _fmt(self):
        return f"  📅  {self._date.strftime('%Y-%m-%d')}"

    def on_change(self, callback):
        self._callback = callback
 
class LeaderReportView(ctk.CTkFrame):
    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.db = Database()
        self.user = user
        self.configure(fg_color="transparent")

        # --- Filter State ---
        today = datetime.today().date()
        self.start_date = today
        self.end_date = today
        self.member_var = ctk.StringVar(value="")
        self.member_search = ""

        # Get team name for this user
        self.team_name = self.db.get_team_name(self.user.get('team_id')) or "Unknown Team"

        # Main Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_reports_list()
 
    def get_member_names(self):
        try:
            query = "SELECT full_name FROM users WHERE role = 'member' AND team_id = %s ORDER BY full_name ASC"
            self.db.cursor.execute(query, (self.user.get('team_id'),))
            return [row['full_name'] for row in self.db.cursor.fetchall()]
        except Exception:
            return []
 
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()
 
    def show_reports_list(self):
        content_padx = 80
        self.clear_container()

        # Header Section
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=80, pady=14)

        # Left title
        ctk.CTkLabel(
            header,
            text=f"📊 {self.team_name} · Report View",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(side="left")

        # Right side container
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right")

        # Category button (TOP RIGHT)
        ctk.CTkButton(
            right_frame,
            text="📂 Category",
            width=120,
            height=36,
            corner_radius=9,
            font=("Arial", 12, "bold"),
            fg_color="#8E44AD",
            hover_color="#6C3483",
            command=self.show_category_ui
        ).pack()

        # Filter Card
        filter_card = ctk.CTkFrame(
            self.container,
            corner_radius=14,
            fg_color="#1E1E1E",
            border_width=1,
            border_color="#2C2C2C"
        )
        filter_card.pack(fill="x", padx=content_padx, pady=(4, 10))
        inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)

        def _lbl(parent, text):
            ctk.CTkLabel(parent, text=text,
                         font=("Arial", 11, "bold"),
                         text_color="white").pack(side="left", padx=(0, 4))

        # Date pickers
        _lbl(inner, "From")
        self.start_cal = DatePickerButton(inner, initial_date=self.start_date)
        self.start_cal.pack(side="left", padx=(0, 16))
        _lbl(inner, "To")
        self.end_cal = DatePickerButton(inner, initial_date=self.end_date)
        self.end_cal.pack(side="left", padx=(0, 24))

        # Separator
        sep = ctk.CTkFrame(inner, width=1, height=32, fg_color="#2A3A4A")
        sep.pack(side="left", padx=(0, 20))

        # Member search
        _lbl(inner, "Member")
        self.member_entry = ctk.CTkEntry(
            inner, placeholder_text="Search member…",
            width=150, height=36,
            corner_radius=8,
            border_color="#2C2C2C", border_width=1,
            fg_color="#1E1E1E",
            font=("Arial", 12)
        )
        self.member_entry.pack(side="left", padx=(0, 16))

        # Action buttons
        def _btn(parent, text, color, hover, cmd, width=75):
            b = ctk.CTkButton(
                parent, text=text, width=width, height=36,
                corner_radius=9,
                font=("Arial", 12, "bold"),
                fg_color=color, hover_color=hover,
                command=cmd
            )
            b.pack(side="left", padx=4)
            return b

        _btn(inner, "🔍 Filter",  "#2471A3", "#1A5276", self.refresh_view, width=80)
        _btn(inner, "✖ Clear",   "#566573", "#424949", self.clear_filters, width=70)
        _btn(inner, "📄 Export", "#C0392B", "#922B21", self.export_to_pdf, width=80)
        
        # List header
        list_header = ctk.CTkFrame(self.container, fg_color="transparent")
        list_header.pack(fill="x", padx=content_padx, pady=(4, 2))
        ctk.CTkLabel(list_header, text="Report List", font=("Arial", 14, "bold"), text_color="white").pack(side="left", padx=4)
        self.count_lbl = ctk.CTkLabel(list_header, text="", font=("Arial", 12), text_color="#566573")
        self.count_lbl.pack(side="left", padx=8)

        self.scroll = ctk.CTkScrollableFrame(
            self.container,
            fg_color="#1A1A1A",
            corner_radius=14,
            border_width=1,
            border_color="#2C2C2C"
        )
        self.scroll.pack(fill="both", expand=True, padx=content_padx, pady=(0, 10))

        self.refresh_view()

    def refresh_view(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        team_id = self.user.get('team_id')
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        # Date validation
        if start > end:
            messagebox.showerror("Invalid Date", "Start date cannot be later than End date.")
            return
        member_search = self.member_entry.get().strip()
        today_date = datetime.today().date()

        query = '''SELECT u.full_name, dr.report_date, dr.category, dr.tasks, dr.hours
                   FROM users u
                   JOIN daily_reports dr ON u.id = dr.user_id
                   WHERE u.team_id=%s AND dr.report_date BETWEEN %s AND %s AND u.role='member' '''
        params = [team_id, start, end]
        if member_search:
            query += " AND u.full_name LIKE %s"
            params.append(f"%{member_search}%")
        query += " ORDER BY dr.report_date ASC, u.full_name ASC, dr.created_at ASC"

        try:
            self.db.cursor.execute(query, tuple(params))
            rows = self.db.cursor.fetchall()
            
            # Group by (date, member)
            from collections import defaultdict
            grouped = defaultdict(list)
            for r in rows:
                key = (r['report_date'], r['full_name'])
                grouped[key].append(r)
                
            self.count_lbl.configure(text=f"({len(grouped)} records)")

            last_date = None
            for (date_val, member), tasks in grouped.items():
                is_today = date_val == today_date
                # Only show date separator if date changes
                if last_date != date_val:
                    date_sep = ctk.CTkFrame(self.scroll, fg_color="transparent")
                    date_sep.pack(fill="x", padx=8, pady=(8, 1))
                    day_str = date_val.strftime("%A")
                    date_str = date_val.strftime("%d %b %Y")
                    badge_color = "#E67E22" if is_today else "#2C3E50"
                    badge_text = f"  {date_str}  ·  {day_str}{'  ← TODAY' if is_today else ''}  "
                    ctk.CTkLabel(
                        date_sep,
                        text=badge_text,
                        font=("Arial", 11, "bold"),
                        text_color="white",
                        fg_color=badge_color,
                        corner_radius=6,
                        padx=6, pady=2
                    ).pack(side="left")
                    last_date = date_val

                # Row for this member on this date
                card = ctk.CTkFrame(self.scroll,
                    corner_radius=12,
                    fg_color="#1E1E1E",
                    border_width=1,
                    border_color="#2C2C2C"
                )
                card.pack(fill="x", pady=1, padx=10)
                # LEFT SIDE (info)
                info = ctk.CTkFrame(card, fg_color="transparent")
                info.pack(side="left", fill="both", expand=True, padx=10, pady=6)

                ctk.CTkLabel(info, text=member,
                            font=("Arial", 12, "bold"),
                            text_color="#E8EDF2").pack(anchor="w")

                total_hours = sum(float(t['hours']) for t in tasks)

                ctk.CTkLabel(info, text=f"Total: {total_hours}h",
                            font=("Arial", 10),
                            text_color="#4A5568").pack(anchor="w")


                # RIGHT SIDE (button)
                btn_frame = ctk.CTkFrame(card, fg_color="transparent")
                btn_frame.pack(side="right", padx=12, pady=6)

                ctk.CTkButton(
                    btn_frame,
                    text="View",
                    width=60,
                    height=25,
                    corner_radius=8,
                    fg_color="#1f538d",
                    hover_color="#174a7a",
                    command=lambda tlist=tasks, m=member, d=date_val:
                    self.open_detail_with_state(m, d, tlist)
                ).pack()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def open_detail_with_state(self, member, date_val, tasks):
        # SAVE CURRENT FILTER STATE
        self.start_date = self.start_cal.get_date()
        self.end_date = self.end_cal.get_date()
        self.member_search = self.member_entry.get()

        self.show_member_detail(member, date_val, tasks)

    def show_member_detail(self, member_name, date_val, tasks):
        self.clear_container()

        content_padx = 80   # ✅ SAME as report list

        # Header
        top = ctk.CTkFrame(self.container, fg_color="transparent")
        top.pack(fill="x", padx=content_padx, pady=14)

        ctk.CTkButton(top, text="← Back", command=self.back_to_list).pack(side="left")

        ctk.CTkLabel(
            top,
            text=f"{member_name} - {date_val}",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(side="left", padx=20)

        # Scroll area
        scroll = ctk.CTkScrollableFrame(
            self.container,
            fg_color="#1A1A1A",
            corner_radius=14,
            border_width=1,
            border_color="#2C2C2C"
        )
        scroll.pack(fill="both", expand=True, padx=content_padx, pady=(0, 10))

        for r in tasks:
            card = ctk.CTkFrame(
                scroll,
                fg_color="#1E1E1E",
                corner_radius=10,
                border_width=1,
                border_color="#2C2C2C"
            )
            card.pack(fill="x", pady=6, padx=10)

            ctk.CTkLabel(
                card,
                text=f"[{r['category']}] {r['hours']}h",
                font=("Arial", 13, "bold"),
                text_color="#E8EDF2"
            ).pack(anchor="w", padx=10, pady=(8, 2))

            ctk.CTkLabel(
                card,
                text=r['tasks'],
                wraplength=700,
                text_color="#AAB7C4"
            ).pack(anchor="w", padx=10, pady=(0, 8))
            
    def back_to_list(self):
        # rebuild UI
        self.show_reports_list()

        # RESTORE STATE
        self.start_cal.set_date(self.start_date)
        self.end_cal.set_date(self.end_date)

        self.member_entry.delete(0, "end")
        self.member_entry.insert(0, self.member_search)

        # reload filtered data
        self.refresh_view()

    def clear_filters(self):
        # Reset internal state
        today = datetime.today().date()
        self.start_date = today
        self.end_date = today

        # Rebuild the whole UI (same as first load)
        self.show_reports_list()

    def export_to_pdf(self):
        team_id = self.user.get('team_id')
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        # Date validation
        if start > end:
            messagebox.showerror("Invalid Date", "Start date cannot be later than End date.")
            return
        member_search = self.member_entry.get().strip()

        query = '''SELECT u.full_name, dr.report_date, dr.category, dr.tasks, dr.hours
                   FROM users u
                   JOIN daily_reports dr ON u.id = dr.user_id
                   WHERE u.team_id=%s AND dr.report_date BETWEEN %s AND %s AND u.role='member' '''
        params = [team_id, start, end]
        if member_search:
            query += " AND u.full_name LIKE %s"
            params.append(f"%{member_search}%")
        query += " ORDER BY dr.report_date ASC, u.full_name ASC, dr.created_at ASC"

        try:
            self.db.cursor.execute(query, tuple(params))
            rows = self.db.cursor.fetchall()
            if not rows:
                messagebox.showinfo("No Data", "No reports found for the selected filters.")
                return
            from fpdf import FPDF
            from collections import defaultdict
            grouped = defaultdict(list)
            for r in rows:
                key = (r['report_date'], r['full_name'])
                grouped[key].append(r)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, f"{self.team_name} Reports", ln=True, align='C')
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, f"From {start} to {end}", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(30, 10, "Date", border=1, align='C')
            pdf.cell(50, 10, "Member", border=1, align='C')
            pdf.cell(35, 10, "Category", border=1, align='C')
            pdf.cell(20, 10, "Hours", border=1, align='C')
            pdf.cell(60, 10, "Task", border=1, align='C')
            pdf.ln()
            pdf.set_font("Arial", '', 12)
            for (date, member), tasks in grouped.items():
                n = len(tasks)
                for i, r in enumerate(tasks):
                    # Merge date/member cells for all but first row (no inner border)
                    if i == 0:
                        pdf.cell(30, 10 * n, str(date), border='LTB', align='C')
                        pdf.cell(50, 10 * n, member, border='LTB', align='C')
                    else:
                        pdf.cell(30, 10, '', border='', align='C')
                        pdf.cell(50, 10, '', border='', align='C')
                    pdf.cell(35, 10, r['category'], border=1, align='C')
                    pdf.cell(20, 10, str(r['hours']), border=1, align='C')
                    pdf.cell(60, 10, r['tasks'], border=1, align='C')
                    pdf.ln()
            default_name = f"{self.team_name}_Reports.pdf"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=default_name,
                filetypes=[("PDF files", "*.pdf")],
                title="Save PDF"
            )
            if file_path:
                pdf.output(file_path)
                messagebox.showinfo("Success", f"PDF saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"PDF Error: {e}")
 
    # --- CALENDAR DROPDOWN LOGIC ---
    def toggle_filter_calendar(self):
        if not self.cal_visible:
            self.setup_calendar_ui()
            self.cal_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.cal_frame.lift()
            self.date_btn.configure(fg_color="#10B981")
        else:
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
        self.date_btn.configure(text=f"📅 {self.filter_date_str}")
        self.toggle_filter_calendar()
 
    def prev_month(self):
        self.cur_month = 12 if self.cur_month == 1 else self.cur_month - 1
        if self.cur_month == 12: self.cur_year -= 1
        self.setup_calendar_ui()
 
    def next_month(self):
        self.cur_month = 1 if self.cur_month == 12 else self.cur_month + 1
        if self.cur_month == 1: self.cur_year += 1
        self.setup_calendar_ui()
 
    # --- VIEW 2: CATEGORY MANAGEMENT ---
    def perform_search(self):
        self.show_reports_list()
 
    def show_category_ui(self):
        self.clear_container()

        content_padx = 80   # ✅ SAME spacing everywhere

        # Header
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=content_padx, pady=14)

        ctk.CTkButton(header, text="← Back", width=100,
                    command=self.show_reports_list).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Manage Categories",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(side="left", padx=20)

        # Input section
        input_f = ctk.CTkFrame(
            self.container,
            fg_color="#1E1E1E",
            corner_radius=14,
            border_width=1,
            border_color="#2C2C2C"
        )
        input_f.pack(fill="x", padx=content_padx, pady=(4, 10))

        self.cat_entry = ctk.CTkEntry(
            input_f,
            placeholder_text="New category name...",
            width=300,
            height=36,
            corner_radius=8,
            border_color="#2C2C2C",
            border_width=1,
            fg_color="#1E1E1E",
            font=("Arial", 12)
        )
        self.cat_entry.pack(side="left", padx=20, pady=14)

        ctk.CTkButton(
            input_f,
            text="Add",
            width=100,
            height=36,
            corner_radius=9,
            fg_color="#2471A3",
            hover_color="#1A5276"
        , command=self.add_category).pack(side="left", padx=10)

        # Category list
        self.cat_scroll = ctk.CTkScrollableFrame(
            self.container,
            fg_color="#1A1A1A",
            corner_radius=14,
            border_width=1,
            border_color="#2C2C2C"
        )
        self.cat_scroll.pack(fill="both", expand=True, padx=content_padx, pady=(0, 10))

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
            row = ctk.CTkFrame(
                self.cat_scroll,
                fg_color="#1E1E1E",
                corner_radius=10,
                border_width=1,
                border_color="#2C2C2C"
            )
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=cat['name']).pack(side="left", padx=20, pady=10)
            ctk.CTkButton(row, text="Delete", width=70, fg_color="#E74C3C",
                          command=lambda cid=cat['id']: self.delete_category(cid)).pack(side="right", padx=10)
 
    def delete_category(self, cat_id):
        if messagebox.askyesno("Confirm", "Delete this category?"):
            self.db.cursor.execute("DELETE FROM report_categories WHERE id = %s", (cat_id,))
            self.db.conn.commit()
            self.refresh_categories()

    def export_pdf(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Export")
        popup.geometry("400x300")
        popup.grab_set()          # force focus
        popup.resizable(True, True)

        # Start date frame
        frame1 = ctk.CTkFrame(popup, fg_color="transparent")
        frame1.pack(pady=(20,5))
        ctk.CTkLabel(frame1, text="Start Date:", font=("Arial", 12)).pack(side="left")
        start_date = DateEntry(frame1, date_pattern='yyyy-mm-dd', width=12)
        start_date.pack(side="left", pady=5)

        # End date frame
        frame2 = ctk.CTkFrame(popup, fg_color="transparent")
        frame2.pack(pady=5)
        ctk.CTkLabel(frame2, text="End Date:", font=("Arial", 12)).pack(side="left")
        end_date = DateEntry(frame2, date_pattern='yyyy-mm-dd', width=12)
        end_date.pack(side="left", pady=5)

        # Member frame
        frame3 = ctk.CTkFrame(popup, fg_color="transparent")
        frame3.pack(pady=5)
        ctk.CTkLabel(frame3, text="Member:", font=("Arial", 12)).pack(side="left")
        members = self.get_member_names()
        member_var = ctk.StringVar()
        member_combo = ctk.CTkOptionMenu(frame3, values=members, variable=member_var, width=200)
        member_combo.pack(side="left", pady=5)

        # Download button
        ctk.CTkButton(popup, text="Download", fg_color="#10B981", command=lambda: self.generate_pdf(start_date.get_date(), end_date.get_date(), member_var.get(), popup)).pack(pady=20)

    def generate_pdf(self, start, end, member, popup):
        if end < start:
            messagebox.showerror("Error", "End date must be on or after start date.")
            return
        if not member:
            messagebox.showerror("Error", "Please select a member.")
            return

        # Query reports
        query = """
            SELECT report_date, category, tasks, hours
            FROM daily_reports dr
            JOIN users u ON u.id = dr.user_id
            WHERE u.full_name = %s AND dr.report_date BETWEEN %s AND %s
            ORDER BY report_date ASC, dr.created_at ASC
        """
        self.db.cursor.execute(query, (member, str(start), str(end)))
        reports = self.db.cursor.fetchall()

        if not reports:
            messagebox.showinfo("No Data", "No reports found for the selected member and date range.")
            return

        # Group by date
        grouped = defaultdict(list)
        for r in reports:
            grouped[str(r['report_date'])].append(r)

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Daily Reports for {member}", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"From {start} to {end}", ln=True, align='C')
        pdf.ln(10)

        # Table headers
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(30, 10, "Date", border=1, align='C')
        pdf.cell(35, 10, "Category", border=1, align='C')
        pdf.cell(25, 10, "Duration", border=1, align='C')
        pdf.cell(100, 10, "Task Description", border=1, align='C')
        pdf.ln()

        # Table rows

        pdf.set_font("Arial", '', 12)
        for date in sorted(grouped.keys()):
            rows = grouped[date]
            total_rows = len(rows)

            for i, r in enumerate(rows):

                # DATE COLUMN (merged look)
                if i == 0:
                    pdf.cell(30, 10, date, border='LTR', align='C')
                elif i == total_rows - 1:
                    pdf.cell(30, 10, "", border='LBR', align='C')
                else:
                    pdf.cell(30, 10, "", border='LR', align='C')

                # border style for other columns
                if i == 0:
                    border_style = 'LTR'
                elif i == total_rows - 1:
                    border_style = 'LBR'
                else:
                    border_style = 'LR'

                pdf.cell(35, 10, r['category'], border=border_style, align='C')
                pdf.cell(25, 10, f"{r['hours']}h", border=border_style, align='C')
                pdf.cell(100, 10, r['tasks'], border=border_style, align='C')

                pdf.ln()

        # Save file
        default_name = f"Daily reports for {member}.pdf"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF"
        )
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Success", f"PDF saved to {file_path}")
            popup.destroy()