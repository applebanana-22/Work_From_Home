import customtkinter as ctk
import calendar
from datetime import datetime
from database import Database
from tkinter import messagebox, ttk
from tkcalendar import Calendar

class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None):
        super().__init__(master, fg_color="transparent")
        self._date = initial_date or datetime.today().date()
        self._open = False
        
        # Fixed Dark Style for Calendar
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
            hover_color="#2A2A2A",
            border_width=1,
            fg_color="#1E1E1E",
            border_color="#2C2C2C",
            text_color="white",
            anchor="w",
            command=self.toggle
        )
        self.btn.pack()
        
        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color="#141E2B",
            corner_radius=12,
            border_width=1,
            border_color="#2A3A4A"
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

class MemberReportFrame(ctk.CTkFrame):
    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.db = Database()
        self.configure(fg_color="transparent")
       
        # State Management
        self.now = datetime.now()
        self.report_rows = [] 

        # Filter State
        today = datetime.today().date()
        self.start_date = datetime(today.year, today.month, 1).date()
        self.end_date = today

        self.show_history_view()

    def clear_view(self):
        for widget in self.winfo_children():
            widget.destroy()

    def get_db_categories(self):
        try:
            self.db.cursor.execute("SELECT name FROM report_categories ORDER BY name ASC")
            results = self.db.cursor.fetchall()
            return [row['name'] for row in results] if results else ["General"]
        except:
            return ["General"]

    def refresh_view(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        if start > end:
            messagebox.showerror("Invalid Date", "Start date cannot be later than End date.")
            self.count_lbl.configure(text="(0 records)")
            return

        try:
            query = """
                SELECT report_date, category, tasks, hours
                FROM daily_reports
                WHERE user_id = %s AND report_date BETWEEN %s AND %s
                ORDER BY report_date DESC, created_at ASC
            """
            self.db.cursor.execute(query, (self.user['id'], start, end))
            reports = self.db.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        from collections import defaultdict
        grouped = defaultdict(list)
        for r in reports:
            grouped[str(r['report_date'])].append(r)

        self.count_lbl.configure(text=f"({len(grouped)} records)")

        for date, rows in sorted(grouped.items(), reverse=True):
            total_hours = sum(float(r['hours']) for r in rows)

            card = ctk.CTkFrame(
                self.scroll,
                corner_radius=12,
                fg_color="#1E1E1E",
                border_width=1,
                border_color="#2C2C2C"
            )
            card.pack(fill="x", pady=6, padx=10)

            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=14, pady=10)

            ctk.CTkLabel(info, text=date, font=("Arial", 13, "bold"), text_color="#E8EDF2").pack(anchor="w")
            ctk.CTkLabel(info, text=f"Total: {total_hours}h", font=("Arial", 11), text_color="#AAB7C4").pack(anchor="w")
            
            summary = f"{len(rows)} tasks" if len(rows) > 1 else rows[0]['tasks']
            ctk.CTkLabel(info, text=summary, font=("Arial", 11), text_color="#718096").pack(anchor="w")

            btn_frame = ctk.CTkFrame(card, fg_color="transparent")
            btn_frame.pack(side="right", padx=12, pady=10)

            def _btn(text, color, hover, cmd):
                return ctk.CTkButton(
                    btn_frame, text=text, width=60, height=30, corner_radius=8,
                    fg_color=color, hover_color=hover, command=cmd
                )

            _btn("View", "#1f538d", "#174a7a", lambda d=date: self.show_detail_view(d)).pack(side="left", padx=4)
            _btn("Edit", "#F39C12", "#D68910", lambda d=date: self.edit_report(d)).pack(side="left", padx=4)
            _btn("Delete", "#E74C3C", "#C0392B", lambda d=date: self.delete_report(d)).pack(side="left", padx=4)

    def show_history_view(self):
        self.clear_view()
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=80, pady=(10, 20))

        ctk.CTkLabel(top, text="Daily Reports", font=("Arial", 20, "bold"), text_color="white").pack(side="left")
        ctk.CTkButton(top, text="+ New Report", fg_color="#10B981", command=self.show_form_view).pack(side="right")

        filter_card = ctk.CTkFrame(self, corner_radius=14, fg_color="#1E1E1E", border_width=1, border_color="#2C2C2C")
        filter_card.pack(fill="x", padx=80, pady=(4, 10))

        inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)

        ctk.CTkLabel(inner, text="From", text_color="white", font=("Arial", 11, "bold")).pack(side="left", padx=(0, 4))
        self.start_cal = DatePickerButton(inner, initial_date=self.start_date)
        self.start_cal.pack(side="left", padx=(0, 16))

        ctk.CTkLabel(inner, text="To", text_color="white", font=("Arial", 11, "bold")).pack(side="left", padx=(0, 4))
        self.end_cal = DatePickerButton(inner, initial_date=self.end_date)
        self.end_cal.pack(side="left", padx=(0, 24))

        ctk.CTkFrame(inner, width=1, height=32, fg_color="#2A3A4A").pack(side="left", padx=(0, 20))

        def _btn(parent, text, color, hover, cmd):
            ctk.CTkButton(parent, text=text, width=80, height=36, corner_radius=9, font=("Arial", 12, "bold"),
                         fg_color=color, hover_color=hover, command=cmd).pack(side="left", padx=4)

        _btn(inner, "🔍 Filter", "#2471A3", "#1A5276", self.refresh_view)
        _btn(inner, "✖ Clear", "#566573", "#424949", self.clear_filters)
        _btn(inner, "📄 Export", "#C0392B", "#922B21", self.export_pdf_reports)

        list_header = ctk.CTkFrame(self, fg_color="transparent")
        list_header.pack(fill="x", padx=80, pady=(4, 2))
        ctk.CTkLabel(list_header, text="Report List", font=("Arial", 14, "bold"), text_color="white").pack(side="left", padx=4)
        self.count_lbl = ctk.CTkLabel(list_header, text="", font=("Arial", 12), text_color="#566573")
        self.count_lbl.pack(side="left", padx=8)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#1A1A1A", corner_radius=14, border_width=1, border_color="#2C2C2C")
        self.scroll.pack(fill="both", expand=True, padx=80, pady=(0, 10))
        self.refresh_view()

    def show_form_view(self):
        self.clear_view()
        self.report_rows = []
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=80, pady=20)

        top_bar = ctk.CTkFrame(header, fg_color="transparent")
        top_bar.pack(fill="x")
        ctk.CTkButton(top_bar, text="← Back", width=80, fg_color="#333333", command=self.show_history_view).pack(side="left")
        self.stats_lbl = ctk.CTkLabel(top_bar, text="Total: 0.0 / 8.0 Hours", font=("Arial", 16, "bold"), text_color="#F1C40F")
        self.stats_lbl.pack(side="right")

        progress_frame = ctk.CTkFrame(header, fg_color="transparent")
        progress_frame.pack(fill="x", pady=(8, 0))
        self.progress = ctk.CTkProgressBar(progress_frame, height=10, progress_color="#10B981")
        self.progress.set(0)
        self.progress.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.date_picker = DatePickerButton(progress_frame, initial_date=datetime.today().date())
        self.date_picker.pack(side="right")

        self.form_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", height=380)
        self.form_scroll.pack(fill="both", expand=True, padx=80, pady=10)

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=80, pady=(0, 20))
        self.save_btn = ctk.CTkButton(footer, text="Save & Submit", width=180, height=40, corner_radius=10, 
                                     fg_color="#1f538d", hover_color="#174a7a", command=self.save_all_reports)
        self.save_btn.pack(side="right")
       
        self.add_btn = ctk.CTkButton(self.form_scroll, text="＋ Add More Tasks", fg_color="transparent", 
                                     border_width=1, border_color="#10B981", text_color="#10B981", command=self.add_item_row)
        self.add_item_row()
        self.add_btn.pack(pady=10, anchor="e", padx=10)

    def add_item_row(self):
        # 👉 Move button to bottom before adding new row
        if hasattr(self, "add_btn"):
            self.add_btn.pack_forget()


 
        container = ctk.CTkFrame(self.form_scroll, fg_color="#252525", corner_radius=10)
        container.pack(fill="x", pady=8, padx=5)
 
        top = ctk.CTkFrame(container, fg_color="transparent")
        top.pack(fill="x", padx=15, pady=(10, 5))
 
        cat_var = ctk.StringVar(value="")
        ctk.CTkOptionMenu(top, values=self.get_db_categories(), variable=cat_var, width=220,
                        fg_color="#1e1e26", button_color="#10B981").pack(side="left")
 
        ctk.CTkLabel(top, text="Hrs:").pack(side="left", padx=(15, 5))
        hour_var = ctk.StringVar(value="0")
        hour_var.trace_add("write", self.update_total_hours)
        ctk.CTkEntry(top, textvariable=hour_var, width=55, justify="center").pack(side="left")
 
        row_data = {"hour_var": hour_var, "cat_var": cat_var}
 
        ctk.CTkButton(
            top,
            text="✕",
            width=30,
            height=30,
            fg_color="#E74C3C",
            command=lambda: self.remove_item_row(container, row_data)
        ).pack(side="right", padx=5)
 
        desc = ctk.CTkTextbox(container, height=80, fg_color="#1e1e26",
                            border_width=1, border_color="#333333")
        desc.pack(fill="x", padx=15, pady=(5, 15))
 
        row_data["desc_txt"] = desc
        self.report_rows.append(row_data)
 
        # 👉 Re-pack button at bottom
        if hasattr(self, "add_btn"):
            self.add_btn.pack(pady=10, anchor="e", padx=10)
 
        self.update_total_hours()

    def update_total_hours(self, *args):
        total = 0
        for row in self.report_rows:
            try:
                val = float(row["hour_var"].get()) if row["hour_var"].get() else 0
                total += val
            except: pass
        self.stats_lbl.configure(text=f"Total: {total:.1f} / 8.0 Hours", text_color="#10B981" if total >= 8 else "#F1C40F")
        self.progress.set(min(total / 8, 1.0))

    def save_all_reports(self):
        try:
            total = 0   # ✅ ADD THIS
 
            # ✅ CALCULATE TOTAL HOURS FIRST
            for row in self.report_rows:
                try:
                    total += float(row["hour_var"].get() or 0)
                except:
                    pass
 
            # ❌ BLOCK IF OVER 8 HOURS
            if total > 8:
                messagebox.showerror("Error", "Total hours cannot exceed 8 hours!")
                return
            
            # 🚨 CHECK IF DATE ALREADY EXISTS
            selected_date = str(self.date_picker.get_date())

            self.db.cursor.execute(
                "SELECT COUNT(*) as count FROM daily_reports WHERE user_id=%s AND report_date=%s",
                (self.user['id'], selected_date)
            )

            result = self.db.cursor.fetchone()

            if result['count'] > 0:
                messagebox.showerror("Error", f"Report for {selected_date} already exists!")
                
                # ✅ GO BACK TO MAIN PAGE AFTER CLICK OK
                self.show_history_view()
                return
 
            saved_count = 0
 
            for row in self.report_rows:
                tasks = row["desc_txt"].get("1.0", "end-1c").strip()
                hours = row["hour_var"].get()
                cat = row["cat_var"].get()
 
                if tasks and float(hours or 0) > 0:
                    q = "INSERT INTO daily_reports (user_id, report_date, tasks, category, hours) VALUES (%s, %s, %s, %s, %s)"
                    self.db.cursor.execute(
                        q,
                        (self.user['id'], str(self.date_picker.get_date()), tasks, cat, hours)
                    )
                    saved_count += 1
           
            if saved_count > 0:
                self.db.conn.commit()
                messagebox.showinfo("Success", f"Saved {saved_count} sections!")
                self.show_history_view()
            else:
                messagebox.showwarning("Empty", "Nothing to save. Check hours and tasks.")
               
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror("Database Error", f"Error: {e}")

    def show_detail_view(self, date):
        self.clear_view()
 
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=80, pady=20)
 
        ctk.CTkButton(top, text="← Back", command=self.show_history_view).pack(side="left")
        ctk.CTkLabel(top, text=f"Details - {date}", font=("Arial", 20, "bold")).pack(side="left", padx=20)
 
        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=80, pady=10)
 
        try:
            query = """
                SELECT category, tasks, hours, created_at
                FROM daily_reports
                WHERE user_id = %s AND report_date = %s
                ORDER BY created_at ASC
            """
            self.db.cursor.execute(query, (self.user['id'], date))
            rows = self.db.cursor.fetchall()
 
            for r in rows:
                card = ctk.CTkFrame(
                    scroll,
                    fg_color=self.bg_card(),
                    corner_radius=10,
                    border_width=1,
                    border_color=self.border_card()
                )
                card.pack(fill="x", pady=8, padx=5)
 
                ctk.CTkLabel(card, text=f"[{r['category']}]  {r['hours']}h",
                            font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=(8, 2))
 
                ctk.CTkLabel(card, text=r['tasks'], wraplength=600,
                            text_color="gray70").pack(anchor="w", padx=10, pady=(0, 8))
 
        except Exception as e:
            print("Detail error:", e)

    def edit_report(self, date):
        self.selected_date_str = date
        self.clear_view()
        self.report_rows = []
 
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=80, pady=20)
 
        ctk.CTkButton(top, text="← Back", command=self.show_history_view).pack(side="left")
        ctk.CTkLabel(top, text=f"Edit Report - {date}", font=("Arial", 20, "bold")).pack(side="left", padx=20)
 
        # ===== TOTAL + PROGRESS (ADD THIS) =====
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.pack(fill="x", padx=80, pady=(0, 6))

        # Progress bar
        self.progress = ctk.CTkProgressBar(progress_frame, height=10, progress_color="#10B981")
        self.progress.set(0)
        self.progress.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Total text (REPLACES date button)
        self.stats_lbl = ctk.CTkLabel(
            progress_frame,
            text="Total: 0.0 / 8.0 Hours",
            font=("Arial", 14, "bold"),
            text_color="#F1C40F"
        )
        self.stats_lbl.pack(side="right")
        
        self.form_scroll = ctk.CTkScrollableFrame(self)
        self.form_scroll.pack(fill="both", expand=True, padx=80, pady=10)
 
        try:
            query = """
                SELECT id, category, tasks, hours
                FROM daily_reports
                WHERE user_id=%s AND report_date=%s
                ORDER BY created_at ASC
            """
            self.db.cursor.execute(query, (self.user['id'], date))
            rows = self.db.cursor.fetchall()
 
            for r in rows:
                self.add_item_row_with_data(r)
            if not rows:
                self.add_item_row()
                
            self.update_total_hours()
               
            self.add_btn = ctk.CTkButton(
                self.form_scroll,
                text="＋ Add More Tasks",
                fg_color="transparent",
                border_width=1,
                border_color="#10B981",
                text_color="#10B981",
                command=self.add_item_row
            )
            self.add_btn.pack(pady=10, anchor="e", padx=10)
 
        except Exception as e:
            print("Edit load error:", e)
 
        # ===== FOOTER (RIGHT ALIGN BUTTON) =====
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=80, pady=(0, 20))

        right_box = ctk.CTkFrame(footer, fg_color="transparent")
        right_box.pack(side="right")

        ctk.CTkButton(
            right_box,
            text="Update Report",
            width=180,
            height=40,
            corner_radius=10,
            fg_color="#F39C12",
            hover_color="#D68910",
            command=lambda: self.update_report(date)
        ).pack()
        
    def add_item_row_with_data(self, data):
        container = ctk.CTkFrame(self.form_scroll, fg_color="#252525", corner_radius=10)
        container.pack(fill="x", pady=8, padx=5)
 
        top = ctk.CTkFrame(container, fg_color="transparent")
        top.pack(fill="x", padx=15, pady=(10, 5))
 
        cat_var = ctk.StringVar(value=data['category'])
        ctk.CTkOptionMenu(
            top,
            values=self.get_db_categories(),
            variable=cat_var,
            width=220,
            fg_color="#1e1e26",
            button_color="#10B981",
            button_hover_color="#0ea371",
            text_color="white"
        ).pack(side="left")
 
        hour_var = ctk.StringVar(value=str(data['hours']))
        hour_var.trace_add("write", self.update_total_hours)
        ctk.CTkEntry(top, textvariable=hour_var, width=55).pack(side="left", padx=10)
 
        # ✅ DELETE BUTTON (TOP RIGHT like your design)
        row_data = {
            "id": data['id'],
            "cat_var": cat_var,
            "hour_var": hour_var
        }
 
        ctk.CTkButton(
            top,
            text="✕",
            width=30,
            height=30,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=lambda: self.delete_single_row(container, row_data)
        ).pack(side="right")
 
        desc = ctk.CTkTextbox(container, height=80)
        desc.insert("1.0", data['tasks'])
        desc.pack(fill="x", padx=15, pady=(5, 15))
 
        row_data["desc_txt"] = desc
        self.report_rows.append(row_data)

    def update_report(self, date):
        try:
            # ✅ VALIDATION FIRST
            total = 0
            for row in self.report_rows:
                try:
                    total += float(row["hour_var"].get() or 0)
                except:
                    pass

            if total > 8:
                messagebox.showerror("Error", "Total hours cannot exceed 8 hours!")
                return

            # delete old
            self.db.cursor.execute(
                "DELETE FROM daily_reports WHERE user_id=%s AND report_date=%s",
                (self.user['id'], date)
            )

            # insert new
            for row in self.report_rows:
                tasks = row["desc_txt"].get("1.0", "end-1c").strip()
                hours = row["hour_var"].get()
                cat = row["cat_var"].get()

                if tasks and float(hours or 0) > 0:
                    self.db.cursor.execute(
                        "INSERT INTO daily_reports (user_id, report_date, tasks, category, hours) VALUES (%s,%s,%s,%s,%s)",
                        (self.user['id'], date, tasks, cat, hours)
                    )

            self.db.conn.commit()
            messagebox.showinfo("Updated", "Report updated successfully")
            self.show_history_view()

        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror("Error", str(e))

    def delete_single_row(self, container, data):
        confirm = messagebox.askyesno("Delete", "Remove this task?")
 
        if not confirm:
            return
 
        try:
            # 🧨 DELETE FROM DATABASE
            if "id" in data:
                self.db.cursor.execute(
                    "DELETE FROM daily_reports WHERE id=%s",
                    (data["id"],)
                )
                self.db.conn.commit()
 
            # 🧹 REMOVE FROM UI
            container.destroy()
            self.report_rows.remove(data)
 
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror("Error", str(e))

    def remove_item_row(self, container, data):
        if len(self.report_rows) > 1:
            container.destroy()
            self.report_rows.remove(data)
            self.update_total_hours()
        else: messagebox.showwarning("Warning", "You need at least one report section.")

    def delete_report(self, date):
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete all reports for {date}?"
            )
 
            if confirm:
                try:
                    query = "DELETE FROM daily_reports WHERE user_id=%s AND report_date=%s"
                    self.db.cursor.execute(query, (self.user['id'], date))
                    self.db.conn.commit()
 
                    messagebox.showinfo("Deleted", "Report deleted successfully.")
                    self.show_history_view()
 
                except Exception as e:
                    self.db.conn.rollback()
                    messagebox.showerror("Error", str(e))

    def clear_filters(self):
        today = datetime.today().date()
        self.start_date = datetime(today.year, today.month, 1).date()
        self.end_date = today
        self.start_cal.set_date(self.start_date)
        self.end_cal.set_date(self.end_date)
        self.refresh_view()

    def export_pdf_reports(self):
        try:
            from fpdf import FPDF
            from tkinter import filedialog
            from collections import defaultdict
        except Exception as e:
            messagebox.showerror("Missing Dependency", f"{e}")
            return

        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        if end < start:
            messagebox.showerror("Error", "End date must be on or after start date.")
            return

        try:
            query = """
                SELECT report_date, category, tasks, hours
                FROM daily_reports
                WHERE user_id = %s AND report_date BETWEEN %s AND %s
                ORDER BY report_date ASC, created_at ASC
            """
            self.db.cursor.execute(query, (self.user['id'], str(start), str(end)))
            rows = self.db.cursor.fetchall()
            if not rows:
                messagebox.showinfo("No Data", "No reports found for the selected date range.")
                return
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        grouped = defaultdict(list)
        for r in rows:
            grouped[str(r['report_date'])].append(r)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"Daily_Report_{self.user.get('full_name', 'Me')}_{start}_{end}.pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not file_path:
            return

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, f"Daily Reports for {self.user.get('full_name', 'Unknown')}", ln=True, align='C')
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, f"From {start} to {end}", ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", 'B', 12)
            pdf.cell(30, 10, "Date", border=1, align='C')
            pdf.cell(35, 10, "Category", border=1, align='C')
            pdf.cell(25, 10, "Duration", border=1, align='C')
            pdf.cell(100, 10, "Task Description", border=1, align='C')
            pdf.ln()

            pdf.set_font("Arial", '', 12)
            for date in sorted(grouped.keys()):
                rows_for_date = grouped[date]
                total_rows = len(rows_for_date)
                for i, r in enumerate(rows_for_date):
                    if i == 0:
                        pdf.cell(30, 10, date, border='LTR', align='C')
                    elif i == total_rows - 1:
                        pdf.cell(30, 10, "", border='LBR', align='C')
                    else:
                        pdf.cell(30, 10, "", border='LR', align='C')

                    border_style = 'LTR' if i == 0 else 'LR'
                    if i == total_rows - 1:
                        border_style = 'LBR'

                    pdf.cell(35, 10, str(r['category']), border=border_style, align='C')
                    pdf.cell(25, 10, f"{r['hours']}h", border=border_style, align='C')
                    pdf.cell(100, 10, str(r['tasks']), border=border_style, align='C')
                    pdf.ln()

            pdf.output(file_path)
            messagebox.showinfo("Success", "PDF exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))