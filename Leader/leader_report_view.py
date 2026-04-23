import customtkinter as ctk
from database import Database
from tkinter import messagebox, filedialog
from datetime import datetime
import calendar
from fpdf import FPDF
from tkcalendar import DateEntry
from collections import defaultdict
 
class LeaderReportView(ctk.CTkFrame):
    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.db = Database()
        self.user = user
        self.configure(fg_color="transparent")
 
        # --- Filter & Calendar State ---
        self.now = datetime.now()
        self.cur_year = self.now.year
        self.cur_month = self.now.month
        self.filter_date_str = self.now.strftime('%Y-%m-%d')
        self.cal_visible = False
        self.member_var = ctk.StringVar(value="")
 
        # Main Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
 
        # Create Calendar Frame here so it's a child of the main view, not the header
        self.cal_frame = ctk.CTkFrame(self, fg_color="#252525", corner_radius=15, border_width=2, border_color="#333333")
 
        self.show_reports_list()
 
    def get_member_names(self):
        try:
            query = "SELECT full_name FROM users WHERE role = 'member' AND team_id = %s ORDER BY full_name ASC"
            self.db.cursor.execute(query, (self.user.get('team_id'),))
            return [row['full_name'] for row in self.db.cursor.fetchall()]
        except Exception:
            return []
 
    def clear_container(self):
        """Clears UI for switching views"""
        for widget in self.container.winfo_children():
            widget.destroy()
        if self.cal_visible:
            self.toggle_filter_calendar()
 
    # --- VIEW 1: GROUPED REPORT LIST ---
    def show_reports_list(self):
        self.clear_container()
 
        # Header Section
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=100, pady=20)
       
        ctk.CTkLabel(header, text="Team Daily Progress",
                     font=("Arial", 24, "bold"), text_color="#00fbff").pack(side="left")
 
        # Export PDF button
        ctk.CTkButton(
            header,
            text="📄 Export PDF",
            fg_color="#10B981",
            width=120,
            height=35,
            command=self.export_pdf
        ).pack(side="right", padx=10)

        # Category button (NEW)
        ctk.CTkButton(
            header,
            text="⚙ Categories",
            fg_color="#f59e0b",
            width=130,
            height=35,
            command=self.show_category_ui
        ).pack(side="right", padx=10)

        controls = ctk.CTkFrame(self.container, fg_color="transparent")
        controls.pack(fill="x", padx=100, pady=(5, 0))
 
        member_options = [" "] + self.get_member_names()
        self.member_dropdown = ctk.CTkOptionMenu(
            controls,
            values=member_options,
            variable=self.member_var,
            width=220,
            fg_color="#1e1e1e",
            button_color="#10B981"
        )
        self.member_dropdown.pack(side="left")
 
        self.date_btn = ctk.CTkButton(controls, text=f"📅 {self.filter_date_str}",
                                      fg_color="#2b2b2b", width=150, height=35,
                                      command=self.toggle_filter_calendar)
        self.date_btn.pack(side="left", padx=10)
 
        ctk.CTkButton(controls, text="Search", fg_color="#2563eb", width=120, height=35,
                      command=self.perform_search).pack(side="left", padx=10)
 
        # Table Headers
        list_header = ctk.CTkFrame(self.container, fg_color="#2b2b2b", height=40)
        list_header.pack(fill="x", padx=100, pady=(10, 0))
       
        ctk.CTkLabel(list_header, text="Team Member", width=180, font=("Arial", 12, "bold")).pack(side="left", padx=20)
        ctk.CTkLabel(list_header, text="Total Hrs", width=80, font=("Arial", 12, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(list_header, text="Daily Summary", font=("Arial", 12, "bold")).pack(side="left", padx=20)
 
        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=25, pady=10)
 
        try:
            member_choice = self.member_var.get()
            query = """
                SELECT u.full_name, SUM(dr.hours) as total_h,
                GROUP_CONCAT(CONCAT('• [', dr.category, '] ', dr.tasks) SEPARATOR '\n') as daily_summary
                FROM users u
                JOIN daily_reports dr ON u.id = dr.user_id
                WHERE dr.report_date = %s
                  AND u.role = 'member'
                  AND u.team_id = %s
            """
            params = [self.filter_date_str, self.user.get('team_id')]
            if member_choice and member_choice != " ":
                query += " AND u.full_name = %s"
                params.append(member_choice)
 
            query += "\n                GROUP BY u.id\n                ORDER BY u.full_name ASC\n            "
            self.db.cursor.execute(query, tuple(params))
            reports = self.db.cursor.fetchall()
 
            if not reports:
                member_choice = self.member_var.get()
 
                if member_choice.strip():   # ✅ handles "" and " "
                    msg = f"No report submitted by {member_choice} for {self.filter_date_str}"
                else:
                    msg = f"No reports submitted for {self.filter_date_str}"
 
                ctk.CTkLabel(
                    scroll,
                    text=msg,
                    text_color="gray70",
                    font=("Arial", 14)
                ).pack(pady=50)
 
            for r in reports:
                card = ctk.CTkFrame(scroll, fg_color="#1e1e1e", corner_radius=10)
                card.pack(fill="x", pady=5, padx=65)
               
                ctk.CTkLabel(card, text=r['full_name'], width=180, font=("Arial", 14, "bold"),
                             text_color="#00fbff", anchor="w").pack(side="left", padx=20, pady=15)
               
                h_val = float(r['total_h'] or 0)
                h_color = "#10B981" if h_val >= 8 else "#F1C40F"
                ctk.CTkLabel(card, text=f"{h_val}h", width=80, text_color=h_color,
                             font=("Arial", 15, "bold")).pack(side="left", padx=10)
 
                # summary (expandable space)
                ctk.CTkLabel(
                    card,
                    text=r['daily_summary'],
                    justify="left",
                    anchor="w",
                    text_color="gray85",
                    wraplength=600
                ).pack(side="left", padx=20, pady=10, fill="x", expand=True)
 
                # ✅ ADD BUTTON
                ctk.CTkButton(
                    card,
                    text="View Detail",
                    width=110,
                    fg_color="#1f538d",
                    command=lambda name=r['full_name']: self.show_member_detail(name)
                ).pack(side="right", padx=10)
 
        except Exception as e:
            print(f"Fetch Error: {e}")
           
    def show_member_detail(self, member_name):
        self.clear_container()
 
        # Header
        top = ctk.CTkFrame(self.container, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=20)
 
        ctk.CTkButton(top, text="← Back", command=self.show_reports_list).pack(side="left")
        ctk.CTkLabel(
            top,
            text=f"{member_name} - {self.filter_date_str}",
            font=("Arial", 20, "bold")
        ).pack(side="left", padx=20)
 
        scroll = ctk.CTkScrollableFrame(self.container)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
 
        try:
            query = """
                SELECT dr.category, dr.tasks, dr.hours, dr.created_at
                FROM daily_reports dr
                JOIN users u ON u.id = dr.user_id
                WHERE u.full_name = %s AND dr.report_date = %s AND u.team_id = %s
                ORDER BY dr.created_at ASC
            """
            self.db.cursor.execute(query, (member_name, self.filter_date_str, self.user.get('team_id')))
            rows = self.db.cursor.fetchall()
 
            for r in rows:
                card = ctk.CTkFrame(scroll, fg_color="#252525", corner_radius=10)
                card.pack(fill="x", pady=8, padx=5)
 
                ctk.CTkLabel(
                    card,
                    text=f"[{r['category']}] {r['hours']}h",
                    font=("Arial", 13, "bold")
                ).pack(anchor="w", padx=10, pady=(8, 2))
 
                ctk.CTkLabel(
                    card,
                    text=r['tasks'],
                    wraplength=600,
                    text_color="gray70"
                ).pack(anchor="w", padx=10, pady=(0, 8))
 
                ctk.CTkLabel(
                    card,
                    text=str(r['created_at']),
                    font=("Arial", 10),
                    text_color="gray50"
                ).pack(anchor="e", padx=10, pady=(0, 5))
 
        except Exception as e:
            print("Leader detail error:", e)
 
    # --- CALENDAR DROPDOWN LOGIC ---
    def toggle_filter_calendar(self):
        if not self.cal_visible:
            self.setup_calendar_ui()
            self.cal_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.cal_frame.lift()
            self.date_btn.configure(fg_color="#10B981")
        else:
            self.cal_frame.place_forget()
            self.date_btn.configure(fg_color="#2b2b2b")
        self.cal_visible = not self.cal_visible
       
    def setup_calendar_ui(self):
        for w in self.cal_frame.winfo_children(): w.destroy()
       
        nav = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        nav.pack(fill="x", padx=10, pady=10)
       
        ctk.CTkButton(nav, text="<", width=30, fg_color="#333333", command=self.prev_month).pack(side="left")
        self.month_lbl = ctk.CTkLabel(nav, text=f"{calendar.month_name[self.cur_month]} {self.cur_year}",
                                      font=("Arial", 13, "bold"), text_color="#00fbff")
        self.month_lbl.pack(side="left", expand=True)
        ctk.CTkButton(nav, text=">", width=30, fg_color="#333333", command=self.next_month).pack(side="right")
 
        grid = ctk.CTkFrame(self.cal_frame, fg_color="transparent")
        grid.pack(padx=10, pady=(5, 15))
 
        days = calendar.monthcalendar(self.cur_year, self.cur_month)
        for r, week in enumerate(days):
            for c, day in enumerate(week):
                if day != 0:
                    is_selected = f"{self.cur_year}-{self.cur_month:02d}-{day:02d}" == self.filter_date_str
                    btn_color = "#10B981" if is_selected else "transparent"
                   
                    ctk.CTkButton(grid, text=str(day), width=35, height=35,
                                  fg_color=btn_color, hover_color="#1f538d",
                                  command=lambda d=day: self.select_date(d)).grid(row=r, column=c, padx=1, pady=1)
 
    def select_date(self, day):
        self.filter_date_str = f"{self.cur_year}-{self.cur_month:02d}-{day:02d}"
        self.date_btn.configure(text=f"📅 {self.filter_date_str}")
        self.toggle_filter_calendar()
 
    def prev_month(self):
        self.cur_month = 12 if self.cur_month == 1 else self.cur_month - 1
        if self.cur_month == 12: self.cur_year -= 1
        self.setup_calendar_ui()
 
    def next_month(self):
        self.cur_month = 1 if self.cur_month == 12 else self.cur_month + 1
        if self.cur_month == 1: self.cur_year += 1
        self.setup_calendar_ui()
 
    # --- VIEW 2: CATEGORY MANAGEMENT ---
    def perform_search(self):
        self.show_reports_list()
 
    def show_category_ui(self):
        self.clear_container()
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkButton(header, text="← Back", width=100, command=self.show_reports_list).pack(side="left")
        ctk.CTkLabel(header, text="Manage Categories", font=("Arial", 22, "bold"), text_color="#10B981").pack(side="left", padx=20)
 
        input_f = ctk.CTkFrame(self.container, fg_color="#1e1e1e", corner_radius=12)
        input_f.pack(fill="x", padx=30, pady=10)
        self.cat_entry = ctk.CTkEntry(input_f, placeholder_text="New category name...", width=300)
        self.cat_entry.pack(side="left", padx=20, pady=20)
        ctk.CTkButton(input_f, text="Add", width=100, command=self.add_category).pack(side="left")
 
        self.cat_scroll = ctk.CTkScrollableFrame(self.container, label_text="Current Categories", fg_color="transparent")
        self.cat_scroll.pack(fill="both", expand=True, padx=30, pady=10)
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
            row = ctk.CTkFrame(self.cat_scroll, fg_color="#2b2b2b")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=cat['name']).pack(side="left", padx=20, pady=10)
            ctk.CTkButton(row, text="Delete", width=70, fg_color="#E74C3C",
                          command=lambda cid=cat['id']: self.delete_category(cid)).pack(side="right", padx=10)
 
    def delete_category(self, cat_id):
        if messagebox.askyesno("Confirm", "Delete this category?"):
            self.db.cursor.execute("DELETE FROM report_categories WHERE id = %s", (cat_id,))
            self.db.conn.commit()
            self.refresh_categories()

    def export_pdf(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Export PDF")
        popup.geometry("400x300")
        popup.grab_set()          # force focus
        popup.resizable(True, True)

        # Start date frame
        frame1 = ctk.CTkFrame(popup, fg_color="transparent")
        frame1.pack(pady=(20,5))
        ctk.CTkLabel(frame1, text="Start Date:", font=("Arial", 12)).pack(side="left")
        start_date = DateEntry(frame1, date_pattern='yyyy-mm-dd', width=12)
        start_date.pack(side="left", pady=5)

        # End date frame
        frame2 = ctk.CTkFrame(popup, fg_color="transparent")
        frame2.pack(pady=5)
        ctk.CTkLabel(frame2, text="End Date:", font=("Arial", 12)).pack(side="left")
        end_date = DateEntry(frame2, date_pattern='yyyy-mm-dd', width=12)
        end_date.pack(side="left", pady=5)

        # Member frame
        frame3 = ctk.CTkFrame(popup, fg_color="transparent")
        frame3.pack(pady=5)
        ctk.CTkLabel(frame3, text="Member:", font=("Arial", 12)).pack(side="left")
        members = self.get_member_names()
        member_var = ctk.StringVar()
        member_combo = ctk.CTkOptionMenu(frame3, values=members, variable=member_var, width=200)
        member_combo.pack(side="left", pady=5)

        # Download button
        ctk.CTkButton(popup, text="Download", fg_color="#10B981", command=lambda: self.generate_pdf(start_date.get_date(), end_date.get_date(), member_var.get(), popup)).pack(pady=20)

    def generate_pdf(self, start, end, member, popup):
        if end < start:
            messagebox.showerror("Error", "End date must be on or after start date.")
            return
        if not member:
            messagebox.showerror("Error", "Please select a member.")
            return

        # Query reports
        query = """
            SELECT report_date, category, tasks, hours
            FROM daily_reports dr
            JOIN users u ON u.id = dr.user_id
            WHERE u.full_name = %s AND dr.report_date BETWEEN %s AND %s
            ORDER BY report_date ASC, dr.created_at ASC
        """
        self.db.cursor.execute(query, (member, str(start), str(end)))
        reports = self.db.cursor.fetchall()

        if not reports:
            messagebox.showinfo("No Data", "No reports found for the selected member and date range.")
            return

        # Group by date
        grouped = defaultdict(list)
        for r in reports:
            grouped[str(r['report_date'])].append(r)

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Daily Reports for {member}", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"From {start} to {end}", ln=True, align='C')
        pdf.ln(10)

        # Table headers
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(30, 10, "Date", border=1, align='C')
        pdf.cell(35, 10, "Category", border=1, align='C')
        pdf.cell(25, 10, "Duration", border=1, align='C')
        pdf.cell(100, 10, "Task Description", border=1, align='C')
        pdf.ln()

        # Table rows

        pdf.set_font("Arial", '', 12)
        for date in sorted(grouped.keys()):
            rows = grouped[date]
            total_rows = len(rows)

            for i, r in enumerate(rows):

                # DATE COLUMN (merged look)
                if i == 0:
                    pdf.cell(30, 10, date, border='LTR', align='C')
                elif i == total_rows - 1:
                    pdf.cell(30, 10, "", border='LBR', align='C')
                else:
                    pdf.cell(30, 10, "", border='LR', align='C')

                # border style for other columns
                if i == 0:
                    border_style = 'LTR'
                elif i == total_rows - 1:
                    border_style = 'LBR'
                else:
                    border_style = 'LR'

                pdf.cell(35, 10, r['category'], border=border_style, align='C')
                pdf.cell(25, 10, f"{r['hours']}h", border=border_style, align='C')
                pdf.cell(100, 10, r['tasks'], border=border_style, align='C')

                pdf.ln()

        # Save file
        default_name = f"Daily reports for {member}.pdf"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF"
        )
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Success", f"PDF saved to {file_path}")
            popup.destroy()