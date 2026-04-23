import customtkinter as ctk
from database import Database
from tkinter import messagebox, filedialog, ttk
from tkcalendar import Calendar
import tkinter as tk
import random
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ── Reusable modern date-picker ──────────────────────────────────────────────
class DatePickerButton(ctk.CTkFrame):
    """A styled button that opens a calendar popup."""
    def __init__(self, master, label="Date", initial_date=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._date = initial_date or datetime.today().date()
        self._callback = None

        self._btn = ctk.CTkButton(
            self, text=self._fmt(), width=140, height=36,
            corner_radius=8,
            font=("Arial", 12),
            fg_color="#1E2A3A", hover_color="#2C3E50",
            border_width=1, border_color="#3D5166",
            anchor="w",
            command=self._open_picker
        )
        self._btn.pack()

    def _fmt(self):
        return f"  📅  {self._date.strftime('%Y-%m-%d')}"

    def _open_picker(self):
        top = tk.Toplevel(self)
        top.title("")
        top.resizable(False, False)
        top.attributes("-topmost", True)
        top.configure(bg="#1A1A2E")

        # position near the button
        x = self._btn.winfo_rootx()
        y = self._btn.winfo_rooty() + self._btn.winfo_height() + 4
        top.geometry(f"280x280+{x}+{y}")

        style = ttk.Style(top)
        style.theme_use("clam")
        style.configure("custom.Calendar",
                        background="#1A1A2E", foreground="white",
                        headersbackground="#16213E", headersforeground="#4FC3F7",
                        selectbackground="#3498DB", selectforeground="white",
                        normalbackground="#1A1A2E", normalforeground="#CCCCCC",
                        weekendbackground="#1A1A2E", weekendforeground="#F39C12",
                        othermonthforeground="#555555",
                        bordercolor="#2A2A4A", relief="flat")

        cal = Calendar(top, style="custom.Calendar",
                       selectmode='day',
                       year=self._date.year,
                       month=self._date.month,
                       day=self._date.day,
                       date_pattern='yyyy-mm-dd',
                       showweeknumbers=False,
                       firstweekday='monday',
                       font="Arial 11",
                       cursor="hand2")
        cal.pack(fill="both", expand=True, padx=8, pady=8)

        def confirm():
            selected = cal.get_date()
            self._date = datetime.strptime(selected, "%Y-%m-%d").date()
            self._btn.configure(text=self._fmt())
            top.destroy()
            if self._callback:
                self._callback(self._date)

        ctk.CTkButton(top, text="✔  Confirm", height=32,
                      fg_color="#27AE60", hover_color="#1E8449",
                      font=("Arial", 12, "bold"),
                      command=confirm).pack(fill="x", padx=8, pady=(0, 8))

    def get_date(self):
        return self._date

    def set_date(self, d):
        self._date = d
        self._btn.configure(text=self._fmt())

    def on_change(self, callback):
        self._callback = callback


# ── Main Schedule Frame ───────────────────────────────────────────────────────
class LeaderSchedule(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user

        today = datetime.today()
        self.current_month_start = today.replace(day=1).date()
        next_month = today.replace(day=28) + timedelta(days=4)
        self.current_month_end = (next_month - timedelta(days=next_month.day)).date()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.setup_ui()
        self.auto_generate_monthly_schedule()
        self.refresh_view()

    # ── UI Setup ──────────────────────────────────────────────────────────────
    def setup_ui(self):
        self.wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self.wrapper.grid(row=0, column=0, sticky="nsew", padx=80, pady=5)

        # ── Page Title ────────────────────────────────────────────────────────
        title_row = ctk.CTkFrame(self.wrapper, fg_color="transparent")
        title_row.pack(fill="x", padx=10, pady=(14, 4))

        team_id = self.user.get('team_id', '—')
        ctk.CTkLabel(
            title_row,
            text=f"🗓  Team {team_id}  ·  WFH Schedule Manager",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(side="left")

        # ── Filter Card ───────────────────────────────────────────────────────
        filter_card = ctk.CTkFrame(
            self.wrapper, corner_radius=14,
            fg_color="#141E2B",
            border_width=1, border_color="#253545"
        )
        filter_card.pack(fill="x", padx=10, pady=(4, 10))

        inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)

        # ── Date pickers ──────────────────────────────────────────────────────
        def _lbl(parent, text):
            ctk.CTkLabel(parent, text=text,
                         font=("Arial", 11),
                         text_color="#8899AA").pack(side="left", padx=(0, 4))

        _lbl(inner, "From")
        self.start_cal = DatePickerButton(inner, initial_date=self.current_month_start)
        self.start_cal.pack(side="left", padx=(0, 16))

        _lbl(inner, "To")
        self.end_cal = DatePickerButton(inner, initial_date=self.current_month_end)
        self.end_cal.pack(side="left", padx=(0, 24))

        # ── Separator ─────────────────────────────────────────────────────────
        sep = ctk.CTkFrame(inner, width=1, height=32, fg_color="#2A3A4A")
        sep.pack(side="left", padx=(0, 20))

        # ── Name filter ───────────────────────────────────────────────────────
        _lbl(inner, "Member")
        self.name_filter = ctk.CTkEntry(
            inner, placeholder_text="Search name…",
            width=150, height=36,
            corner_radius=8,
            border_color="#3D5166", border_width=1,
            fg_color="#1E2A3A",
            font=("Arial", 12)
        )
        self.name_filter.pack(side="left", padx=(0, 16))

        # ── Status dropdown ───────────────────────────────────────────────────
        _lbl(inner, "Status")
        self.status_filter = ctk.CTkComboBox(
            inner, values=["All", "Office", "WFH"],
            width=110, height=36,
            corner_radius=8,
            border_color="#3D5166", border_width=1,
            fg_color="#1E2A3A",
            button_color="#2C3E50",
            font=("Arial", 12)
        )
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=(0, 24))

        # ── Action buttons ────────────────────────────────────────────────────
        def _btn(parent, text, color, hover, cmd, width=100):
            b = ctk.CTkButton(
                parent, text=text, width=width, height=36,
                corner_radius=9,
                font=("Arial", 12, "bold"),
                fg_color=color, hover_color=hover,
                command=cmd
            )
            b.pack(side="left", padx=4)
            return b

        _btn(inner, "🔍  Filter",  "#2471A3", "#1A5276", self.refresh_view)
        _btn(inner, "✖  Clear",   "#566573", "#424949", self.clear_filters, width=90)
        _btn(inner, "📄  Export", "#C0392B", "#922B21", self.export_to_pdf, width=100)

        # ── List header ───────────────────────────────────────────────────────
        list_header = ctk.CTkFrame(self.wrapper, fg_color="transparent")
        list_header.pack(fill="x", padx=10, pady=(4, 2))

        ctk.CTkLabel(list_header,
                     text="Team Schedule Log",
                     font=("Arial", 14, "bold"),
                     text_color="#AABBCC").pack(side="left", padx=4)

        self.count_lbl = ctk.CTkLabel(list_header, text="",
                                      font=("Arial", 12),
                                      text_color="#566573")
        self.count_lbl.pack(side="left", padx=8)

        # ── Scroll list ───────────────────────────────────────────────────────
        self.scroll = ctk.CTkScrollableFrame(
            self.wrapper,
            fg_color="#0D1117",
            corner_radius=14,
            border_width=1,
            border_color="#1E2A3A"
        )
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # ── Auto-generate ─────────────────────────────────────────────────────────
    def auto_generate_monthly_schedule(self):
        leader_team_id = self.user.get('team_id')
        if not leader_team_id:
            return
        self.db.cursor.execute(
            "SELECT id FROM users WHERE role='member' AND team_id=%s", (leader_team_id,))
        members = self.db.cursor.fetchall()
        if not members:
            return
        try:
            cur = self.current_month_start
            while cur <= self.current_month_end:
                if cur.weekday() < 5:
                    for m in members:
                        self.db.cursor.execute(
                            "SELECT id FROM wfh_schedules WHERE user_id=%s AND schedule_date=%s",
                            (m['id'], cur))
                        if not self.db.cursor.fetchone():
                            status = random.choice(['Office', 'WFH'])
                            self.db.cursor.execute(
                                "INSERT INTO wfh_schedules (user_id,leader_id,schedule_date,status) VALUES(%s,%s,%s,%s)",
                                (m['id'], self.user['id'], cur, status))
                cur += timedelta(days=1)
            self.db.conn.commit()
        except Exception as e:
            print(f"Sync Error: {e}")

    # ── Refresh list ──────────────────────────────────────────────────────────
    def refresh_view(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        leader_team_id = self.user.get('team_id')
        start        = self.start_cal.get_date()
        end          = self.end_cal.get_date()
        name_search  = f"%{self.name_filter.get()}%"
        status_search = self.status_filter.get()
        today_date   = datetime.today().date()

        query = """SELECT s.*, u.full_name
                   FROM wfh_schedules s
                   JOIN users u ON s.user_id = u.id
                   WHERE u.team_id=%s
                     AND s.schedule_date BETWEEN %s AND %s
                     AND u.full_name LIKE %s"""
        params = [leader_team_id, start, end, name_search]
        if status_search != "All":
            query += " AND s.status=%s"
            params.append(status_search)
        query += " ORDER BY s.schedule_date ASC, u.full_name ASC"

        try:
            self.db.cursor.execute(query, tuple(params))
            rows = self.db.cursor.fetchall()

            self.count_lbl.configure(text=f"({len(rows)} records)")

            # Group by date
            from itertools import groupby
            for date_val, group in groupby(rows, key=lambda r: r['schedule_date']):
                group = list(group)
                is_today = date_val == today_date

                # ── Date separator row ─────────────────────────────────────
                date_sep = ctk.CTkFrame(self.scroll, fg_color="transparent")
                date_sep.pack(fill="x", padx=8, pady=(8, 1))

                day_str  = date_val.strftime("%A")
                date_str = date_val.strftime("%d %b %Y")
                badge_color = "#E67E22" if is_today else "#2C3E50"
                badge_text  = f"  {date_str}  ·  {day_str}{'  ← TODAY' if is_today else ''}  "

                ctk.CTkLabel(
                    date_sep,
                    text=badge_text,
                    font=("Arial", 11, "bold"),
                    text_color="white",
                    fg_color=badge_color,
                    corner_radius=6,
                    padx=6, pady=2
                ).pack(side="left")

                # ── Member cards under that date ───────────────────────────
                for r in group:
                    is_wfh = r['status'] == 'WFH'
                    accent = "#F39C12" if is_today else ("#3498DB" if is_wfh else "#27AE60")

                    # Card — compact, with colored left border
                    card = ctk.CTkFrame(
                        self.scroll,
                        corner_radius=8,
                        fg_color="#151C28",
                        border_width=1,
                        border_color=accent
                    )
                    card.pack(fill="x", pady=1, padx=10)

                    # ── Left: Avatar ──────────────────────────────────────
                    name       = r['full_name']
                    initials   = "".join([n[0] for n in name.split()[:2]]).upper()
                    avatar_clr = "#1A3A5C" if is_wfh else "#1A4032"

                    avatar = ctk.CTkFrame(card, width=34, height=34,
                                          corner_radius=17, fg_color=avatar_clr,
                                          border_width=2, border_color=accent)
                    avatar.pack(side="left", padx=(10, 0), pady=6)
                    avatar.pack_propagate(False)
                    ctk.CTkLabel(avatar, text=initials,
                                 font=("Arial", 11, "bold"),
                                 text_color=accent).pack(expand=True)

                    # ── Middle: Name + sub info ───────────────────────────
                    info = ctk.CTkFrame(card, fg_color="transparent")
                    info.pack(side="left", fill="both", expand=True, padx=10, pady=6)

                    ctk.CTkLabel(info, text=name,
                                 font=("Arial", 12, "bold"),
                                 text_color="#E8EDF2").pack(anchor="w")

                    emp_id = r.get('employee_id', '')
                    sub_text = f"ID: {emp_id}" if emp_id else "Team Member"
                    ctk.CTkLabel(info, text=sub_text,
                                 font=("Arial", 9),
                                 text_color="#4A5568").pack(anchor="w")

                    # ── Right: Status pill + edit icon ────────────────────
                    right = ctk.CTkFrame(card, fg_color="transparent")
                    right.pack(side="right", padx=(0, 10), pady=6)

                    pill_bg   = "#1A3A5C" if is_wfh else "#1A4032"
                    pill_text = "#5DADE2" if is_wfh else "#58D68D"
                    status_icon = "🏠" if is_wfh else "🏢"

                    ctk.CTkLabel(
                        right,
                        text=f" {status_icon} {r['status']} ",
                        font=("Arial", 11, "bold"),
                        text_color=pill_text,
                        fg_color=pill_bg,
                        corner_radius=6,
                        padx=6, pady=2
                    ).pack(side="left", padx=(0, 6))

                    ctk.CTkButton(
                        right,
                        text="✎",
                        width=30, height=30,
                        corner_radius=8,
                        font=("Arial", 13),
                        fg_color="transparent",
                        hover_color="#1E2A3A",
                        text_color="#4A5568",
                        text_color_disabled="#2A3548",
                        command=lambda row=r: self.open_edit_popup(row)
                    ).pack(side="left")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ── Edit popup ────────────────────────────────────────────────────────────
    def open_edit_popup(self, row_data):
        popup = ctk.CTkToplevel(self)
        popup.title("Update Schedule Status")
        popup.geometry("360x240")
        popup.resizable(False, False)
        popup.attributes('-topmost', True)
        popup.configure(fg_color="#0D1117")

        ctk.CTkLabel(popup, text="✏  Edit Schedule",
                     font=("Arial", 16, "bold"),
                     text_color="white").pack(pady=(20, 4))

        ctk.CTkLabel(popup, text=f"{row_data['full_name']}  ·  {row_data['schedule_date']}",
                     font=("Arial", 12),
                     text_color="#8899AA").pack()

        ctk.CTkFrame(popup, height=1, fg_color="#1E2A3A").pack(fill="x", padx=20, pady=12)

        status_var = ctk.StringVar(value=row_data['status'])
        seg = ctk.CTkSegmentedButton(
            popup, values=["Office", "WFH"],
            variable=status_var,
            font=("Arial", 13, "bold"),
            selected_color="#2471A3",
            unselected_color="#1E2A3A",
            fg_color="#141E2B"
        )
        seg.pack(pady=8)

        def save_change():
            try:
                self.db.cursor.execute(
                    "UPDATE wfh_schedules SET status=%s WHERE id=%s",
                    (status_var.get(), row_data['id']))
                self.db.conn.commit()
                popup.destroy()
                self.refresh_view()
            except Exception as e:
                messagebox.showerror("Update Fail", str(e))

        ctk.CTkButton(popup, text="✔  Save Change",
                      height=38, corner_radius=10,
                      font=("Arial", 13, "bold"),
                      fg_color="#27AE60", hover_color="#1E8449",
                      command=save_change).pack(pady=(12, 0), padx=30, fill="x")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def clear_filters(self, refresh=True):
        self.start_cal.set_date(self.current_month_start)
        self.end_cal.set_date(self.current_month_end)
        self.name_filter.delete(0, 'end')
        self.status_filter.set("All")
        if refresh:
            self.refresh_view()

    # ── PDF Export ────────────────────────────────────────────────────────────
    def export_to_pdf(self):
        leader_team_id = self.user.get('team_id')
        start = self.start_cal.get_date()
        end   = self.end_cal.get_date()

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"Team_{leader_team_id}_Schedule.pdf"
        )
        if not file_path:
            return
        try:
            self.db.cursor.execute(
                """SELECT s.schedule_date, u.full_name, s.status
                   FROM wfh_schedules s JOIN users u ON s.user_id=u.id
                   WHERE u.team_id=%s AND s.schedule_date BETWEEN %s AND %s
                   ORDER BY s.schedule_date ASC""",
                (leader_team_id, start, end))
            data = self.db.cursor.fetchall()

            doc      = SimpleDocTemplate(file_path, pagesize=letter)
            styles   = getSampleStyleSheet()
            elements = [
                Paragraph(f"Team {leader_team_id} Work Schedule", styles['Title']),
                Paragraph(f"Period: {start} to {end}", styles['Normal']),
                Spacer(1, 15)
            ]
            table_data = [["Date", "Member Name", "Status"]]
            for r in data:
                day = r['schedule_date'].strftime('%a')
                table_data.append([f"{r['schedule_date']} ({day})", r['full_name'], r['status']])

            t = Table(table_data, colWidths=[130, 200, 100])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR',  (0, 0), (-1, 0), colors.whitesmoke),
                ('GRID',       (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            elements.append(t)
            doc.build(elements)
            messagebox.showinfo("Export Successful", "PDF saved successfully.")
        except Exception as e:
            messagebox.showerror("Export Error", f"PDF Error: {e}")