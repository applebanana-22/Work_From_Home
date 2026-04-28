import customtkinter as ctk
from database import Database
from tkinter import messagebox, filedialog, ttk
from tkcalendar import Calendar
import tkinter as tk
import random
from datetime import datetime, timedelta
from itertools import groupby
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ── FIXED DATE PICKER ────────────────────────────────────────────────────────
class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._date = initial_date or datetime.today().date()
        self._open = False
        self._callback = None

        # Button styling
        self.btn = ctk.CTkButton(
            self, text=self._fmt(), width=170, height=36, corner_radius=10,
            fg_color=("#EAECEE", "#1E2A3A"), hover_color=("#D5D8DC", "#2C3E50"),
            border_width=1, border_color=("#ABB2B9", "#3D5166"),
            text_color=("#1A1A1A", "#FFFFFF"), anchor="w", command=self.toggle
        )
        self.btn.pack()

        # Dropdown Panel
        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(), fg_color=("#FFFFFF", "#141E2B"),
            corner_radius=12, border_width=1, border_color=("#ABB2B9", "#2A3A4A")
        )

        # Apply Global Style before creating Calendar
        self.apply_style()

        self.cal = Calendar(
            self.panel, selectmode="day", date_pattern="yyyy-mm-dd",
            year=self._date.year, month=self._date.month, day=self._date.day,
            showweeknumbers=False, font=("Arial", 11)
        )
        self.cal.pack(padx=8, pady=8)
        self.cal.bind("<<CalendarSelected>>", self._select)

    def apply_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg = "#1A1A2E" if is_dark else "#FFFFFF"
        fg = "white" if is_dark else "black"
        
        style.configure("Custom.Calendar", 
            background=bg, foreground=fg, 
            headersbackground="#16213E" if is_dark else "#EAECEE",
            selectbackground="#3498DB", selectforeground="white"
        )

    def _fmt(self): return f"   📅   {self._date.strftime('%Y-%m-%d')}"

    def toggle(self):
        if self._open: self.panel.place_forget()
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


