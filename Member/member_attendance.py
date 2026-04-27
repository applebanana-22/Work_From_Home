import customtkinter as ctk
from database import Database
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox, ttk
from xml.sax.saxutils import escape
from tkcalendar import Calendar
import tkinter as tk
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._date = initial_date or datetime.today().date()
        self._callback = None

        self._field = ctk.CTkFrame(
            self,
            width=140,
            height=32,
            corner_radius=10,
            fg_color=("#F9F9FA", "#343638"),
            border_width=0,
        )
        self.configure(
            width=140,
            height=32,
            corner_radius=10,
            fg_color="transparent",
            border_width=1,
            border_color=("#979DA2", "#565B5E"),
        )
        self._field.pack_propagate(False)
        self._field.pack(fill="both", expand=True)

        self._date_lbl = ctk.CTkLabel(
            self._field,
            text=self._fmt(),
            font=("Arial", 12),
            text_color=("#1A1A1A", "#DCE4EE"),
        )
        self._date_lbl.pack(side="left", padx=(10, 0))

        self._arrow_lbl = ctk.CTkLabel(
            self._field,
            text="▼",
            font=("Arial", 11),
            text_color="#A7B4C2",
        )
        self._arrow_lbl.pack(side="right", padx=(0, 10))

        for w in (self._field, self._date_lbl, self._arrow_lbl):
            w.bind("<Button-1>", self._open_picker)

    def _fmt(self):
        return self._date.strftime('%Y-%m-%d')

    def _open_picker(self, _event=None):
        top = tk.Toplevel(self)
        top.overrideredirect(True)
        top.resizable(False, False)
        top.attributes("-topmost", True)
        top.configure(bg="#1A1A2E")

        x = self._field.winfo_rootx()
        y = self._field.winfo_rooty() + self._field.winfo_height() + 4
        top.geometry(f"280x280+{x}+{y}")

        style = ttk.Style(top)
        style.theme_use("clam")
        style.configure(
            "custom.Calendar",
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
            relief="flat",
        )

        cal = Calendar(
            top,
            style="custom.Calendar",
            selectmode="day",
            year=self._date.year,
            month=self._date.month,
            day=self._date.day,
            date_pattern="yyyy-mm-dd",
            showweeknumbers=False,
            firstweekday="monday",
            font="Arial 11",
            cursor="hand2",
        )
        cal.pack(fill="both", expand=True, padx=8, pady=8)

        def select_and_close(_event=None):
            selected = cal.get_date()
            self._date = datetime.strptime(selected, "%Y-%m-%d").date()
            self._date_lbl.configure(text=self._fmt())
            top.destroy()
            if self._callback:
                self._callback(self._date)

        cal.bind("<<CalendarSelected>>", select_and_close)
        top.bind("<FocusOut>", lambda _e: top.destroy())
        top.focus_force()

    def get_date(self):
        return self._date

    def set_date(self, value):
        if isinstance(value, datetime):
            value = value.date()
        self._date = value
        self._date_lbl.configure(text=self._fmt())

    def on_change(self, callback):
        self._callback = callback


