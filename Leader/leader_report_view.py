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

        # The Calendar widget is a standard TK widget, so we use a neutral dark-friendly theme 
        # that remains legible, but the wrapper around it is theme-aware.
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

        # BUTTON - Theme Aware (Light/Dark)
        self.btn = ctk.CTkButton(
            self,
            text=self._fmt(),
            width=140,
            height=36,
            corner_radius=8,
            fg_color=("#F2F2F2", "#1E1E1E"),
            text_color=("#000000", "#FFFFFF"),
            hover_color=("#E5E5E5", "#2A2A2A"),
            border_width=1,
            border_color=("#CCCCCC", "#2C2C2C"),
            anchor="w",
            command=self.toggle
        )
        self.btn.pack()

        # FLOATING PANEL - Theme Aware
        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color=("#FFFFFF", "#141E2B"),
            corner_radius=12,
            border_width=1,
            border_color=("#CCCCCC", "#2A3A4A")
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
        self.member_search = ""

        # Get team name for this user
        self.team_id = self.user.get('team_id')
        self.team_name = self.db.get_team_name(self.team_id) or "Unknown Team"

        # Main Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_reports_list()

    def get_member_names(self):
        try:
            query = "SELECT full_name FROM users WHERE role = 'member' AND team_id = %s ORDER BY full_name ASC"
            self.db.cursor.execute(query, (self.team_id,))
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
            text_color=("#333333", "#FFFFFF")
        ).pack(side="left")

        # Right side container
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right")

        # Category button
        ctk.CTkButton(
            right_frame,
            text="📂 Category",
            width=120, height=36, corner_radius=9,
            font=("Arial", 12, "bold"),
            fg_color="#8E44AD", hover_color="#6C3483",
            command=self.show_category_ui
        ).pack()

        # Filter Card - Theme Aware Colors
        filter_card = ctk.CTkFrame(
            self.container,
            corner_radius=14,
            fg_color=("#F9F9F9", "#1E1E1E"),
            border_width=1,
            border_color=("#E0E0E0", "#2C2C2C")
        )
        filter_card.pack(fill="x", padx=content_padx, pady=(4, 10))
        inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)

        def _lbl(parent, text):
            ctk.CTkLabel(parent, text=text,
                         font=("Arial", 11, "bold"),
                         text_color=("#555555", "#FFFFFF")).pack(side="left", padx=(0, 4))

        # Date pickers
        _lbl(inner, "From")
        self.start_cal = DatePickerButton(inner, initial_date=self.start_date)
        self.start_cal.pack(side="left", padx=(0, 16))
        _lbl(inner, "To")
        self.end_cal = DatePickerButton(inner, initial_date=self.end_date)
        self.end_cal.pack(side="left", padx=(0, 24))

        # Separator
        sep = ctk.CTkFrame(inner, width=1, height=32, fg_color=("#CCCCCC", "#2A3A4A"))
        sep.pack(side="left", padx=(0, 20))

        # Member search
        _lbl(inner, "Member")
        self.member_entry = ctk.CTkEntry(
            inner, placeholder_text="Search member…",
            width=150, height=36, corner_radius=8,
            border_color=("#CCCCCC", "#2C2C2C"), border_width=1,
            fg_color=("#FFFFFF", "#1E1E1E"),
            text_color=("#000000", "#FFFFFF"),
            font=("Arial", 12)
        )
        self.member_entry.pack(side="left", padx=(0, 8))

        # Action buttons
        def _btn(parent, text, color, hover, cmd, width=75):
            b = ctk.CTkButton(
                parent, text=text, width=width, height=36,
                corner_radius=9, font=("Arial", 12, "bold"),
                fg_color=color, hover_color=hover, command=cmd
            )
            b.pack(side="left", padx=4)
            return b

        _btn(inner, "🔍 Filter", "#2471A3", "#1A5276", self.refresh_view, width=80)
        _btn(inner, "✖ Clear", "#566573", "#424949", self.clear_filters, width=70)
        _btn(inner, "📄 Export", "#C0392B", "#922B21", self.export_to_pdf, width=80)
        
        # List header
        list_header = ctk.CTkFrame(self.container, fg_color="transparent")
        list_header.pack(fill="x", padx=content_padx, pady=(4, 2))
        ctk.CTkLabel(list_header, text="Report List", font=("Arial", 14, "bold"), text_color=("#333333", "#FFFFFF")).pack(side="left", padx=4)
        self.count_lbl = ctk.CTkLabel(list_header, text="", font=("Arial", 12), text_color="#566573")
        self.count_lbl.pack(side="left", padx=8)

        self.scroll = ctk.CTkScrollableFrame(
            self.container,
            fg_color=("#EEEEEE", "#1A1A1A"),
            corner_radius=14,
            border_width=1,
            border_color=("#DDDDDD", "#2C2C2C")
        )
        self.scroll.pack(fill="both", expand=True, padx=content_padx, pady=(0, 10))

        self.refresh_view()

    def refresh_view(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        team_id = self.team_id
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
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
            
            grouped = defaultdict(list)
            for r in rows:
                key = (r['report_date'], r['full_name'])
                grouped[key].append(r)
                
            self.count_lbl.configure(text=f"({len(grouped)} records)")

            last_date = None
            for (date_val, member), tasks in grouped.items():
                is_today = date_val == today_date
                if last_date != date_val:
                    date_sep = ctk.CTkFrame(self.scroll, fg_color="transparent")
                    date_sep.pack(fill="x", padx=8, pady=(8, 1))
                    day_str = date_val.strftime("%A")
                    date_str = date_val.strftime("%d %b %Y")
                    badge_color = "#E67E22" if is_today else ("#BDC3C7", "#2C3E50")
                    badge_text = f"  {date_str}  ·  {day_str}{'  ← TODAY' if is_today else ''}  "
                    ctk.CTkLabel(
                        date_sep, text=badge_text,
                        font=("Arial", 11, "bold"),
                        text_color=("black", "white"),
                        fg_color=badge_color, corner_radius=6,
                        padx=6, pady=2
                    ).pack(side="left")
                    last_date = date_val

                card = ctk.CTkFrame(self.scroll,
                    corner_radius=12,
                    fg_color=("#FFFFFF", "#1E1E1E"),
                    border_width=1,
                    border_color=("#E0E0E0", "#2C2C2C")
                )
                card.pack(fill="x", pady=1, padx=10)
                info = ctk.CTkFrame(card, fg_color="transparent")
                info.pack(side="left", fill="both", expand=True, padx=10, pady=6)

                ctk.CTkLabel(info, text=member, font=("Arial", 12, "bold"), text_color=("#333333", "#E8EDF2")).pack(anchor="w")
                total_hours = sum(float(t['hours']) for t in tasks)
                ctk.CTkLabel(info, text=f"Total: {total_hours}h", font=("Arial", 10), text_color="#7F8C8D").pack(anchor="w")

                btn_frame = ctk.CTkFrame(card, fg_color="transparent")
                btn_frame.pack(side="right", padx=12, pady=6)

                ctk.CTkButton(
                    btn_frame, text="View", width=60, height=25, corner_radius=8,
                    fg_color="#1f538d", hover_color="#174a7a",
                    command=lambda tlist=tasks, m=member, d=date_val:
                    self.open_detail_with_state(m, d, tlist)
                ).pack()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def open_detail_with_state(self, member, date_val, tasks):
        self.start_date = self.start_cal.get_date()
        self.end_date = self.end_cal.get_date()
        self.member_search = self.member_entry.get()
        self.show_member_detail(member, date_val, tasks)

    def show_member_detail(self, member_name, date_val, tasks):
        self.clear_container()
        content_padx = 80
        top = ctk.CTkFrame(self.container, fg_color="transparent")
        top.pack(fill="x", padx=content_padx, pady=14)

        ctk.CTkButton(top, text="← Back", command=self.back_to_list).pack(side="left")
        ctk.CTkLabel(top, text=f"{member_name} - {date_val}", font=("Arial", 20, "bold"), text_color=("#333333", "#FFFFFF")).pack(side="left", padx=20)

        scroll = ctk.CTkScrollableFrame(self.container, fg_color=("#EEEEEE", "#1A1A1A"), corner_radius=14, border_width=1, border_color=("#DDDDDD", "#2C2C2C"))
        scroll.pack(fill="both", expand=True, padx=content_padx, pady=(0, 10))

        for r in tasks:
            card = ctk.CTkFrame(scroll, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=10, border_width=1, border_color=("#E0E0E0", "#2C2C2C"))
            card.pack(fill="x", pady=6, padx=10)

            ctk.CTkLabel(card, text=f"[{r['category']}] {r['hours']}h", font=("Arial", 13, "bold"), text_color=("#2471A3", "#E8EDF2")).pack(anchor="w", padx=10, pady=(8, 2))
            ctk.CTkLabel(card, text=r['tasks'], wraplength=700, text_color=("#555555", "#AAB7C4")).pack(anchor="w", padx=10, pady=(0, 8))
            
    def back_to_list(self):
        self.show_reports_list()
        self.start_cal.set_date(self.start_date)
        self.end_cal.set_date(self.end_date)
        self.member_entry.delete(0, "end")
        self.member_entry.insert(0, self.member_search)
        self.refresh_view()

    def clear_filters(self):
        today = datetime.today().date()
        self.start_date = today
        self.end_date = today
        self.member_search = ""
        self.show_reports_list()

    def export_to_pdf(self):
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        member_search = self.member_entry.get().strip()
        query = '''SELECT u.full_name, dr.report_date, dr.category, dr.tasks, dr.hours
                    FROM users u JOIN daily_reports dr ON u.id = dr.user_id
                    WHERE u.team_id=%s AND dr.report_date BETWEEN %s AND %s AND u.role='member' '''
        params = [self.team_id, start, end]
        if member_search:
            query += " AND u.full_name LIKE %s"
            params.append(f"%{member_search}%")
        query += " ORDER BY dr.report_date ASC, u.full_name ASC"

        try:
            self.db.cursor.execute(query, tuple(params))
            rows = self.db.cursor.fetchall()
            if not rows:
                messagebox.showinfo("No Data", "No reports found.")
                return
            
            grouped = defaultdict(list)
            for r in rows: grouped[(r['report_date'], r['full_name'])].append(r)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, f"{self.team_name} Reports", ln=True, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", 'B', 10)
            headers = ["Date", "Member", "Category", "Hrs", "Task"]
            w = [25, 35, 30, 15, 85]
            for i, h in enumerate(headers): pdf.cell(w[i], 10, h, border=1, align='C')
            pdf.ln()

            pdf.set_font("Arial", '', 9)
            for (date, member), tasks in grouped.items():
                for i, r in enumerate(tasks):
                    pdf.cell(w[0], 10, str(date) if i==0 else "", border='LR' if i<len(tasks)-1 else 'LRB', align='C')
                    pdf.cell(w[1], 10, member if i==0 else "", border='LR' if i<len(tasks)-1 else 'LRB', align='C')
                    pdf.cell(w[2], 10, r['category'], border=1, align='C')
                    pdf.cell(w[3], 10, str(r['hours']), border=1, align='C')
                    pdf.cell(w[4], 10, r['tasks'][:50], border=1)
                    pdf.ln()

            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=f"{self.team_name}_Reports.pdf")
            if file_path:
                pdf.output(file_path)
                messagebox.showinfo("Success", "PDF saved.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_category_ui(self):
        self.clear_container()
        content_padx = 80
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=content_padx, pady=14)

        ctk.CTkButton(header, text="← Back", width=100, command=self.show_reports_list).pack(side="left")
        ctk.CTkLabel(header, text="Manage Categories", font=("Arial", 22, "bold"), text_color=("#333333", "#FFFFFF")).pack(side="left", padx=20)

        input_f = ctk.CTkFrame(self.container, fg_color=("#F9F9F9", "#1E1E1E"), corner_radius=14, border_width=1, border_color=("#E0E0E0", "#2C2C2C"))
        input_f.pack(fill="x", padx=content_padx, pady=(4, 10))

        self.cat_entry = ctk.CTkEntry(input_f, placeholder_text="New category name...", width=300, height=36, corner_radius=8,
                                     border_color=("#CCCCCC", "#2C2C2C"), fg_color=("#FFFFFF", "#1E1E1E"), text_color=("#000000", "#FFFFFF"))
        self.cat_entry.pack(side="left", padx=20, pady=14)
        ctk.CTkButton(input_f, text="Add", width=100, fg_color="#2471A3", command=self.add_category).pack(side="left", padx=10)

        self.cat_scroll = ctk.CTkScrollableFrame(self.container, fg_color=("#EEEEEE", "#1A1A1A"), corner_radius=14, border_width=1, border_color=("#DDDDDD", "#2C2C2C"))
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
            row = ctk.CTkFrame(self.cat_scroll, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=10, border_width=1, border_color=("#E0E0E0", "#2C2C2C"))
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=cat['name'], text_color=("#333333", "#FFFFFF")).pack(side="left", padx=20, pady=10)
            ctk.CTkButton(row, text="Delete", width=70, fg_color="#E74C3C", command=lambda cid=cat['id']: self.delete_category(cid)).pack(side="right", padx=10)

    def delete_category(self, cat_id):
        if messagebox.askyesno("Confirm", "Delete this category?"):
            self.db.cursor.execute("DELETE FROM report_categories WHERE id = %s", (cat_id,))
            self.db.conn.commit()
            self.refresh_categories()