import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
from xml.sax.saxutils import escape

from database import Database


class AdminAttendance(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.db = Database()
        self.user = user
        self.team_map = {"All Teams": None}
        self.month_map = {}
        self.current_rows = []
        self.metric_colors = {
            "work": "#27AE60",
            "leave": "#3498DB",
            "late": "#E67E22",
            "ot": "#8B5CF6",
        }
        self.month_total_workdays = "-"

        self._build_ui()
        self._load_team_options()

        # IMPORTANT: load months first
        self.after(100, self._load_month_options)

        # load data AFTER UI is ready
        self.after(300, self.load_data)

    def _build_ui(self):
        header_f = ctk.CTkFrame(self, fg_color="transparent")
        header_f.pack(fill="x", padx=100, pady=(10, 10))

        ctk.CTkLabel(
            header_f,
            text="Employee Attendance Dashboard",
            font=("Arial", 24, "bold"),
            text_color=("#0F161F", "#EAF2FF"),
        ).pack(side="left")

        control_card = ctk.CTkFrame(
            self,
            fg_color=("#F6F8FC", "#1F2833"),
            corner_radius=16,
            border_width=1,
            border_color=("#D6DEEB", "#3A4656"),
        )
        control_card.pack(fill="x", padx=100, pady=(0, 5))

        ctk.CTkLabel(control_card, text="Search").grid(row=0, column=0, padx=(20, 6), pady=10, sticky="w")
        self.search_entry = ctk.CTkEntry(
            control_card,
            placeholder_text="Name or ID",
            width=220,
            corner_radius=10,
        )
        self.search_entry.grid(row=0, column=1, padx=6, pady=4)
        self.search_entry.bind("<KeyRelease>", lambda _e: self.load_data())

        ctk.CTkLabel(control_card, text="Team").grid(row=0, column=2, padx=(18, 6), pady=8, sticky="w")
        self.team_filter = ctk.CTkComboBox(
            control_card,
            values=["All Teams"],
            width=180,
            corner_radius=10,
            command=lambda _v: self.load_data(),
        )
        self.team_filter.grid(row=0, column=3, padx=6, pady=8)
        self.team_filter.set("All Teams")

        ctk.CTkLabel(control_card, text="Month").grid(row=0, column=4, padx=(18, 6), pady=8, sticky="w")

        self.month_filter = ctk.CTkComboBox(
        control_card,
        values=[],
        width=180,
        corner_radius=10,
        command=lambda v: self.load_data(),
        )

        self.month_filter.grid(row=0, column=5, padx=6, pady=8)

        ctk.CTkButton(
            control_card,
            text="Reset",
            width=78,
            corner_radius=10,
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=self.reset_filters,
        ).grid(row=0, column=7, padx=6, pady=8)

        ctk.CTkButton(
        control_card,
        text="Export PDF",
        width=98,
        corner_radius=10,
        fg_color="#DC2626",
        hover_color="#B91C1C",
        command=self.export_pdf,
    ).grid(row=0, column=8, padx=(100, 20), pady=8) # Changed 6 to 100 for more margin-left

        self.result_label = ctk.CTkLabel(self, text="0 records | Month Work: -", text_color=("#334155", "#CBD5E1"))
        self.result_label.pack(anchor="w", padx=100, pady=(0, 6))

        self._create_table()

    def _create_table(self):
    # main container
        self.table_card = ctk.CTkFrame(
            self,
            fg_color=("#FFFFFF", "#1B1F24"),
            corner_radius=16,
            border_width=1,
            border_color=("#D6DEEB", "#2A3442"),
        )
        self.table_card.pack(fill="both", expand=True, padx=100, pady=(0, 20))
        header = ctk.CTkFrame(
            self.table_card,
            fg_color=("#9CA3AF", "#334155"),
            corner_radius=8,
        )
        header.pack(fill="x", padx=10, pady=(10, 0))

        def h(text, w):
            return ctk.CTkLabel(
                header,
                text=text,
                width=w,
                text_color=("#000000", "#FFFFFF"),
                font=("Arial", 12, "bold")
            )

        h("Emp ID", 60).pack(side="left", padx=10)
        h("Name", 180).pack(side="left", padx=10)
        h("Team", 120).pack(side="left", padx=10)
        h("Work", 80).pack(side="left", padx=10)
        h("Leave", 80).pack(side="left", padx=10)
        h("Late", 80).pack(side="left", padx=10)
        h("OT", 100).pack(side="left", padx=10)
        # 🔥 SCROLL FRAME (like AdminUsers)
        self.scroll = ctk.CTkScrollableFrame(
            self.table_card,
            fg_color="transparent"
        )
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

    def _load_team_options(self):
        try:
            self.db.cursor.execute("SELECT team_id, team_name FROM teams ORDER BY team_name")
            rows = self.db.cursor.fetchall()
            self.team_map = {"All Teams": None}
            for row in rows:
                label = f"{row['team_name']}"
                self.team_map[label] = row["team_id"]
            self.team_filter.configure(values=list(self.team_map.keys()))
            self.team_filter.set("All Teams")
        except Exception as e:
            print(f"Team filter error: {e}")

    def _load_month_options(self):
        try:
            payroll_calc = """
                CASE 
                    WHEN DAY({col}) >= 26 
                    THEN DATE_FORMAT(DATE_ADD({col}, INTERVAL 1 MONTH), '%Y-%m')
                    ELSE DATE_FORMAT({col}, '%Y-%m')
                END
            """
            
            sql = f"""
                SELECT DISTINCT ym FROM (
                    SELECT {payroll_calc.format(col='attendance_date')} AS ym FROM attendance
                    UNION
                    SELECT {payroll_calc.format(col='start_date')} AS ym FROM leave_requests
                    UNION
                    SELECT {payroll_calc.format(col='ot_date')} AS ym FROM overtime_requests
                ) x
                WHERE ym IS NOT NULL
                ORDER BY ym DESC
            """

            self.db.cursor.execute(sql)
            rows = self.db.cursor.fetchall()

            self.month_map = {}
            values = []

            for r in rows:
                ym = r["ym"]
                dt = datetime.strptime(ym, "%Y-%m")
                label = dt.strftime("%B %Y")
                self.month_map[label] = ym
                values.append(label)

            # Apply values to dropdown
            self.month_filter.configure(values=values)
            self.update_idletasks()

            # ================= DEFAULT = CURRENT PAYROLL MONTH =================
            today = datetime.now()
            if today.day >= 26:
                if today.month == 12:
                    current_payroll_ym = f"{today.year + 1}-01"
                else:
                    current_payroll_ym = f"{today.year}-{today.month + 1:02d}"
            else:
                current_payroll_ym = today.strftime("%Y-%m")

            # Find matching label
            selected_label = None
            for label, ym_val in self.month_map.items():
                if ym_val == current_payroll_ym:
                    selected_label = label
                    break

            # Fallback to latest available month
            if not selected_label and values:
                selected_label = values[0]

            # Set default
            if selected_label:
                self.month_filter.set(selected_label)
            else:
                self.month_filter.set("")

        except Exception as e:
            print("Month filter error:", e)
            values = list(self.month_map.keys())
            if values:
                self.month_filter.set(values[0])
            else:
                self.month_filter.set("")

    @staticmethod
    def _pretty_month_label(ym):
        return datetime.strptime(ym, "%Y-%m").strftime("%b %Y")

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

    @staticmethod
    def _num_or_dash(value):
        return "-" if value in (None, "") else f"{float(value):g}"

    def _get_employee_attendance_rows(self, user_id, month_key=""):
        sql = """
        SELECT
            d.work_date AS attendance_date,
            a.check_in,
            a.check_out,
            IFNULL(o.ot_hours, 0) AS ot_hours,
            CASE WHEN a.check_in IS NOT NULL AND a.check_in > '07:45:00' THEN 1 ELSE 0 END AS is_late
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
                CASE
                    WHEN DAY(d.work_date) >= 26
                    THEN DATE_FORMAT(DATE_ADD(d.work_date, INTERVAL 1 MONTH), '%Y-%m')
                    ELSE DATE_FORMAT(d.work_date, '%Y-%m')
                END
            ) = %s
            """
            params.append(month_key)

        sql += " ORDER BY d.work_date DESC"
        self.db.cursor.execute(sql, tuple(params))
        return self.db.cursor.fetchall()

    def _open_employee_attendance_detail(self, user_id, full_name):
        month_label = self.month_filter.get()
        month_key = self.month_map.get(month_label, "")

        try:
            rows = self._get_employee_attendance_rows(user_id, month_key)
        except Exception as e:
            messagebox.showerror("Fetch Error", f"Cannot load attendance detail: {e}")
            return

        detail_win = ctk.CTkToplevel(self)
        detail_win.title(f"Attendance Detail - {full_name}")
        detail_win.geometry("860x560")
        detail_win.transient(self.winfo_toplevel())
        detail_win.grab_set()

        ctk.CTkLabel(
            detail_win,
            text=f"{full_name} (ID: {user_id})",
            font=("Arial", 18, "bold"),
        ).pack(anchor="w", padx=20, pady=(18, 4))

        ctk.CTkLabel(
            detail_win,
            text=f"Month: {month_label}",
            text_color=("#334155", "#CBD5E1"),
        ).pack(anchor="w", padx=20, pady=(0, 10))

        table_card = ctk.CTkFrame(
            detail_win,
            fg_color=("#FFFFFF", "#1B1F24"),
            corner_radius=12,
            border_width=1,
            border_color=("#D6DEEB", "#2A3442"),
        )
        table_card.pack(fill="both", expand=True, padx=20, pady=(0, 14))

        header = ctk.CTkFrame(table_card, fg_color=("#9CA3AF", "#334155"), corner_radius=8)
        header.pack(fill="x", padx=10, pady=(10, 0))

        def h(text, w):
            return ctk.CTkLabel(
                header,
                text=text,
                width=w,
                text_color=("#000000", "#FFFFFF"),
                font=("Arial", 12, "bold"),
            )

        h("Date", 170).pack(side="left", padx=10)
        h("Check-In", 140).pack(side="left", padx=10)
        h("Check-Out", 140).pack(side="left", padx=10)
        h("OT Hours", 120).pack(side="left", padx=10)
        h("Remark", 120).pack(side="left", padx=10)

        scroll = ctk.CTkScrollableFrame(table_card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        if not rows:
            ctk.CTkLabel(
                scroll,
                text="No attendance records found for the selected month.",
                text_color=("#64748B", "#94A3B8"),
            ).pack(pady=20)
            return

        for row in rows:
            card = ctk.CTkFrame(scroll, fg_color=("#EEF2F7", "#1F2933"), corner_radius=10)
            card.pack(fill="x", pady=4, padx=4)

            date_value = self._dash(row["attendance_date"])
            check_in_value = self._dash(row["check_in"])
            check_out_value = self._dash(row["check_out"])
            ot_value = f"{float(row['ot_hours'] or 0):g}"
            remark = "LATE" if row["is_late"] else "ON TIME"
            remark_color = self.metric_colors["late"] if row["is_late"] else self.metric_colors["work"]

            ctk.CTkLabel(card, text=date_value, width=170).pack(side="left", padx=10)
            ctk.CTkLabel(card, text=check_in_value, width=140).pack(side="left", padx=10)
            ctk.CTkLabel(card, text=check_out_value, width=140).pack(side="left", padx=10)
            ctk.CTkLabel(card, text=ot_value, width=120, text_color=self.metric_colors["ot"]).pack(side="left", padx=10)
            ctk.CTkLabel(card, text=remark, width=120, text_color=remark_color).pack(side="left", padx=10)

    def reset_filters(self):
        # 1. Clear search box
        self.search_entry.delete(0, "end")
        
        # 2. Reset team filter
        self.team_filter.set("All Teams")
        
        # 3. Calculate Current Payroll Month (26th to 25th logic)
        today = datetime.now()
        if today.day >= 26:
            # If today is 26th or later, we are in next month's payroll
            if today.month == 12:
                current_payroll_ym = f"{today.year + 1}-01"
            else:
                current_payroll_ym = f"{today.year}-{today.month + 1:02d}"
        else:
            # If today is 1st to 25th, we are in this month's payroll
            current_payroll_ym = today.strftime("%Y-%m")
            
        # 4. Find the matching label in our map (e.g., "April 2026")
        all_labels = list(self.month_map.keys())
        default_label = all_labels[0] if all_labels else ""
        for label, ym_val in self.month_map.items():
            if ym_val == current_payroll_ym:
                default_label = label
                break
        
        # Fallback: if current payroll month has no data yet, pick the latest available
        if default_label not in all_labels and len(all_labels) > 0:
            default_label = all_labels[0]

        self.month_filter.set(default_label)
        
        # 5. Refresh the table
        self.load_data()

    def load_data(self):
    # clear old rows (scroll frame)
        for w in self.scroll.winfo_children():
         w.destroy()

        search_query = self.search_entry.get().strip()
        selected_team = self.team_filter.get()
        selected_month = self.month_filter.get()

        team_id = self.team_map.get(selected_team)
        month_key = self.month_map.get(selected_month, "")
        
        # Calculate workdays for selected month
        if month_key:
            self.month_total_workdays = self._calculate_month_total_workdays(month_key)
        else:
            self.month_total_workdays = "-"

        # Always apply month filter (since there is no 'All Months' option)
        att_where = f"""
            WHERE (
                CASE 
                    WHEN DAY(attendance_date) >= 26 
                    THEN DATE_FORMAT(DATE_ADD(attendance_date, INTERVAL 1 MONTH), '%Y-%m')
                    ELSE DATE_FORMAT(attendance_date, '%Y-%m')
                END
            ) = %s
        """
        att_params = [month_key]

        leave_where = "WHERE status = 'Approved'"
        leave_where += f"""
            AND (
                CASE 
                    WHEN DAY(start_date) >= 26 
                    THEN DATE_FORMAT(DATE_ADD(start_date, INTERVAL 1 MONTH), '%Y-%m')
                    ELSE DATE_FORMAT(start_date, '%Y-%m')
                END
            ) = %s
        """
        leave_params = [month_key]

        ot_where = "WHERE status IN ('Accepted', 'Approved')"
        ot_where += f"""
            AND (
                CASE 
                    WHEN DAY(ot_date) >= 26 
                    THEN DATE_FORMAT(DATE_ADD(ot_date, INTERVAL 1 MONTH), '%Y-%m')
                    ELSE DATE_FORMAT(ot_date, '%Y-%m')
                END
            ) = %s
        """
        ot_params = [month_key]

    # ================= SEARCH FILTER =================
        outer_where = "WHERE (a.latest_date IS NOT NULL OR o.overtimehour IS NOT NULL) AND (u.full_name LIKE %s OR CAST(u.id AS CHAR) LIKE %s)"
        outer_params = [f"%{search_query}%", f"%{search_query}%"]

        if team_id is not None:
            outer_where += " AND u.team_id = %s"
            outer_params.append(team_id)

        sql = f"""
            SELECT
                u.id,
                u.full_name,
                IFNULL(t.team_name, '-') AS team_name,
                IFNULL(a.latest_date, '-') AS latest_date,
                IFNULL(a.workdays, 0) AS workdays,
                IFNULL(lr.leaveday, 0) AS leaveday,
                IFNULL(a.latecount, 0) AS latecount,
                IFNULL(o.overtimehour, 0) AS overtimehour
            FROM users u
            LEFT JOIN teams t ON u.team_id = t.team_id

            LEFT JOIN (
                SELECT
                    user_id,
                    MAX(attendance_date) AS latest_date,
                    COUNT(DISTINCT attendance_date) AS workdays,
                    SUM(CASE WHEN check_in > '07:45:00' THEN 1 ELSE 0 END) AS latecount
                FROM attendance
                {att_where}
                GROUP BY user_id
            ) a ON u.id = a.user_id

            LEFT JOIN (
                SELECT
                    user_id,
                    SUM(
                        CASE
                            WHEN total_days IS NOT NULL THEN total_days
                            ELSE (DATEDIFF(end_date, start_date) + 1) *
                                 (CASE WHEN shift_type = 'Full Day' THEN 1.0 ELSE 0.5 END)
                        END
                    ) AS leaveday
                FROM leave_requests
                {leave_where}
                GROUP BY user_id
            ) lr ON u.id = lr.user_id

            LEFT JOIN (
                SELECT
                    member_id,
                    ROUND(SUM(COALESCE(hours, 0)), 2) AS overtimehour
                FROM overtime_requests
                {ot_where}
                GROUP BY member_id
            ) o ON u.id = o.member_id

            {outer_where}
            ORDER BY u.id
        """

        params = att_params + leave_params + ot_params + outer_params

        try:
                self.db.cursor.execute(sql, tuple(params))
                self.current_rows = self.db.cursor.fetchall()

            # ================= CREATE CARDS =================
                for row in self.current_rows:
                    card = ctk.CTkFrame(
                        self.scroll,
                        fg_color=("#EEF2F7", "#1F2933"),
                        corner_radius=10
                    )
                    card.pack(fill="x", pady=4, padx=5)

                    # row content
                    ctk.CTkLabel(card, text=self._dash(row["id"]), width=60).pack(side="left", padx=10)
                    ctk.CTkButton(
                        card,
                        text=self._dash(row["full_name"]),
                        width=180,
                        anchor="w",
                        fg_color="transparent",
                        hover_color=("#DBEAFE", "#1E3A5F"),
                        text_color=("#1D4ED8", "#60A5FA"),
                        font=("Arial", 12, "underline"),
                        cursor="hand2",
                        command=lambda user_id=row["id"], full_name=row["full_name"]: self._open_employee_attendance_detail(user_id, full_name),
                    ).pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._dash(row["team_name"]), width=120).pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._dash(row["workdays"]), width=80, text_color=self.metric_colors["work"]).pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._num_or_dash(row["leaveday"]), width=80, text_color=self.metric_colors["leave"]).pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._dash(row["latecount"]), width=80, text_color=self.metric_colors["late"]).pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._num_or_dash(row["overtimehour"]), width=100, text_color=self.metric_colors["ot"]).pack(side="left", padx=10)

                    # 🔥 bottom border line (like AdminUsers style)
                    border = ctk.CTkFrame(card, height=1, fg_color=("#D6DEEB", "#334155"))
                    border.pack(fill="x", side="bottom", pady=(6, 0))

                self.result_label.configure(text=f"{len(self.current_rows)} records | Month Work: {self.month_total_workdays}")

        except Exception as e:
                print("Fetch Error:", e)
                self.result_label.configure(text=f"0 records | Month Work: {self.month_total_workdays}")

    def export_pdf(self):
        if not self.current_rows:
            messagebox.showwarning("No Data", "No records to export.")
            return

        selected_month = self.month_filter.get().replace(" ", "_")
        selected_team = self.team_filter.get().split(" (#")[0].replace(" ", "_")
        file_name = f"Attendance_{selected_team}_{selected_month}.pdf"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=file_name,
            filetypes=[("PDF files", "*.pdf")],
        )
        if not file_path:
            return

        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        except Exception as e:
            messagebox.showerror("Missing Dependency", f"Cannot export PDF: {e}")
            return

        try:
            doc = SimpleDocTemplate(
                file_path,
                pagesize=letter,
                leftMargin=28,
                rightMargin=28,
                topMargin=28,
                bottomMargin=28,
            )
            styles = getSampleStyleSheet()
            elements = []
            safe_team_label = escape(self.team_filter.get())
            safe_month_label = escape(self.month_filter.get())
            safe_month_work = escape(str(self.month_total_workdays))

            title_style = ParagraphStyle(
                "AdminTitle",
                parent=styles["Title"],
                fontName="Helvetica-Bold",
                fontSize=22,
                leading=26,
                textColor=colors.HexColor("#0B1220"),
                alignment=1,
                spaceAfter=6,
            )
            meta_style = ParagraphStyle(
                "AdminMeta",
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
                    Paragraph(f"<b><font color='#1D4ED8'>Team:</font></b> {safe_team_label}", meta_style),
                    Paragraph(
                        f"<b><font color='#1D4ED8'>Month:</font></b> {safe_month_label}<br/>"
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

            table_data = [[
                "Emp ID",
                "Employee",
                "Team",
                "Work Days",
                "Leave Days",
                "Late Count",
                "OT Hours",
            ]]
            for row in self.current_rows:
                table_data.append([
                    self._dash(row["id"]),
                    self._dash(row["full_name"]),
                    self._dash(row["team_name"]),
                    self._dash(row["workdays"]),
                    self._num_or_dash(row["leaveday"]),
                    self._dash(row["latecount"]),
                    self._num_or_dash(row["overtimehour"]),
                ])

            table = Table(
                table_data,
                repeatRows=1,
                colWidths=[0.8 * inch, 2.0 * inch, 1.4 * inch, 1.0 * inch, 1.0 * inch, 0.95 * inch, 0.95 * inch],
            )
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("ALIGN", (1, 1), (2, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("TEXTCOLOR", (3, 1), (3, -1), colors.HexColor("#16A34A")),
                ("TEXTCOLOR", (4, 1), (4, -1), colors.HexColor("#0284C7")),
                ("TEXTCOLOR", (5, 1), (5, -1), colors.HexColor("#EA580C")),
                ("TEXTCOLOR", (6, 1), (6, -1), colors.HexColor("#7C3AED")),
            ]))
            elements.append(table)

            doc.build(elements)
            messagebox.showinfo("Export Successful", "Attendance PDF exported successfully.")
        except Exception as e:
            messagebox.showerror("Export Error", f"PDF export failed: {e}")