class MemberAttendance(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color=("white", "#1A1A1A"))
        self.db = Database()
        self.user = user
        self.LATE_TIME = "09:00:00"

        self.month_map = {"All Months": ""}
        self.month_rows = []
        self.current_rows = []
        self.date_filter_enabled = False
        self.month_total_workdays = "-"
        self.metric_colors = {
            "work": "#27AE60",
            "leave": "#3498DB",
            "late": "#E67E22",
            "ot": "#8B5CF6",
        }

        self.setup_ui()

    # ---------------- UI ----------------
    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=100, pady=20)

        ctk.CTkLabel(
            header,
            text="Attendance & Work Summary",
            font=("Arial", 22, "bold")
        ).pack(side="left")

        # ---------------- FILTER ----------------
        filter_frame = ctk.CTkFrame(
            self,
            fg_color=("#F6F8FC", "#1F2833"),
            corner_radius=16,
            border_width=1,
            border_color=("#D6DEEB", "#3A4656"),
        )
        filter_frame.pack(fill="x", padx=100, pady=(0, 18))

        ctk.CTkLabel(filter_frame, text="Search").grid(row=0, column=0, padx=(20, 6), pady=10, sticky="w")

        self.search_entry = ctk.CTkEntry(
            filter_frame,
            width=220,
            corner_radius=10,
        )
        self.search_entry.grid(row=0, column=1, padx=6, pady=8)
        self.search_entry.bind("<KeyRelease>", lambda _e: self.load_data())

        ctk.CTkLabel(filter_frame, text="Date").grid(row=0, column=2, padx=(18, 6), pady=8, sticky="w")

        self.date_picker = DatePickerButton(filter_frame, initial_date=datetime.today().date())
        self.date_picker.grid(row=0, column=3, padx=6, pady=8)
        self.date_picker.on_change(lambda _d: self._on_date_selected())

        ctk.CTkLabel(filter_frame, text="Month").grid(row=0, column=4, padx=(18, 6), pady=8, sticky="w")

        self.month_filter = ctk.CTkComboBox(
            filter_frame,
            values=[],
            width=180,
            corner_radius=10,
            command=lambda _v: self.load_data()
        )
        self.month_filter.grid(row=0, column=5, padx=6, pady=8)

        ctk.CTkButton(
            filter_frame,
            text="Reset",
            width=78,
            fg_color="#6B7280",
            hover_color="#4B5563",
            corner_radius=10,
            command=self.reset_filters
        ).grid(row=0, column=6, padx=6, pady=8)

        ctk.CTkButton(
            filter_frame,
            text="Export PDF",
            width=98,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            corner_radius=10,
            command=self.export_pdf
        ).grid(row=0, column=7, padx=(153, 20), pady=8)

        # ---------------- STATS ----------------
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=100, pady=5)

        self.month_work_lbl = self.create_stat_card("Month Work", "0", self.metric_colors["work"])
        self.working_lbl = self.create_stat_card("Working Days", "0", self.metric_colors["work"])
        self.leave_lbl = self.create_stat_card("Leave Days", "0", self.metric_colors["leave"])
        self.late_lbl = self.create_stat_card("Late Days", "0", self.metric_colors["late"])
        self.ot_lbl = self.create_stat_card("OT Hours", "0", self.metric_colors["ot"])

        # ---------------- TABLE ----------------
        self.table_card = ctk.CTkFrame(
            self,
            fg_color=("#FFFFFF", "#1B1F24"),
            corner_radius=16,
            border_width=1,
            border_color=("#D6DEEB", "#2A3442"),
        )
        self.table_card.pack(fill="both", expand=True, padx=100, pady=10)

        header_row = ctk.CTkFrame(self.table_card, fg_color=("#9CA3AF", "#334155"))
        header_row.pack(fill="x", padx=10, pady=(10, 0))

        def h(text, w):
            return ctk.CTkLabel(header_row, text=text, width=w,
                                text_color=("#000000", "#FFFFFF"), font=("Arial", 12, "bold"))

        h("Date", 140).pack(side="left", padx=10)
        h("Check-In", 120).pack(side="left", padx=10)
        h("Check-Out", 120).pack(side="left", padx=10)
        h("OT", 100).pack(side="left", padx=10)
        h("Remark", 120).pack(side="left", padx=10)

        self.scroll = ctk.CTkScrollableFrame(self.table_card, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_months()
        self.load_data()

    # ---------------- CARD ----------------
    def create_stat_card(self, title, value, color):
        card = ctk.CTkFrame(self.stats_container, corner_radius=10, width=180)
        card.pack(side="left", padx=(25, 25))

        ctk.CTkLabel(card, text=title).pack(padx=15, pady=(5, 0))

        val_lbl = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 18, "bold"),
            text_color=color
        )
        val_lbl.pack(pady=(0, 5))

        return val_lbl

    @staticmethod
    def _current_payroll_month_key():
        today = datetime.now()
        if today.day >= 26:
            if today.month == 12:
                return f"{today.year + 1}-01"
            return f"{today.year}-{today.month + 1:02d}"
        return today.strftime("%Y-%m")

    @staticmethod
    def _calculate_month_total_workdays(month_key):
        if not month_key:
            return "-"

        payroll_month = datetime.strptime(month_key, "%Y-%m")
        end_date = payroll_month.replace(day=25).date()
        if payroll_month.month == 1:
            start_date = payroll_month.replace(year=payroll_month.year - 1, month=12, day=26).date()
        else:
            start_date = payroll_month.replace(month=payroll_month.month - 1, day=26).date()

        count = 0
        current = start_date
        while current <= end_date:
            if current.weekday() < 5:
                count += 1
            current += timedelta(days=1)

        return str(count)

    @staticmethod
    def _dash(value):
        return "-" if value in (None, "") else str(value)

    # ---------------- MONTHS ----------------
    def load_months(self):
        payroll_calc = """
            CASE
                WHEN DAY({col}) >= 26
                THEN DATE_FORMAT(DATE_ADD({col}, INTERVAL 1 MONTH), '%Y-%m')
                ELSE DATE_FORMAT({col}, '%Y-%m')
            END
        """
        sql = """
            SELECT DISTINCT ym FROM (
                SELECT {att_ym} AS ym
                FROM attendance
                WHERE user_id = %s

                UNION

                SELECT {leave_ym} AS ym
                FROM leave_requests
                WHERE user_id = %s

                UNION

                SELECT {ot_ym} AS ym
                FROM overtime_requests
                WHERE member_id = %s
                AND status IN ('Accepted', 'Approved')
            ) m
            WHERE ym IS NOT NULL
            ORDER BY ym DESC
        """.format(
            att_ym=payroll_calc.format(col="attendance_date"),
            leave_ym=payroll_calc.format(col="start_date"),
            ot_ym=payroll_calc.format(col="ot_date"),
        )

        self.db.cursor.execute(sql, (self.user["id"], self.user["id"], self.user["id"]))
        rows = self.db.cursor.fetchall()

        values = []
        self.month_map = {}

        for r in rows:
            ym = r["ym"]
            dt = datetime.strptime(ym, "%Y-%m")
            label = dt.strftime("%B %Y")
            self.month_map[label] = ym
            values.append(label)

        # apply values
        self.month_filter.configure(values=values)
        self.update_idletasks()

        # ===== CURRENT PAYROLL MONTH =====
        today = datetime.now()
        if today.day >= 26:
            if today.month == 12:
                current_ym = f"{today.year + 1}-01"
            else:
                current_ym = f"{today.year}-{today.month + 1:02d}"
        else:
            current_ym = today.strftime("%Y-%m")

        # find match
        selected_label = None
        for label, ym in self.month_map.items():
            if ym == current_ym:
                selected_label = label
                break

        # fallback → latest
        if not selected_label and values:
            selected_label = values[0]

        # set default
        if selected_label:
            self.month_filter.set(selected_label)
        else:
            self.month_filter.set("")

    def _on_date_selected(self, _event=None):
        self.date_filter_enabled = True
        self.load_data()

    # ---------------- DATA ----------------
    def load_data(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        user_id = self.user["id"]
        search = self.search_entry.get().lower().strip()
        month_key = self.month_map.get(self.month_filter.get(), "")
        month_key_for_total = month_key if month_key else self._current_payroll_month_key()
        self.month_total_workdays = self._calculate_month_total_workdays(month_key_for_total)
        self.month_work_lbl.configure(text=self.month_total_workdays)
        sel_date = self.date_picker.get_date()

        sql = """
        SELECT
            d.work_date AS attendance_date,
            a.check_in,
            a.check_out,
            IFNULL(o.ot_hours, 0) AS ot_hours,
            CASE WHEN a.attendance_date IS NULL THEN 0 ELSE 1 END AS has_attendance
        FROM (
            SELECT attendance_date AS work_date
            FROM attendance
            WHERE user_id = %s
            UNION
            SELECT DATE(ot_date) AS work_date
            FROM overtime_requests
            WHERE member_id = %s
              AND status IN ('Accepted', 'Approved')
        ) d
        LEFT JOIN attendance a
               ON a.user_id = %s
              AND a.attendance_date = d.work_date
        LEFT JOIN (
            SELECT DATE(ot_date) AS ot_date, ROUND(SUM(COALESCE(hours, 0)), 2) AS ot_hours
            FROM overtime_requests
            WHERE member_id = %s
              AND status IN ('Accepted', 'Approved')
            GROUP BY DATE(ot_date)
        ) o ON d.work_date = o.ot_date
        WHERE d.work_date IS NOT NULL
        """
        params = [user_id, user_id, user_id, user_id]

        if month_key:
            sql += """
            AND (
                CASE WHEN DAY(d.work_date)>=26
                THEN DATE_FORMAT(DATE_ADD(d.work_date,INTERVAL 1 MONTH),'%Y-%m')
                ELSE DATE_FORMAT(d.work_date,'%Y-%m')
                END
            )=%s
            """
            params.append(month_key)

        sql += " ORDER BY d.work_date DESC"

        self.db.cursor.execute(sql, tuple(params))
        month_rows = self.db.cursor.fetchall()
        self.month_rows = month_rows

        leave_sql = """
            SELECT IFNULL(SUM(
                CASE
                    WHEN total_days IS NOT NULL THEN total_days
                    ELSE (DATEDIFF(end_date, start_date) + 1) *
                         (CASE WHEN shift_type = 'Full Day' THEN 1.0 ELSE 0.5 END)
                END
            ), 0) leave_days
            FROM leave_requests
            WHERE user_id=%s
              AND status='Approved'
        """
        leave_params = [user_id]
        if month_key:
            leave_sql += """
            AND (
                CASE WHEN DAY(start_date)>=26
                THEN DATE_FORMAT(DATE_ADD(start_date,INTERVAL 1 MONTH),'%Y-%m')
                ELSE DATE_FORMAT(start_date,'%Y-%m')
                END
            )=%s
            """
            leave_params.append(month_key)

        self.db.cursor.execute(leave_sql, tuple(leave_params))
        leave_row = self.db.cursor.fetchone() or {"leave_days": 0}
        leave_days = float(leave_row["leave_days"] or 0)

        late = 0
        ot_total = 0.0

        for r in month_rows:
            if r["check_in"] and str(r["check_in"]) > self.LATE_TIME:
                late += 1
            ot_total += float(r["ot_hours"] or 0)

        working_days = sum(int(r.get("has_attendance", 0) or 0) for r in month_rows)
        self.working_lbl.configure(text=str(working_days))
        self.leave_lbl.configure(text=f"{leave_days:g}")
        self.late_lbl.configure(text=str(late))
        self.ot_lbl.configure(text=f"{ot_total:g}")

        display = []

        for r in month_rows:
            if not r["attendance_date"] and float(r["ot_hours"] or 0) <= 0:
                continue

            if self.date_filter_enabled and sel_date and r["attendance_date"] != sel_date:
                continue

            if search and search not in str(r["attendance_date"]).lower():
                continue

            display.append(r)

        self.current_rows = display

        for r in display:
            row = ctk.CTkFrame(self.scroll, fg_color=("#EEF2F7", "#1F2933"), corner_radius=10)
            row.pack(fill="x", pady=4)

            ctk.CTkLabel(row, text=self._dash(r["attendance_date"]), width=140).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=self._dash(r["check_in"]), width=120).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=self._dash(r["check_out"]), width=120).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"{float(r['ot_hours'] or 0):g}", width=100, text_color=self.metric_colors["ot"]).pack(side="left", padx=10)

            remark = "LATE" if r["check_in"] and str(r["check_in"]) > self.LATE_TIME else "ON TIME"
            color = "#E67E22" if remark == "LATE" else "#27AE60"

            ctk.CTkLabel(row, text=remark, text_color=color, width=120).pack(side="left", padx=10)

    # ---------------- RESET ----------------
    def reset_filters(self):
        self.search_entry.delete(0, "end")

        # ===== CURRENT PAYROLL MONTH =====
        today = datetime.now()
        if today.day >= 26:
            if today.month == 12:
                current_ym = f"{today.year + 1}-01"
            else:
                current_ym = f"{today.year}-{today.month + 1:02d}"
        else:
            current_ym = today.strftime("%Y-%m")

        # find match
        selected_label = None
        all_labels = list(self.month_map.keys())

        for label, ym in self.month_map.items():
            if ym == current_ym:
                selected_label = label
                break

        # fallback
        if not selected_label and all_labels:
            selected_label = all_labels[0]

        if selected_label:
            self.month_filter.set(selected_label)

        self.date_filter_enabled = False
        self.date_picker.set_date(datetime.now().date())

        self.load_data()

    # ---------------- PDF ----------------
    def export_pdf(self):
        if not self.current_rows:
            messagebox.showwarning("No Data", "No records to export.")
            return

        selected_month = self.month_filter.get().replace(" ", "_")
        selected_member = str(self.user.get("full_name", "Member")).replace(" ", "_")
        file_name = f"Attendance_{selected_member}_{selected_month}.pdf"

        file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=file_name,
            filetypes=[("PDF files", "*.pdf")],
        )
        if not file:
            return

        doc = SimpleDocTemplate(
            file,
            pagesize=letter,
            leftMargin=28,
            rightMargin=28,
            topMargin=28,
            bottomMargin=28,
        )
        styles = getSampleStyleSheet()
        elements = []
        safe_member = escape(str(self.user.get("full_name", "Member")))
        safe_month = escape(self.month_filter.get())
        safe_month_work = escape(str(self.month_total_workdays))

        title_style = ParagraphStyle(
            "MemberTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#0B1220"),
            alignment=1,
            spaceAfter=6,
        )
        meta_style = ParagraphStyle(
            "MemberMeta",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#334155"),
        )

        elements.append(Paragraph("Employee Attendance Report", title_style))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", meta_style))
        elements.append(Spacer(1, 10))

        info_table = Table(
            [[
                Paragraph(f"<b><font color='#1D4ED8'>Member:</font></b> {safe_member}", meta_style),
                Paragraph(
                    f"<b><font color='#1D4ED8'>Month:</font></b> {safe_month}<br/>"
                    f"<b><font color='#1D4ED8'>Month Work:</font></b> {safe_month_work}",
                    meta_style
                ),
            ]],
            colWidths=[3.8 * inch, 3.2 * inch],
        )
        info_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#E2E8F0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 18))

        data = [["Date", "In", "Out", "OT", "Remark"]]
        for r in self.current_rows:
            remark = "LATE" if r["check_in"] and str(r["check_in"]) > self.LATE_TIME else "ON TIME"
            remark_color = "#EA580C" if remark == "LATE" else "#16A34A"
            data.append([
                self._dash(r["attendance_date"]),
                self._dash(r["check_in"]),
                self._dash(r["check_out"]),
                f"{float(r['ot_hours'] or 0):g}",
                Paragraph(f"<font color='{remark_color}'>{remark}</font>", meta_style)
            ])

        table = Table(
            data,
            repeatRows=1,
            colWidths=[1.5 * inch, 1.1 * inch, 1.1 * inch, 0.9 * inch, 1.5 * inch],
        )
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("TEXTCOLOR", (3, 1), (3, -1), colors.HexColor("#7C3AED")),
        ]))

        elements.append(table)
        doc.build(elements)
        messagebox.showinfo("Export Successful", "Attendance PDF exported successfully.")
