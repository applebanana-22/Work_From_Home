import customtkinter as ctk
from database import Database
from tkinter import messagebox, filedialog, ttk
from tkcalendar import DateEntry
import random
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class LeaderSchedule(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color=("#EBEBEB", "#1A1A1A"))
        self.db = Database()
        self.user = user 
        
        # --- AUTO DATE CALCULATION ---
        today = datetime.today()
        self.current_month_start = today.replace(day=1).date()
        next_month = today.replace(day=28) + timedelta(days=4)
        self.current_month_end = (next_month - timedelta(days=next_month.day)).date()

        self.setup_ui()
        self.auto_generate_monthly_schedule()
        self.refresh_view()

    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=10)
        
        team_id = self.user.get('team_id', 'Unknown')
        ctk.CTkLabel(header, text=f"Team {team_id} Schedule Manager", 
                     font=("Arial", 22, "bold")).pack(side="left")

        # --- ADVANCED CONTROLS ---
        control_frame = ctk.CTkFrame(self, corner_radius=10)
        control_frame.pack(fill="x", padx=30, pady=10)
        
        # 1. Date Filters
        ctk.CTkLabel(control_frame, text="From:").grid(row=0, column=0, padx=(10, 2), pady=10)
        self.start_cal = DateEntry(control_frame, width=10, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.start_cal.set_date(self.current_month_start)
        self.start_cal.grid(row=0, column=1, padx=5, pady=10)

        ctk.CTkLabel(control_frame, text="To:").grid(row=0, column=2, padx=(10, 2), pady=10)
        self.end_cal = DateEntry(control_frame, width=10, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.end_cal.set_date(self.current_month_end)
        self.end_cal.grid(row=0, column=3, padx=5, pady=10)

        # 2. Member Name Filter
        ctk.CTkLabel(control_frame, text="Name:").grid(row=0, column=4, padx=(10, 2), pady=10)
        self.name_filter = ctk.CTkEntry(control_frame, placeholder_text="Member Name", width=120)
        self.name_filter.grid(row=0, column=5, padx=5, pady=10)

        # 3. Status Filter
        ctk.CTkLabel(control_frame, text="Status:").grid(row=0, column=6, padx=(10, 2), pady=10)
        self.status_filter = ctk.CTkComboBox(control_frame, values=["All", "Office", "WFH"], width=100)
        self.status_filter.set("All")
        self.status_filter.grid(row=0, column=7, padx=5, pady=10)

        # 4. Action Buttons
        ctk.CTkButton(control_frame, text="🔍 Filter", fg_color="#34495E", width=80,
                      command=self.refresh_view).grid(row=0, column=8, padx=(15, 5), pady=10)
        
        ctk.CTkButton(control_frame, text="📄 PDF", fg_color="#E74C3C", width=80,
                      command=self.export_to_pdf).grid(row=0, column=9, padx=5, pady=10)

        self.scroll = ctk.CTkScrollableFrame(self, label_text="Team Schedule Log")
        self.scroll.pack(fill="both", expand=True, padx=30, pady=10)

    def auto_generate_monthly_schedule(self):
        leader_team_id = self.user.get('team_id')
        if not leader_team_id: return
        self.db.cursor.execute("SELECT id FROM users WHERE role = 'member' AND team_id = %s", (leader_team_id,))
        members = self.db.cursor.fetchall()
        if not members: return
        try:
            current_date = self.current_month_start
            while current_date <= self.current_month_end:
                if current_date.weekday() < 5: 
                    for m in members:
                        check_sql = "SELECT id FROM wfh_schedules WHERE user_id = %s AND schedule_date = %s"
                        self.db.cursor.execute(check_sql, (m['id'], current_date))
                        if not self.db.cursor.fetchone():
                            status = random.choice(['Office', 'WFH'])
                            sql = "INSERT INTO wfh_schedules (user_id, leader_id, schedule_date, status) VALUES (%s, %s, %s, %s)"
                            self.db.cursor.execute(sql, (m['id'], self.user['id'], current_date, status))
                current_date += timedelta(days=1)
            self.db.conn.commit()
        except Exception as e: print(f"Sync Error: {e}")

    def refresh_view(self):
        for w in self.scroll.winfo_children(): w.destroy()
        
        leader_team_id = self.user.get('team_id')
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        name_search = f"%{self.name_filter.get()}%"
        status_search = self.status_filter.get()
        today_date = datetime.today().date()

        # Build Dynamic Query
        query = """SELECT s.*, u.full_name FROM wfh_schedules s
                   JOIN users u ON s.user_id = u.id 
                   WHERE u.team_id = %s AND s.schedule_date BETWEEN %s AND %s
                   AND u.full_name LIKE %s"""
        params = [leader_team_id, start, end, name_search]

        if status_search != "All":
            query += " AND s.status = %s"
            params.append(status_search)
        
        query += " ORDER BY s.schedule_date ASC, u.full_name ASC"
        
        try:
            self.db.cursor.execute(query, tuple(params))
            rows = self.db.cursor.fetchall()

            for r in rows:
                is_today = r['schedule_date'] == today_date
                b_color = "#F39C12" if is_today else ("#F0F0F0", "#252525")
                bg_color = ("#E5E5E5", "#333333") if is_today else ("#F0F0F0", "#252525")
                
                card = ctk.CTkFrame(self.scroll, fg_color=bg_color, border_width=2 if is_today else 0, border_color=b_color)
                card.pack(fill="x", pady=2, padx=5)
                
                status_color = "#27AE60" if r['status'] == 'Office' else "#3498DB"
                day_name = r['schedule_date'].strftime('%a')
                
                info_text = f"{r['schedule_date']} ({day_name}) | {r['full_name']}"
                if is_today: info_text += " [TODAY]"

                ctk.CTkLabel(card, text=info_text, font=("Arial", 12, "bold" if is_today else "normal")).pack(side="left", padx=15, pady=8)
                
                # Edit Button
                ctk.CTkButton(card, text="Edit", width=60, height=24, fg_color="#7F8C8D",
                              command=lambda row=r: self.open_edit_popup(row)).pack(side="right", padx=10)
                
                ctk.CTkLabel(card, text=r['status'], text_color=status_color, font=("Arial", 12, "bold")).pack(side="right", padx=10)
        except Exception as e: messagebox.showerror("Error", str(e))

    def open_edit_popup(self, row_data):
        popup = ctk.CTkToplevel(self)
        popup.title("Update Team Status")
        popup.geometry("320x220")
        popup.attributes('-topmost', True) 

        ctk.CTkLabel(popup, text=f"Change Status for {row_data['full_name']}", 
                     font=("Arial", 14, "bold")).pack(pady=15)
        
        status_var = ctk.StringVar(value=row_data['status'])
        status_dropdown = ctk.CTkComboBox(popup, values=["Office", "WFH"], variable=status_var)
        status_dropdown.pack(pady=5)

        def save_change():
            new_status = status_var.get()
            try:
                # Database ကို Update လုပ်ခြင်း
                sql = "UPDATE wfh_schedules SET status = %s WHERE id = %s"
                self.db.cursor.execute(sql, (new_status, row_data['id']))
                self.db.conn.commit()
                
                popup.destroy()
                messagebox.showinfo("Success", f"Updated to {new_status} for {row_data['full_name']}")
                self.refresh_view() # Leader view ကို refresh လုပ်ခြင်း
            except Exception as e:
                messagebox.showerror("Update Fail", str(e))

        ctk.CTkButton(popup, text="Confirm Change", command=save_change, 
                      fg_color="#27AE60", hover_color="#2ECC71").pack(pady=20)

        def save_change():
            try:
                sql = "UPDATE wfh_schedules SET status = %s WHERE id = %s"
                self.db.cursor.execute(sql, (status_var.get(), row_data['id']))
                self.db.conn.commit()
                popup.destroy()
                self.refresh_view()
            except Exception as e: messagebox.showerror("Update Fail", str(e))

        ctk.CTkButton(popup, text="Save", command=save_change, fg_color="#27AE60").pack(pady=10)


    def export_to_pdf(self):
        leader_team_id = self.user.get('team_id')
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                                   initialfile=f"Team_{leader_team_id}_Schedule.pdf")
        if not file_path: return

        try:
            query = """SELECT s.schedule_date, u.full_name, s.status 
                       FROM wfh_schedules s JOIN users u ON s.user_id = u.id 
                       WHERE u.team_id = %s AND s.schedule_date BETWEEN %s AND %s 
                       ORDER BY s.schedule_date ASC"""
            self.db.cursor.execute(query, (leader_team_id, start, end))
            data = self.db.cursor.fetchall()

            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            elements.append(Paragraph(f"Team {leader_team_id} Work Schedule", styles['Title']))
            elements.append(Paragraph(f"Period: {start} to {end}", styles['Normal']))
            elements.append(Spacer(1, 15))
            
            table_data = [["Date", "Member Name", "Status"]]
            for r in data:
                day = r['schedule_date'].strftime('%a')
                table_data.append([f"{r['schedule_date']} ({day})", r['full_name'], r['status']])

            t = Table(table_data, colWidths=[130, 200, 100])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            elements.append(t)
            doc.build(elements)
            messagebox.showinfo("Export Successful", "PDF saved successfully.")
        except Exception as e:
            messagebox.showerror("Export Error", f"PDF Error: {e}")
            
    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=10)
        
        team_id = self.user.get('team_id', 'Unknown')
        ctk.CTkLabel(header, text=f"Team {team_id} Schedule Manager", 
                     font=("Arial", 22, "bold")).pack(side="left")

        # --- ADVANCED CONTROLS ---
        control_frame = ctk.CTkFrame(self, corner_radius=10)
        control_frame.pack(fill="x", padx=30, pady=10)
        
        # 1. Date Filters
        ctk.CTkLabel(control_frame, text="From:").grid(row=0, column=0, padx=(10, 2), pady=10)
        self.start_cal = DateEntry(control_frame, width=10, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.start_cal.grid(row=0, column=1, padx=5, pady=10)

        ctk.CTkLabel(control_frame, text="To:").grid(row=0, column=2, padx=(10, 2), pady=10)
        self.end_cal = DateEntry(control_frame, width=10, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.end_cal.grid(row=0, column=3, padx=5, pady=10)

        # 2. Member Name Filter
        ctk.CTkLabel(control_frame, text="Name:").grid(row=0, column=4, padx=(10, 2), pady=10)
        self.name_filter = ctk.CTkEntry(control_frame, placeholder_text="Member Name", width=120)
        self.name_filter.grid(row=0, column=5, padx=5, pady=10)

        # 3. Status Filter
        ctk.CTkLabel(control_frame, text="Status:").grid(row=0, column=6, padx=(10, 2), pady=10)
        self.status_filter = ctk.CTkComboBox(control_frame, values=["All", "Office", "WFH"], width=100)
        self.status_filter.grid(row=0, column=7, padx=5, pady=10)

        # 4. Action Buttons (Added Clear Button)
        ctk.CTkButton(control_frame, text="🔍 Filter", fg_color="#34495E", width=70,
                      command=self.refresh_view).grid(row=0, column=8, padx=(15, 2), pady=10)
        
        ctk.CTkButton(control_frame, text="🧹 Clear", fg_color="#95A5A6", width=70,
                      command=self.clear_filters).grid(row=0, column=9, padx=2, pady=10)
        
        ctk.CTkButton(control_frame, text="📄 PDF", fg_color="#E74C3C", width=70,
                      command=self.export_to_pdf).grid(row=0, column=10, padx=(2, 10), pady=10)

        # Reset defaults on startup
        self.clear_filters(refresh=False)

        self.scroll = ctk.CTkScrollableFrame(self, label_text="Team Schedule Log")
        self.scroll.pack(fill="both", expand=True, padx=30, pady=10)

    def clear_filters(self, refresh=True):
        """Resets all search fields and date picks to the current month defaults."""
        # Reset Dates
        self.start_cal.set_date(self.current_month_start)
        self.end_cal.set_date(self.current_month_end)
        
        # Reset Name Entry
        self.name_filter.delete(0, 'end')
        
        # Reset ComboBox
        self.status_filter.set("All")
        
        # Optionally refresh the list
        if refresh:
            self.refresh_view()