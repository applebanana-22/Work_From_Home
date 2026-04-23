import customtkinter as ctk
from database import Database
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


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
        header.pack(fill="x", padx=30, pady=20)

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
        filter_frame.pack(fill="x", padx=30, pady=(0, 18))

        ctk.CTkLabel(filter_frame, text="Search").grid(row=0, column=0, padx=(20, 6), pady=10, sticky="w")

        self.search_entry = ctk.CTkEntry(
            filter_frame,
            width=220,
            corner_radius=10,
        )
        self.search_entry.grid(row=0, column=1, padx=6, pady=8)
        self.search_entry.bind("<KeyRelease>", lambda _e: self.load_data())

        ctk.CTkLabel(filter_frame, text="Date").grid(row=0, column=2, padx=(18, 6), pady=8, sticky="w")

        self.date_picker = DateEntry(filter_frame, date_pattern="yyyy-mm-dd")
        self.date_picker.configure(width=18)
        self.date_picker.grid(row=0, column=3, padx=6, pady=8)
        self.date_picker.bind("<<DateEntrySelected>>", self._on_date_selected)

        ctk.CTkLabel(filter_frame, text="Month").grid(row=0, column=4, padx=(18, 6), pady=8, sticky="w")

        self.month_filter = ctk.CTkComboBox(
            filter_frame,
            values=["All Months"],
            width=180,
            corner_radius=10,
            command=lambda _v: self.load_data()
        )
        self.month_filter.grid(row=0, column=5, padx=6, pady=8)
        self.month_filter.set("All Months")

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
        ).grid(row=0, column=7, padx=(305, 20), pady=8)

        # ---------------- STATS ----------------
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=60, pady=5)

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
        self.table_card.pack(fill="both", expand=True, padx=30, pady=10)

        header_row = ctk.CTkFrame(self.table_card, fg_color=("#0F172A", "#334155"))
        header_row.pack(fill="x", padx=10, pady=(10, 0))

        def h(text, w):
            return ctk.CTkLabel(header_row, text=text, width=w,
                                text_color="white", font=("Arial", 12, "bold"))

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
        sql = """
            SELECT DISTINCT DATE_FORMAT(attendance_date,'%Y-%m') ym
            FROM attendance
            WHERE user_id=%s
            ORDER BY ym DESC
        """
        self.db.cursor.execute(sql, (self.user["id"],))
        rows = self.db.cursor.fetchall()

        values = ["All Months"]
        self.month_map = {"All Months": ""}

        for r in rows:
            ym = r["ym"]
            dt = datetime.strptime(ym, "%Y-%m")
            label = dt.strftime("%B %Y")
            self.month_map[label] = ym
            values.append(label)

        self.month_filter.configure(values=values)

        today = datetime.now()
        if today.day >= 26:
            current_ym = f"{today.year + (today.month == 12)}-{(today.month % 12 + 1):02d}"
        else:
            current_ym = today.strftime("%Y-%m")

        default = "All Months"
        for label, ym in self.month_map.items():
            if ym == current_ym:
                default = label
                break

        self.after(50, lambda: self.month_filter.set(default))

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
            FROM overtime
            WHERE TRIM(member_name) = TRIM(%s)
              AND status IN ('Accepted', 'Approved')
        ) d
        LEFT JOIN attendance a
               ON a.user_id = %s
              AND a.attendance_date = d.work_date
        LEFT JOIN (
            SELECT DATE(ot_date) AS ot_date, SUM(hours) AS ot_hours
            FROM overtime
            WHERE TRIM(member_name) = TRIM(%s)
              AND status IN ('Accepted', 'Approved')
            GROUP BY DATE(ot_date)
        ) o ON d.work_date = o.ot_date
        WHERE d.work_date IS NOT NULL
        """
        params = [user_id, self.user["full_name"], user_id, self.user["full_name"]]

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
                    WHEN is_half_day = 1 THEN (DATEDIFF(end_date, start_date) + 1) + 0.5
                    ELSE DATEDIFF(end_date, start_date) + 1
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
            row = ctk.CTkFrame(self.scroll, fg_color=("white", "#1F2933"), corner_radius=10)
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
        self.month_filter.set("All Months")
        self.date_filter_enabled = False
        self.date_picker.set_date(datetime.now())
        self.load_data()

    # ---------------- PDF ----------------
    def export_pdf(self):
        if not self.current_rows:
            messagebox.showwarning("No Data", "No records to export.")
            return

        file = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not file:
            return

        doc = SimpleDocTemplate(file)

        data = [["Date", "In", "Out", "OT", "Remark"]]
        for r in self.current_rows:
            remark = "LATE" if r["check_in"] and str(r["check_in"]) > self.LATE_TIME else "ON TIME"
            data.append([
                self._dash(r["attendance_date"]),
                self._dash(r["check_in"]),
                self._dash(r["check_out"]),
                f"{float(r['ot_hours'] or 0):g}",
                remark
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ]))

        doc.build([table])
        messagebox.showinfo("Success", "PDF exported")