# ── FULL LEADER SCHEDULE MODULE ─────────────────────────────────────────────
class LeaderSchedule(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user

        today = datetime.today()
        self.current_month_start = today.replace(day=1).date()
        next_month = today.replace(day=28) + timedelta(days=4)
        self.current_month_end = (next_month - timedelta(days=next_month.day)).date()

        self.setup_ui()
        self.auto_generate_monthly_schedule()
        self.refresh_view()

    def setup_ui(self):
        self.wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self.wrapper.pack(fill="both", expand=True, padx=40, pady=5)

        # Title Row
        title_row = ctk.CTkFrame(self.wrapper, fg_color="transparent")
        title_row.pack(fill="x", padx=10, pady=(14, 4))
        
        ctk.CTkLabel(title_row, text=f"🗓 Team {self.user.get('team_id', '—')} Schedule Manager",
                     font=("Arial", 20, "bold"), text_color=("#1A1A1A", "white")).pack(side="left")

        # Filter Card
        filter_card = ctk.CTkFrame(self.wrapper, corner_radius=14, fg_color=("#F2F4F4", "#141E2B"),
                                   border_width=1, border_color=("#D5D8DC", "#253545"))
        filter_card.pack(fill="x", padx=10, pady=10)

        inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=14)

        # From/To Selectors
        self.start_cal = DatePickerButton(inner, initial_date=self.current_month_start)
        self.start_cal.pack(side="left", padx=5)

        self.end_cal = DatePickerButton(inner, initial_date=self.current_month_end)
        self.end_cal.pack(side="left", padx=5)

        # Name Search
        self.name_filter = ctk.CTkEntry(inner, placeholder_text="Search member...", width=150, height=36)
        self.name_filter.pack(side="left", padx=10)

        # Status Dropdown
        self.status_filter = ctk.CTkComboBox(inner, values=["All", "Office", "WFH"], width=110, height=36)
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=5)

        # Buttons
        ctk.CTkButton(inner, text="🔍 Filter", width=90, fg_color="#2471A3", command=self.refresh_view).pack(side="left", padx=4)
        ctk.CTkButton(inner, text="✖ Clear", width=80, fg_color="#566573", command=self.clear_filters).pack(side="left", padx=4)
        ctk.CTkButton(inner, text="📄 Export", width=90, fg_color="#C0392B", command=self.export_to_pdf).pack(side="left", padx=4)

        # Result Count
        self.count_lbl = ctk.CTkLabel(self.wrapper, text="", font=("Arial", 12), text_color="#566573")
        self.count_lbl.pack(anchor="w", padx=15)

        # Scroll Area
        self.scroll = ctk.CTkScrollableFrame(self.wrapper, fg_color=("#FFFFFF", "#0D1117"),
                                             corner_radius=14, border_width=1, border_color=("#D5D8DC", "#1E2A3A"))
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    

    def refresh_view(self):
        for w in self.scroll.winfo_children(): w.destroy()
        
        query = """SELECT s.*, u.full_name, u.employee_id FROM wfh_schedules s 
                   JOIN users u ON s.user_id = u.id WHERE u.team_id=%s 
                   AND s.schedule_date BETWEEN %s AND %s AND u.full_name LIKE %s"""
        params = [self.user.get('team_id'), self.start_cal.get_date(), self.end_cal.get_date(), f"%{self.name_filter.get()}%"]
        
        if self.status_filter.get() != "All":
            query += " AND s.status=%s"
            params.append(self.status_filter.get())
        query += " ORDER BY s.schedule_date ASC"

        try:
            self.db.cursor.execute(query, tuple(params))
            rows = self.db.cursor.fetchall()
            self.count_lbl.configure(text=f"Showing {len(rows)} records")

            for date_val, group in groupby(rows, key=lambda r: r['schedule_date']):
                # Date Separator
                date_sep = ctk.CTkFrame(self.scroll, fg_color="transparent")
                date_sep.pack(fill="x", padx=8, pady=(10, 2))
                ctk.CTkLabel(date_sep, text=date_val.strftime('%d %b %Y (%A)'), font=("Arial", 12, "bold"),
                             fg_color="#2C3E50", text_color="white", corner_radius=6, padx=10).pack(side="left")

                for r in group:
                    is_wfh = r['status'] == 'WFH'
                    accent = "#3498DB" if is_wfh else "#27AE60"
                    
                    card = ctk.CTkFrame(self.scroll, fg_color=("#F8F9F9", "#151C28"), border_width=1, border_color=accent)
                    card.pack(fill="x", pady=2, padx=10)

                    # Avatar
                    initials = "".join([n[0] for n in r['full_name'].split()[:2]]).upper()
                    avatar = ctk.CTkFrame(card, width=34, height=34, corner_radius=17, fg_color=accent)
                    avatar.pack(side="left", padx=10, pady=6)
                    avatar.pack_propagate(False)
                    ctk.CTkLabel(avatar, text=initials, font=("Arial", 10, "bold"), text_color="white").pack(expand=True)

                    ctk.CTkLabel(card, text=r['full_name'], font=("Arial", 13, "bold")).pack(side="left", padx=5)
                    
                    # Status Pill
                    pill_bg = ("#D6EAF8", "#1A3A5C") if is_wfh else ("#D4EFDF", "#1A4032")
                    ctk.CTkLabel(card, text=f" {r['status']} ", text_color=accent, fg_color=pill_bg, corner_radius=6).pack(side="right", padx=15)
                    
                    # Edit Button
                    ctk.CTkButton(card, text="✎", width=30, height=30, fg_color="transparent", text_color="#4A5568",
                                  command=lambda row=r: self.open_edit_popup(row)).pack(side="right")

        except Exception as e: messagebox.showerror("Error", str(e))

    def open_edit_popup(self, row_data):
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Status")
        popup.geometry("300x200")
        popup.attributes('-topmost', True)
        
        status_var = ctk.StringVar(value=row_data['status'])
        ctk.CTkSegmentedButton(popup, values=["Office", "WFH"], variable=status_var).pack(pady=30)

        def save():
            self.db.cursor.execute("UPDATE wfh_schedules SET status=%s WHERE id=%s", (status_var.get(), row_data['id']))
            self.db.conn.commit()
            popup.destroy()
            self.refresh_view()
        
        ctk.CTkButton(popup, text="Save Changes", fg_color="#27AE60", command=save).pack()

    def clear_filters(self):
        self.name_filter.delete(0, 'end')
        self.status_filter.set("All")
        self.refresh_view()

    def export_to_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile="Team_Schedule.pdf")
        if not file_path: return
        try:
            self.db.cursor.execute("SELECT s.schedule_date, u.full_name, s.status FROM wfh_schedules s JOIN users u ON s.user_id=u.id WHERE u.team_id=%s ORDER BY s.schedule_date ASC", (self.user['team_id'],))
            data = self.db.cursor.fetchall()
            
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = [Paragraph(f"Team Schedule Report", getSampleStyleSheet()['Title']), Spacer(1, 12)]
            
            table_data = [["Date", "Member Name", "Status"]]
            for r in data: table_data.append([str(r['schedule_date']), r['full_name'], r['status']])
            
            t = Table(table_data)
            t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.darkblue), ('TEXTCOLOR',(0,0),(-1,0), colors.whitesmoke), ('GRID',(0,0),(-1,-1), 0.5, colors.grey)]))
            elements.append(t)
            doc.build(elements)
            messagebox.showinfo("Export", "PDF Exported Successfully!")
        except Exception as e: messagebox.showerror("PDF Error", str(e))
        
    def auto_generate_monthly_schedule(self):
        team_id = self.user.get('team_id')
        if not team_id: return
        self.db.cursor.execute("SELECT id FROM users WHERE role='member' AND team_id=%s", (team_id,))
        members = self.db.cursor.fetchall()
        
        try:
            curr = self.current_month_start
            while curr <= self.current_month_end:
                if curr.weekday() < 5:
                    for m in members:
                        self.db.cursor.execute("SELECT id FROM wfh_schedules WHERE user_id=%s AND schedule_date=%s", (m['id'], curr))
                        if not self.db.cursor.fetchone():
                            status = random.choice(['Office', 'WFH'])
                            self.db.cursor.execute("INSERT INTO wfh_schedules (user_id, leader_id, schedule_date, status) VALUES(%s,%s,%s,%s)",
                                                   (m['id'], self.user['id'], curr, status))
                curr += timedelta(days=1)
            self.db.conn.commit()
        except Exception as e: print(f"Generate Error: {e}")