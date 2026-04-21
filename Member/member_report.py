import customtkinter as ctk
import calendar
from datetime import datetime
from database import Database
from tkinter import messagebox
 
class MemberReportFrame(ctk.CTkFrame):
    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.db = Database()
        self.configure(fg_color="transparent")
       
        # State Management
        self.now = datetime.now()
        self.cur_year = self.now.year
        self.cur_month = self.now.month
        self.selected_date_str = self.now.strftime('%Y-%m-%d')
        self.cal_visible = False
        self.report_rows = []  # Stores dicts: {'container', 'cat_var', 'hour_var', 'desc_txt'}
 
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
 
    # --- 1. HISTORY VIEW (Grouped by Day) ---
    def show_history_view(self):
        self.clear_view()
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Daily Report History", font=("Arial", 24, "bold"), text_color="#00fbff").pack(side="left")
        ctk.CTkButton(header, text="+ Add Daily Report", fg_color="#1f538d", height=35, command=self.show_form_view).pack(side="right")
        ctk.CTkButton(
            header,
            text="Export PDF",
            fg_color="#DC2626",
            command=self.export_pdf_reports
        ).pack(side="right", padx=10)
        list_header = ctk.CTkFrame(self, fg_color="#2b2b2b", height=40)
        list_header.pack(fill="x", padx=30, pady=(10, 0))
        ctk.CTkLabel(list_header, text="Date", width=120).pack(side="left", padx=10)
        ctk.CTkLabel(list_header, text="Total Hrs", width=100).pack(side="left", padx=10)
        ctk.CTkLabel(list_header, text="Title", width=200).pack(side="left", padx=20)
 
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=25, pady=10)
 
        try:
            # SQL groups entries by date so history is clean
            query = """
                SELECT report_date, SUM(hours) as total_h,
                GROUP_CONCAT(DISTINCT category SEPARATOR ', ') as title
                FROM daily_reports
                WHERE user_id = %s
                GROUP BY report_date
                ORDER BY report_date DESC
            """
            self.db.cursor.execute(query, (self.user['id'],))
            reports = self.db.cursor.fetchall()
            for r in reports:
                row = ctk.CTkFrame(scroll, fg_color="#1e1e1e", height=45)
                row.pack(fill="x", pady=2)
               
                ctk.CTkLabel(row, text=str(r['report_date']), width=120, text_color="gray70").pack(side="left", padx=10)
               
                # Hour highlighting (Green if 8+ hours)
                h_val = float(r['total_h'])
                h_color = "#10B981" if h_val >= 8 else "#F1C40F"
                ctk.CTkLabel(row, text=f"{h_val}h", width=100, text_color=h_color, font=("Arial", 12, "bold")).pack(side="left", padx=10)
               
                title_txt = (r['title'][:75] + '..') if len(r['title']) > 75 else r['title']
 
                ctk.CTkLabel(
                    row,
                    text=title_txt,
                    anchor="w",
                    text_color="#10B981"
                ).pack(side="left", padx=20, fill="x", expand=True)
 
                btn_frame = ctk.CTkFrame(row, fg_color="transparent")
                btn_frame.pack(side="right", padx=10)
 
                # VIEW BUTTON
                ctk.CTkButton(
                    btn_frame,
                    text="View",
                    width=70,
                    fg_color="#1f538d",
                    command=lambda d=r['report_date']: self.show_detail_view(d)
                ).pack(side="left", padx=5)
 
                # EDIT BUTTON
                ctk.CTkButton(
                    btn_frame,
                    text="Edit",
                    width=70,
                    fg_color="#F39C12",
                    command=lambda d=r['report_date']: self.edit_report(d)
                ).pack(side="left", padx=5)
 
                # DELETE BUTTON
                ctk.CTkButton(
                    btn_frame,
                    text="Delete",
                    width=70,
                    fg_color="#E74C3C",
                    command=lambda d=r['report_date']: self.delete_report(d)
                ).pack(side="left", padx=5)
        except Exception as e:
            print(f"History Error: {e}")
           
       
 
    # --- 2. ENTRY FORM (With Hours & Progress) ---
    def show_form_view(self):
        self.clear_view()
        self.report_rows = []
       
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=30, pady=20)
        ctk.CTkButton(top_bar, text="← Back", width=80, fg_color="#333333", command=self.show_history_view).pack(side="left")
       
        # Stats Display
        self.stats_lbl = ctk.CTkLabel(top_bar, text="Total: 0 / 8 Hours", font=("Arial", 16, "bold"), text_color="#F1C40F")
        self.stats_lbl.pack(side="right", padx=20)
       
        # Container for progress + date (same row)
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.pack(fill="x", padx=40, pady=(0, 10))
 
        # Progress bar (left)
        self.progress = ctk.CTkProgressBar(progress_frame, height=10, progress_color="#10B981")
        self.progress.set(0)
        self.progress.pack(side="left", fill="x", expand=True, padx=(0, 10))
 
        # Date button (right)
        self.date_btn = ctk.CTkButton(
            progress_frame,
            text=f"📅 {self.selected_date_str}",
            width=140,
            fg_color="#2b2b2b",
            command=self.toggle_calendar
        )
        self.date_btn.pack(side="right")
 
        self.cal_frame = ctk.CTkFrame(self, fg_color="#252525", corner_radius=15)
        self.setup_calendar_ui()
 
        self.form_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", height=380)
        self.form_scroll.pack(fill="both", expand=True, padx=20, pady=10)
       
        self.add_item_row() # Initial Row
 
        # Add button INSIDE scroll (dynamic position)
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
 
        btn_f = ctk.CTkFrame(self, fg_color="transparent")
        btn_f.pack(fill="x", padx=40, pady=20)
        ctk.CTkButton(btn_f, text="Save & Submit Report", fg_color="#1f538d", height=45, command=self.save_all_reports).pack(fill="x")
 
    def update_total_hours(self, *args):
        total = 0
        for row in self.report_rows:
            try:
                val = float(row["hour_var"].get()) if row["hour_var"].get() else 0
                total += val
            except: pass
        self.stats_lbl.configure(text=f"Total: {total} / 8 Hours")
        self.progress.set(min(total / 8, 1.0))
        self.stats_lbl.configure(text_color="#10B981" if total >= 8 else "#F1C40F")
 
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
 
    def remove_item_row(self, container, data):
        if len(self.report_rows) > 1:
            container.destroy()
            self.report_rows.remove(data)
            self.update_total_hours()
        else:
            messagebox.showwarning("Warning", "You need at least one report section.")
 
    # --- 3. SAVE TO DATABASE ---
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
 
            saved_count = 0
 
            for row in self.report_rows:
                tasks = row["desc_txt"].get("1.0", "end-1c").strip()
                hours = row["hour_var"].get()
                cat = row["cat_var"].get()
 
                if tasks and float(hours or 0) > 0:
                    q = "INSERT INTO daily_reports (user_id, report_date, tasks, category, hours) VALUES (%s, %s, %s, %s, %s)"
                    self.db.cursor.execute(q, (self.user['id'], self.selected_date_str, tasks, cat, hours))
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
        top.pack(fill="x", padx=30, pady=20)
 
        ctk.CTkButton(top, text="← Back", command=self.show_history_view).pack(side="left")
        ctk.CTkLabel(top, text=f"Details - {date}", font=("Arial", 20, "bold")).pack(side="left", padx=20)
 
        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
 
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
                card = ctk.CTkFrame(scroll, fg_color="#252525", corner_radius=10)
                card.pack(fill="x", pady=8, padx=5)
 
                ctk.CTkLabel(card, text=f"[{r['category']}]  {r['hours']}h",
                            font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=(8, 2))
 
                ctk.CTkLabel(card, text=r['tasks'], wraplength=600,
                            text_color="gray70").pack(anchor="w", padx=10, pady=(0, 8))
 
        except Exception as e:
            print("Detail error:", e)
           
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
       
    def edit_report(self, date):
        self.selected_date_str = date
        self.clear_view()
        self.report_rows = []
 
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=20)
 
        ctk.CTkButton(top, text="← Back", command=self.show_history_view).pack(side="left")
        ctk.CTkLabel(top, text=f"Edit Report - {date}", font=("Arial", 20, "bold")).pack(side="left", padx=20)
 
        self.form_scroll = ctk.CTkScrollableFrame(self)
        self.form_scroll.pack(fill="both", expand=True, padx=20, pady=10)
 
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
 
        ctk.CTkButton(
            self,
            text="Update Report",
            fg_color="#F39C12",
            command=lambda: self.update_report(date)
        ).pack(pady=20)
 
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
            width=220
        ).pack(side="left")
 
        hour_var = ctk.StringVar(value=str(data['hours']))
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
 
    # --- CALENDAR METHODS ---
    def setup_calendar_ui(self):
        nav = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        nav.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(nav, text="<", width=30, command=self.prev_month).pack(side="left")
        self.month_label = ctk.CTkLabel(nav, text="", font=("Arial", 13, "bold"))
        self.month_label.pack(side="left", expand=True)
        ctk.CTkButton(nav, text=">", width=30, command=self.next_month).pack(side="right")
        self.grid_frame = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.render_calendar()
 
    def render_calendar(self):
        for w in self.grid_frame.winfo_children(): w.destroy()
        self.month_label.configure(text=f"{calendar.month_name[self.cur_month]} {self.cur_year}")
        cal = calendar.monthcalendar(self.cur_year, self.cur_month)
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day != 0:
                    btn = ctk.CTkButton(self.grid_frame, text=str(day), width=35, height=35,
                                        fg_color="transparent", command=lambda d=day: self.select_day(d))
                    btn.grid(row=r, column=c, padx=2, pady=2)
 
    def select_day(self, day):
        self.selected_date_str = f"{self.cur_year}-{self.cur_month:02d}-{day:02d}"
        self.date_btn.configure(text=f"📅 {self.selected_date_str}")
        self.toggle_calendar()
 
    def prev_month(self):
        self.cur_month = 12 if self.cur_month == 1 else self.cur_month - 1
        if self.cur_month == 12: self.cur_year -= 1
        self.render_calendar()
 
    def next_month(self):
        self.cur_month = 1 if self.cur_month == 12 else self.cur_month + 1
        if self.cur_month == 1: self.cur_year += 1
        self.render_calendar()
 
    def toggle_calendar(self):
        if not self.cal_visible:
            self.cal_frame.pack(after=self.date_btn, pady=10, padx=40)
        else:
            self.cal_frame.pack_forget()
        self.cal_visible = not self.cal_visible
       
    def export_pdf_reports(self):
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from tkinter import filedialog
        except Exception as e:
            messagebox.showerror("Missing Dependency", f"{e}")
            return
 
        # Fetch data
        try:
            query = """
                SELECT report_date, category, tasks, hours
                FROM daily_reports
                WHERE user_id = %s
                ORDER BY report_date DESC
            """
            self.db.cursor.execute(query, (self.user['id'],))
            rows = self.db.cursor.fetchall()
 
            if not rows:
                messagebox.showwarning("No Data", "No reports to export.")
                return
 
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return
 
        # Save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile="Daily_Report.pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
 
        if not file_path:
            return
 
        # Create PDF
        try:
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []
 
            elements.append(Paragraph("Daily Report", styles["Title"]))
            elements.append(Paragraph(f"User: {self.user.get('full_name', 'Unknown')}", styles["Normal"]))
            elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
            elements.append(Spacer(1, 12))
 
            # Table
            table_data = [["Date", "Category", "Hours", "Tasks"]]
 
            for r in rows:
                table_data.append([
                    str(r["report_date"]),
                    str(r["category"]),
                    str(r["hours"]),
                    str(r["tasks"]),
                ])
 
            table = Table(table_data, repeatRows=1)
 
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ]))
 
            elements.append(table)
 
            doc.build(elements)
 
            messagebox.showinfo("Success", "PDF exported successfully!")
 
        except Exception as e:
            messagebox.showerror("Export Error", str(e))