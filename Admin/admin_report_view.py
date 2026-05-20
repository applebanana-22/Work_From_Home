import customtkinter as ctk
from database import Database
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
import tkinter as tk
from fpdf import FPDF
from tkcalendar import Calendar
from collections import defaultdict

# ── Reusable modern date-picker ──────────────────────────────────────────────
class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None):
        super().__init__(master, fg_color="transparent")

        self._date = initial_date or datetime.today().date()
        self._open = False

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

        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color=("#FFFFFF", "#141E2B"),
            corner_radius=12,
            border_width=1,
            border_color=("#CCCCCC", "#2A3A4A")
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

class DailyReportFrame(ctk.CTkFrame):
    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.db = Database()
        self.user = user
        self.configure(fg_color="transparent")

        today = datetime.today().date()
        self.start_date = today
        self.end_date = today
        self.member_search = ""
        self.selected_team = "All Teams"          # bottom report filter
        self.count_selected_team = "All Teams"   # top count filter

        self.team_options = ["All Teams"]
        self.team_map = {"All Teams": None}
        self.load_team_options()

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_reports_list()

    def load_team_options(self):
        try:
            teams = self.db.get_all_teams() or []
            for team in teams:
                team_name = team.get('team_name')
                team_id = team.get('team_id')
                if team_name:
                    self.team_options.append(team_name)
                    self.team_map[team_name] = team_id
        except Exception:
            pass

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_reports_list(self):
        content_padx = 80
        self.clear_container()

        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=content_padx, pady=14)

        ctk.CTkLabel(
            header,
            text="📊 Daily Report",
            font=("Arial", 20, "bold"),
            text_color=("#333333", "#FFFFFF")
        ).pack(side="left")

        counts_bar = ctk.CTkFrame(
            self.container,
            corner_radius=14,
            fg_color=("#F9F9F9", "#1E1E1E"),
            border_width=1,
            border_color=("#E0E0E0", "#2C2C2C")
        )
        counts_bar.pack(fill="x", padx=content_padx, pady=(0, 10))

        left_wrap = ctk.CTkFrame(counts_bar, fg_color="transparent")
        left_wrap.pack(anchor="w", padx=18, pady=14)

        top_row = ctk.CTkFrame(left_wrap, fg_color="transparent")
        top_row.pack(anchor="w", pady=(0, 6))

        self.count_date = DatePickerButton(
            top_row,
            initial_date=datetime.today().date()
        )

        self.count_date.pack(side="left", padx=(0, 8))

        # keep first date picker selectable
        self.count_date.btn.configure(
            command=self.count_date.toggle
        )

        # Team selector next to the counts date
        self.count_team_menu = ctk.CTkOptionMenu(
            top_row,
            values=self.team_options,
            command=self.set_count_team_filter,
            width=120,
            height=28,
            corner_radius=8,
            fg_color=("#FFFFFF", "#2E2E2E"),
            button_color=("#FFFFFF", "#2E2E2E"),
            text_color=("#000000", "#FFFFFF"),
            button_hover_color=("#E5E5E5", "#2A2A2A")
        )
        self.count_team_menu.set(self.count_selected_team)
        self.count_team_menu.pack(side="left", padx=(8, 8))

        # Filter and Clear buttons
        self.count_filter_btn = ctk.CTkButton(
            top_row,
            text="🔍 Filter",
            width=90,
            height=32,
            corner_radius=8,
            fg_color="#2471A3",
            hover_color="#1A5276",
            font=("Arial", 11, "bold"),
            command=self.apply_counts_filter
        )
        self.count_filter_btn.pack(side="left", padx=(6, 4))

        self.count_clear_btn = ctk.CTkButton(
            top_row,
            text="✖ Clear",
            width=80,
            height=32,
            corner_radius=8,
            fg_color="#566573",
            hover_color="#424949",
            font=("Arial", 11, "bold"),
            command=self.clear_counts
        )
        self.count_clear_btn.pack(side="left")
        def create_small_card(parent, title, color, command=None):

            card = ctk.CTkFrame(
                parent,
                width=140,
                height=72,
                corner_radius=15,
                fg_color=("#FFFFFF", "#2B2B2B"),
                border_width=1,
                border_color=("#DDDDDD", "#3A3A3A")
            )

            card.pack(side="left", padx=(0, 16))
            card.pack_propagate(False)

            title_lbl = ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 12),
                text_color=("#666666", "#888888")
            )

            title_lbl.pack(pady=(10, 0))

            value_lbl = ctk.CTkLabel(
                card,
                text="0",
                font=("Arial", 20, "bold"),
                text_color=color,
                cursor="hand2" if command else ""
            )

            value_lbl.pack(pady=(2, 0))

            if command:
                title_lbl.bind("<Button-1>", lambda e: command())
                value_lbl.bind("<Button-1>", lambda e: command())
                card.bind("<Button-1>", lambda e: command())

            return value_lbl

        stats_wrap = ctk.CTkFrame(left_wrap, fg_color="transparent")
        stats_wrap.pack(anchor="w")

        self.total_lbl = create_small_card(stats_wrap, "Total Members", "#3498DB")
        self.submitted_lbl = create_small_card(stats_wrap, "Submitted", "#27AE60", lambda: self.show_member_list(True))
        self.not_submitted_lbl = create_small_card(stats_wrap, "Not Submitted", "#C0392B", lambda: self.show_member_list(False))

        filter_card = ctk.CTkFrame(
            self.container,
            corner_radius=14,
            fg_color=("#F9F9F9", "#1E1E1E"),
            border_width=1,
            border_color=("#E0E0E0", "#2C2C2C")
        )
        filter_card.pack(fill="x", padx=content_padx, pady=(4, 10))
        inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        inner.pack(fill="x", padx=8, pady=8)

        def _lbl(parent, text):
            ctk.CTkLabel(parent, text=text,
                         font=("Arial", 11, "bold"),
                         text_color=("#555555", "#FFFFFF")).pack(side="left", padx=(0, 4))

        _lbl(inner, "From")
        self.start_cal = DatePickerButton(inner, initial_date=self.start_date)
        self.start_cal.pack(side="left", padx=(0, 8))

        _lbl(inner, "To")
        self.end_cal = DatePickerButton(inner, initial_date=self.end_date)
        self.end_cal.pack(side="left", padx=(0, 12))

        # team dropdown (no label to save space)
        self.team_menu = ctk.CTkOptionMenu(
            inner,
            values=self.team_options,
            command=self.set_report_team_filter,
            width=120,
            height=28,
            corner_radius=8,
            fg_color=("#FFFFFF", "#2E2E2E"),
            button_color=("#FFFFFF", "#2E2E2E"),
            text_color=("#000000", "#FFFFFF"),
            button_hover_color=("#E5E5E5", "#2A2A2A")
        )
        self.team_menu.set(self.selected_team)
        self.team_menu.pack(side="left", padx=(0, 8))

        _lbl(inner, "Member")
        self.member_entry = ctk.CTkEntry(
            inner,
            placeholder_text="Search name",
            width=89,
            height=36,
            corner_radius=8,
            border_color=("#CCCCCC", "#2C2C2C"),
            border_width=1,
            fg_color=("#FFFFFF", "#1E1E1E"),
            text_color=("#000000", "#FFFFFF"),
            font=("Arial", 12)
        )
        self.member_entry.pack(side="left", padx=(0, 10), pady=2)

        def _btn(parent, text, color, hover, cmd, width=70):
            b = ctk.CTkButton(
                parent, text=text, width=width, height=32,
                corner_radius=9, font=("Arial", 11, "bold"),
                fg_color=color, hover_color=hover, command=cmd
            )
            b.pack(side="left", padx=4)
            return b

        _btn(inner, "🔍 Filter", "#2471A3", "#1A5276", self.refresh_view, width=74)
        _btn(inner, "✖ Clear", "#566573", "#424949", self.clear_filters, width=70)
        _btn(inner, "📄 Export", "#C0392B", "#922B21", self.export_to_pdf, width=72)

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
        self.refresh_counts()

    def set_report_team_filter(self, value):
        self.selected_team = value

    def set_count_team_filter(self, value):
        self.count_selected_team = value

    def refresh_view(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        if start > end:
            messagebox.showerror("Invalid Date", "Start date cannot be later than End date.")
            return

        member_search = self.member_entry.get().strip()
        team_id = self.team_map.get(self.selected_team)

        query = '''SELECT u.full_name, dr.report_date, dr.today_work,
                dr.tomorrow_work, dr.problems_issues, dr.shared_matters,
                t.team_name
            FROM users u
            JOIN daily_reports dr ON u.id = dr.user_id
            LEFT JOIN teams t ON u.team_id = t.team_id
            WHERE u.role='member' AND dr.report_date BETWEEN %s AND %s'''
        params = [start, end]

        if team_id is not None:
            query += " AND u.team_id = %s"
            params.append(team_id)

        if member_search:
            query += " AND u.full_name LIKE %s"
            params.append(f"%{member_search}%")

        query += " ORDER BY dr.report_date DESC, u.full_name ASC, dr.created_at DESC"

        try:
            self.db.cursor.execute(query, tuple(params))
            rows = self.db.cursor.fetchall()

            grouped = defaultdict(list)
            for r in rows:
                key = (r['report_date'], r['full_name'])
                grouped[key].append(r)

            self.count_lbl.configure(text=f"({len(grouped)} records)")
            if not grouped:
                ctk.CTkLabel(
                    self.scroll,
                    text="No records found.",
                    font=("Arial", 15, "bold"),
                    text_color=("#666666", "#AAAAAA")
                ).pack(
                    pady=20
                )
                return

            last_date = None
            today_date = datetime.today().date()
            for (date_val, member), tasks in grouped.items():
                if last_date != date_val:
                    date_sep = ctk.CTkFrame(self.scroll, fg_color="transparent")
                    date_sep.pack(fill="x", padx=8, pady=(8, 1))
                    day_str = date_val.strftime("%A")
                    date_str = date_val.strftime("%d %b %Y")
                    badge_color = "#E67E22" if date_val == today_date else ("#BDC3C7", "#2C3E50")
                    badge_text = f"  {date_str}  ·  {day_str}{'  ← TODAY' if date_val == today_date else ''}  "
                    ctk.CTkLabel(
                        date_sep, text=badge_text,
                        font=("Arial", 11, "bold"),
                        text_color=("black", "white"),
                        fg_color=badge_color, corner_radius=6,
                        padx=6, pady=2
                    ).pack(side="left")
                    last_date = date_val

                team_name = tasks[0].get('team_name') or "Unknown Team"
                card = ctk.CTkFrame(self.scroll,
                    corner_radius=12,
                    fg_color=("#FFFFFF", "#1E1E1E"),
                    border_width=1,
                    border_color=("#E0E0E0", "#2C2C2C")
                )
                card.pack(fill="x", pady=1, padx=10)
                info = ctk.CTkFrame(card, fg_color="transparent")
                info.pack(side="left", fill="both", expand=True, padx=10, pady=6)

                ctk.CTkLabel(
                    info,
                    text=f"{member} ({team_name})",
                    font=("Arial", 12, "bold"),
                    text_color=("#333333", "#E8EDF2")
                ).pack(anchor="w", pady=(0, 4))

                preview = tasks[0].get('today_work', "") if tasks else ""
                preview = preview or "No details yet."
                lines = preview.splitlines()
                if len(lines) > 2:
                    preview = "\n".join(lines[:2]) + " ..."
                elif len(preview) > 120:
                    preview = preview[:120] + "..."

                ctk.CTkLabel(
                    info,
                    text=preview,
                    wraplength=650,
                    justify="left",
                    anchor="w",
                    text_color=("#555555", "#AAB7C4")
                ).pack(anchor="w", fill="x", pady=(4, 0))

                btn_frame = ctk.CTkFrame(card, fg_color="transparent")
                btn_frame.pack(side="right", padx=12, pady=6)

                ctk.CTkButton(
                    btn_frame,
                    text="View",
                    width=60,
                    height=30,
                    corner_radius=8,
                    font=("Arial", 12, "bold"),
                    fg_color="#2E5B9A",
                    hover_color="#1F4E8C",
                    command=lambda tlist=tasks, m=member, d=date_val: self.open_detail_with_state(m, d, tlist)
                ).pack()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_counts(self):
        try:
            sel_date = self.count_date.get_date()
        except Exception:
            sel_date = datetime.today().date()

        try:

            # Apply team filter if selected
            team_id = self.team_map.get(self.count_selected_team)

            if team_id is None:
                q_total = "SELECT COUNT(*) AS cnt FROM users WHERE role='member'"
                self.db.cursor.execute(q_total)
                total = self.db.cursor.fetchone().get('cnt', 0) or 0

                q_sub = '''SELECT COUNT(DISTINCT u.id) AS cnt FROM users u
                           JOIN daily_reports dr ON u.id=dr.user_id
                           WHERE u.role='member' AND dr.report_date=%s'''
                self.db.cursor.execute(q_sub, (sel_date,))
                submitted = self.db.cursor.fetchone().get('cnt', 0) or 0
            else:
                q_total = "SELECT COUNT(*) AS cnt FROM users WHERE role='member' AND team_id=%s"
                self.db.cursor.execute(q_total, (team_id,))
                total = self.db.cursor.fetchone().get('cnt', 0) or 0

                q_sub = '''SELECT COUNT(DISTINCT u.id) AS cnt FROM users u
                           JOIN daily_reports dr ON u.id=dr.user_id
                           WHERE u.role='member' AND dr.report_date=%s AND u.team_id=%s'''
                self.db.cursor.execute(q_sub, (sel_date, team_id))
                submitted = self.db.cursor.fetchone().get('cnt', 0) or 0

            not_sub = max(0, total - submitted)
            self.total_lbl.configure(text=str(total))
            self.submitted_lbl.configure(text=str(submitted))
            self.not_submitted_lbl.configure(text=str(not_sub))
        except Exception as e:
            print("Error refreshing counts:", e)

    def apply_counts_filter(self):
        # ONLY refresh top 3 count cards
        # DO NOT affect report history filters below
        self.refresh_counts()

    def show_member_list(self, submitted=True):
        try:
            sel_date = self.count_date.get_date()
        except Exception:
            sel_date = datetime.today().date()

        team_id = self.team_map.get(self.count_selected_team)

        if submitted:
            q = '''SELECT u.full_name, t.team_name FROM users u
                   LEFT JOIN teams t ON u.team_id=t.team_id
                   JOIN daily_reports dr ON u.id=dr.user_id
                   WHERE u.role='member' AND dr.report_date=%s'''
            params = [sel_date]
            if team_id is not None:
                q += " AND u.team_id=%s"
                params.append(team_id)
            q += " ORDER BY u.full_name ASC"
            title = f"Members who submitted on {sel_date}"
        else:
            q = '''SELECT u.full_name, t.team_name FROM users u
                   LEFT JOIN teams t ON u.team_id=t.team_id
                   WHERE u.role='member' AND u.id NOT IN
                   (SELECT user_id FROM daily_reports WHERE report_date=%s)'''
            params = [sel_date]
            if team_id is not None:
                q += " AND u.team_id=%s"
                params.append(team_id)
            q += " ORDER BY u.full_name ASC"
            title = f"Members who not Submitted on {sel_date}"

        try:
            self.db.cursor.execute(q, params)
            rows = self.db.cursor.fetchall() or []

            self.clear_container()
            content_padx = 80

            top = ctk.CTkFrame(self.container, fg_color="transparent")
            top.pack(fill="x", padx=content_padx, pady=20)

            ctk.CTkButton(
                top,
                text="← Back",
                width=80,
                fg_color=("#DBDBDB", "#333333"),
                text_color=("black", "white"),
                hover_color=("#CFCFCF", "#444444"),
                corner_radius=8,
                command=self.back_to_list
            ).pack(side="left")

            ctk.CTkLabel(
                top,
                text=title,
                font=("Arial", 20, "bold"),
                text_color=("black", "white")
            ).pack(side="left", padx=20)

            # MAIN CARD
            main_card = ctk.CTkFrame(
                self.container,
                corner_radius=14,
                fg_color=("#F0F0F0", "#252525"),
                border_width=1,
                border_color=("#DDDDDD", "#333333")
            )

            main_card.pack(
                fill="both",
                expand=True,
                padx=content_padx,
                pady=(0, 20)
            )

            # INNER LIST BOX
            list_frame = ctk.CTkScrollableFrame(
                main_card,
                fg_color=("#FFFFFF", "#1E1E26"),
                corner_radius=12,
                border_width=1,
                border_color=("#DDDDDD", "#333333")
            )

            list_frame.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=20
            )

            if not rows:
                ctk.CTkLabel(list_frame, text="No members found.", font=("Arial", 12)).pack(anchor="w", padx=8, pady=6)
            else:
                for i, row in enumerate(rows, start=1):
                    team_name = row.get('team_name') or "Unknown Team"
                    ctk.CTkLabel(
                        list_frame,
                        text=f"{i}. {row.get('full_name')} ({team_name})",
                        font=("Arial", 12)
                    ).pack(anchor="w", padx=8, pady=4)

            self.refresh_counts()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_detail_with_state(self, member, date_val, tasks):
        self.start_date = self.start_cal.get_date()
        self.end_date = self.end_cal.get_date()
        self.member_search = self.member_entry.get()
        self.selected_team = self.team_menu.get()
        team_name = tasks[0].get("team_name", "No Team") if tasks else "No Team"
        self.show_member_detail(member, team_name, date_val, tasks)

    def show_member_detail(self, member_name, team_name, date_val, tasks):
        self.clear_container()

        content_padx = 80
        top = ctk.CTkFrame(self.container, fg_color="transparent")
        top.pack(fill="x", padx=content_padx, pady=20)

        ctk.CTkButton(
            top,
            text="← Back",
            width=80,
            fg_color=("#DBDBDB", "#333333"),
            text_color=("black", "white"),
            hover_color=("#CFCFCF", "#444444"),
            corner_radius=8,
            command=self.back_to_list
        ).pack(side="left")

        ctk.CTkLabel(
            top,
            text=f"{member_name} ({team_name}) - {date_val}",
            font=("Arial", 20, "bold"),
            text_color=("black", "white")
        ).pack(side="left", padx=20)

        self.form_scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.form_scroll.pack(fill="both", expand=True, padx=content_padx, pady=10)

        COLOR_CONTAINER_BG = ("#F0F0F0", "#252525")
        COLOR_TEXT_MAIN = ("#1A1A1A", "#E8EDF2")

        for r in tasks:
            def add_readonly_section(title, content):
                content = content or "-"
                lines = content.split("\n")
                total_lines = 0
                for line in lines:
                    wrapped = max(1, (len(line) // 85) + 1)
                    total_lines += wrapped
                textbox_height = max(45, total_lines * 24)
                section = ctk.CTkFrame(self.form_scroll, fg_color=COLOR_CONTAINER_BG, corner_radius=10)
                section.pack(fill="x", pady=8, padx=5)
                ctk.CTkLabel(section, text=title, font=("Arial", 14, "bold"), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=15, pady=(12, 6))
                text_box = ctk.CTkTextbox(section, height=int(textbox_height), fg_color=("#FFFFFF", "#1e1e26"), border_width=1, border_color=("#DBDBDB", "#333333"), text_color=("black", "white"), wrap="word")
                text_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
                text_box.insert("1.0", content)
                text_box.configure(state="disabled")

            add_readonly_section("Today's Work Detail", r.get('today_work', ""))
            add_readonly_section("Tomorrow's Work Schedule", r.get('tomorrow_work', ""))
            add_readonly_section("Problems / Issues", r.get('problems_issues', ""))
            add_readonly_section("Shared Matters", r.get('shared_matters', ""))

    def back_to_list(self):
        self.show_reports_list()
        self.start_cal.set_date(self.start_date)
        self.end_cal.set_date(self.end_date)
        self.team_menu.set(self.selected_team)
        self.member_entry.delete(0, "end")
        self.member_entry.insert(0, self.member_search)
        self.refresh_view()

    def clear_filters(self):
        today = datetime.today().date()
        self.start_date = today
        self.end_date = today
        self.member_search = ""
        self.selected_team = "All Teams"
        # reset count selector if present
        try:
            if hasattr(self, 'count_date'):
                self.count_date.set_date(today)
        except Exception:
            pass
        self.show_reports_list()

    def clear_counts(self):
        today = datetime.today().date()
        try:
            if hasattr(self, 'count_date'):
                self.count_date.set_date(today)

            self.count_selected_team = "All Teams"

            if hasattr(self, 'count_team_menu'):
                self.count_team_menu.set("All Teams")

        except Exception:
            pass
        # ONLY refresh top counts
        self.refresh_counts()
    
    def export_to_pdf(self):
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        member_search = self.member_entry.get().strip()
        team_id = self.team_map.get(self.selected_team)

        query = '''
        SELECT
            dr.report_date,
            u.full_name,
            t.team_name,
            dr.today_work,
            dr.tomorrow_work,
            dr.problems_issues,
            dr.shared_matters
            FROM users u
            JOIN daily_reports dr ON u.id = dr.user_id
            LEFT JOIN teams t ON u.team_id = t.team_id
            WHERE u.role='member'
            AND dr.report_date BETWEEN %s AND %s
        '''
        params = [start, end]

        if team_id is not None:
            query += " AND u.team_id = %s"
            params.append(team_id)

        if member_search:
            query += " AND u.full_name LIKE %s"
            params.append(f"%{member_search}%")

        query += '''
            ORDER BY
            dr.report_date DESC,
            u.full_name ASC,
            dr.created_at ASC
        '''

        try:
            self.db.cursor.execute(query, tuple(params))
            rows = self.db.cursor.fetchall()
            if not rows:
                messagebox.showinfo("No Data", "No reports found.")
                return

            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"Admin_Daily_Reports.pdf"
            )
            if not file_path:
                return

            class PDF(FPDF):
                def header(self):
                    self.set_font("Arial", "B", 20)
                    self.cell(0, 12, "Admin Daily Reports", ln=True, align="C")
                    self.ln(4)
                    self.set_font("Arial", "B", 11)
                    self.cell(14, 8, "Date :", ln=0)
                    self.set_font("Arial", "", 11)
                    self.cell(0, 8, f"{self.start_date} ~ {self.end_date}", ln=True)
                    self.ln(4)
                    self.set_font("Arial", "B", 10)
                    headers = ["Date", "Name", "Team", "Today's Work Detail", "Tomorrow's Work Schedule", "Problems/Issues", "Shared Matters"]
                    widths = self.col_widths
                    for i, header in enumerate(headers):
                        self.cell(widths[i], 12, header, border=1, align="C")
                    self.ln()

            pdf = PDF("L", "mm", "A4")
            pdf.start_date = start
            pdf.end_date = end
            pdf.col_widths = [28, 32, 28, 52, 52, 38, 38]
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            body_font_size = 8
            pdf.set_font("Arial", "", body_font_size)
            line_height = 5

            def split_text(text, width):
                if not text:
                    return ["-"]
                pdf.set_font("Arial", "", body_font_size)
                lines = []
                for paragraph in str(text).split("\n"):
                    words = paragraph.split(" ")
                    current_line = ""
                    for word in words:
                        test_line = (current_line + " " + word).strip()
                        if pdf.get_string_width(test_line) <= width - 2:
                            current_line = test_line
                        else:
                            if current_line:
                                lines.append(current_line)
                            current_line = word
                    if current_line:
                        lines.append(current_line)
                return lines if lines else ["-"]

            for r in rows:
                cells = [
                    str(r['report_date']),
                    str(r.get('full_name') or "-"),
                    str(r.get('team_name') or "-"),
                    str(r.get('today_work') or "-"),
                    str(r.get('tomorrow_work') or "-"),
                    str(r.get('problems_issues') or "-"),
                    str(r.get('shared_matters') or "-")
                ]
                split_cells = []
                max_lines = 1
                for i, text in enumerate(cells):
                    lines = split_text(text, pdf.col_widths[i])
                    split_cells.append(lines)
                    max_lines = max(max_lines, len(lines))
                row_height = (max_lines * line_height) + 3
                if pdf.get_y() + row_height > 190:
                    pdf.add_page()
                    pdf.set_font("Arial", "", body_font_size)
                x = pdf.get_x(); y = pdf.get_y()
                for width in pdf.col_widths:
                    pdf.rect(x, y, width, row_height)
                    x += width
                x = pdf.l_margin
                for i, lines in enumerate(split_cells):
                    current_y = y + 2
                    for line in lines:
                        pdf.set_xy(x + 2, current_y)
                        pdf.cell(pdf.col_widths[i] - 4, line_height, line, border=0)
                        current_y += line_height
                    x += pdf.col_widths[i]
                pdf.set_y(y + row_height)

            pdf.output(file_path)
            messagebox.showinfo("Success", "PDF exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
