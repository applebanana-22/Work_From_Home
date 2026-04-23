import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta

from database import Database


class AdminAttendance(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.db = Database()
        self.user = user
        self.team_map = {"All Teams": None}
        self.month_map = {"All Months": ""}
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
        self.after(200, self.load_data)

    def _build_ui(self):
        header_f = ctk.CTkFrame(self, fg_color="transparent")
        header_f.pack(fill="x", padx=100, pady=(10, 10))

        ctk.CTkLabel(
            header_f,
            text="Employee Attendance Dashboard",
            font=("Arial", 24, "bold"),
            text_color=("#1E3A5F", "#EAF2FF"),
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
        values=["All Months"],   # ✅ declare here
        width=180,
        corner_radius=10,
        command=lambda v: self.load_data(),
        )

        self.month_filter.grid(row=0, column=5, padx=6, pady=8)

        self.month_filter.set("All Months")   # ✅ also here (after creation)

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

        self.result_label = ctk.CTkLabel(self, text="0 records", text_color=("#334155", "#CBD5E1"))
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
            fg_color=("#0F172A", "#334155"),
            corner_radius=8,
        )
        header.pack(fill="x", padx=10, pady=(10, 0))

        def h(text, w):
            return ctk.CTkLabel(
                header,
                text=text,
                width=w,
                text_color="white",
                font=("Arial", 12, "bold")
            )

        h("Emp ID", 60).pack(side="left", padx=10)
        h("Name", 180).pack(side="left", padx=10)
        h("Team", 120).pack(side="left", padx=10)
        h("Month Work", 95).pack(side="left", padx=10)
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
            # 1. Define the SQL logic to get unique payroll months based on 26th-25th cycle
            # We use the same CASE logic used in your load_data method
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
                    SELECT {payroll_calc.format(col='ot_date')} AS ym FROM overtime
                ) x
                WHERE ym IS NOT NULL
                ORDER BY ym DESC
            """

            self.db.cursor.execute(sql)
            rows = self.db.cursor.fetchall()

            self.month_map = {"All Months": ""}
            values = ["All Months"]

            for r in rows:
                ym = r["ym"]
                dt = datetime.strptime(ym, "%Y-%m")
                label = dt.strftime("%B %Y")
                self.month_map[label] = ym
                values.append(label)

            self.month_filter.configure(values=values)
            self.update_idletasks()

            # ================= DEFAULT = CURRENT PAYROLL MONTH =================
            # Logic: If today is >= 26, the 'Current Payroll' is NEXT month.
            today = datetime.now()
            if today.day >= 26:
                # Move to next month
                if today.month == 12:
                    current_payroll_ym = f"{today.year + 1}-01"
                else:
                    current_payroll_ym = f"{today.year}-{today.month + 1:02d}"
            else:
                current_payroll_ym = today.strftime("%Y-%m")

            default_label = "All Months"
            for label, ym_val in self.month_map.items():
                if ym_val == current_payroll_ym:
                    default_label = label
                    break

            # If the calculated current payroll month isn't in DB yet, 
            # fall back to the most recent month available in the list
            if default_label == "All Months" and len(values) > 1:
                default_label = values[1]

            self.after(50, lambda: self.month_filter.set(default_label))

        except Exception as e:
            print("Month filter error:", e)
            self.month_filter.set("All Months")

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
        default_label = "All Months"
        for label, ym_val in self.month_map.items():
            if ym_val == current_payroll_ym:
                default_label = label
                break
        
        # Fallback: if current payroll month has no data yet, pick the latest available
        if default_label == "All Months" and len(self.month_map) > 1:
            # Get the first item after "All Months" from values list
            all_labels = list(self.month_map.keys())
            if len(all_labels) > 1:
                default_label = all_labels[1]

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
        month_key_for_total = month_key if month_key else self._current_payroll_month_key()
        self.month_total_workdays = self._calculate_month_total_workdays(month_key_for_total)

        att_where = ""
        leave_where = "WHERE status = 'Approved'"
        ot_where = "WHERE status IN ('Accepted', 'Approved')"

        att_params = []
        leave_params = []
        ot_params = []

    # ================= PAYROLL FILTER =================
        if month_key:
            att_where = f"""
                WHERE (
                    CASE 
                        WHEN DAY(attendance_date) >= 26 
                        THEN DATE_FORMAT(DATE_ADD(attendance_date, INTERVAL 1 MONTH), '%Y-%m')
                        ELSE DATE_FORMAT(attendance_date, '%Y-%m')
                    END
                ) = %s
            """
            att_params.append(month_key)

        if month_key:
            leave_where += f"""
                AND (
                    CASE 
                        WHEN DAY(start_date) >= 26 
                        THEN DATE_FORMAT(DATE_ADD(start_date, INTERVAL 1 MONTH), '%Y-%m')
                        ELSE DATE_FORMAT(start_date, '%Y-%m')
                    END
                ) = %s
            """
            leave_params.append(month_key)

            ot_where += f"""
                AND (
                    CASE 
                        WHEN DAY(ot_date) >= 26 
                        THEN DATE_FORMAT(DATE_ADD(ot_date, INTERVAL 1 MONTH), '%Y-%m')
                        ELSE DATE_FORMAT(ot_date, '%Y-%m')
                    END
                ) = %s
            """
            ot_params.append(month_key)

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
                            WHEN is_half_day = 1 THEN (DATEDIFF(end_date, start_date) + 1) + 0.5
                            ELSE DATEDIFF(end_date, start_date) + 1
                        END
                    ) AS leaveday
                FROM leave_requests
                {leave_where}
                GROUP BY user_id
            ) lr ON u.id = lr.user_id

            LEFT JOIN (
                SELECT
                    member_name,
                    SUM(hours) AS overtimehour
                FROM overtime
                {ot_where}
                GROUP BY member_name
            ) o ON TRIM(u.full_name) = TRIM(o.member_name)

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
                        fg_color=("white", "#1F2933"),
                        corner_radius=10
                    )
                    card.pack(fill="x", pady=4, padx=5)

                    # row content
                    ctk.CTkLabel(card, text=self._dash(row["id"]), width=60).pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._dash(row["full_name"]), width=180, anchor="w").pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._dash(row["team_name"]), width=120).pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._dash(self.month_total_workdays), width=95, text_color=self.metric_colors["work"]).pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._dash(row["workdays"]), width=80, text_color=self.metric_colors["work"]).pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._num_or_dash(row["leaveday"]), width=80, text_color=self.metric_colors["leave"]).pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._dash(row["latecount"]), width=80, text_color=self.metric_colors["late"]).pack(side="left", padx=10)
                    ctk.CTkLabel(card, text=self._num_or_dash(row["overtimehour"]), width=100, text_color=self.metric_colors["ot"]).pack(side="left", padx=10)

                    # 🔥 bottom border line (like AdminUsers style)
                    border = ctk.CTkFrame(card, height=1, fg_color=("#D6DEEB", "#334155"))
                    border.pack(fill="x", side="bottom", pady=(6, 0))

                self.result_label.configure(text=f"{len(self.current_rows)} records")

        except Exception as e:
                print("Fetch Error:", e)
                self.result_label.configure(text="0 records")

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
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        except Exception as e:
            messagebox.showerror("Missing Dependency", f"Cannot export PDF: {e}")
            return

        try:
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            elements.append(Paragraph("Employee Attendance Report", styles["Title"]))
            elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
            elements.append(Paragraph(f"Team Filter: {self.team_filter.get()}", styles["Normal"]))
            elements.append(Paragraph(f"Month Filter: {self.month_filter.get()}", styles["Normal"]))
            elements.append(Spacer(1, 12))

            table_data = [[
                "Emp ID",
                "Employee",
                "Team",
                "Latest Date",
                "Month Work (26-25)",
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
                    self._dash(row["latest_date"]),
                    self._dash(self.month_total_workdays),
                    self._dash(row["workdays"]),
                    self._num_or_dash(row["leaveday"]),
                    self._dash(row["latecount"]),
                    self._num_or_dash(row["overtimehour"]),
                ])

            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#EEF2F7")]),
            ]))
            elements.append(table)

            doc.build(elements)
            messagebox.showinfo("Export Successful", "Attendance PDF exported successfully.")
        except Exception as e:
            messagebox.showerror("Export Error", f"PDF export failed: {e}")
