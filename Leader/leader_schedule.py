import customtkinter as ctk
from database import Database
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
import random
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class LeaderSchedule(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user  # This contains the logged-in Leader's team_id
        self.setup_ui()

    def setup_ui(self):
        # Header - Automatically detects Leader's team from background data
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=10)
        
        team_id = self.user.get('team_id', 'Unknown')
        ctk.CTkLabel(header, text=f"Team {team_id} WFH Scheduler", 
                     font=("Arial", 22, "bold")).pack(side="left")

        # --- CONTROLS SECTION ---
        control_frame = ctk.CTkFrame(self, corner_radius=10)
        control_frame.pack(fill="x", padx=30, pady=10)
        
        # 1. Date Range
        ctk.CTkLabel(control_frame, text="From:").grid(row=0, column=0, padx=(15, 5), pady=15)
        self.start_cal = DateEntry(control_frame, width=12, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.start_cal.grid(row=0, column=1, padx=5, pady=15)

        ctk.CTkLabel(control_frame, text="To:").grid(row=0, column=2, padx=(15, 5), pady=15)
        self.end_cal = DateEntry(control_frame, width=12, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.end_cal.grid(row=0, column=3, padx=5, pady=15)

        # 2. Action Buttons
        ctk.CTkButton(control_frame, text="🔍 Filter Range", fg_color="#34495E", width=100,
                      command=self.refresh_view).grid(row=0, column=4, padx=(20, 5), pady=15)
        
        ctk.CTkButton(control_frame, text="🎲 Generate Schedule", fg_color="#8E44AD", width=150,
                      command=self.generate_schedule).grid(row=0, column=5, padx=5, pady=15)
        
        ctk.CTkButton(control_frame, text="📄 Export PDF", fg_color="#E74C3C", width=100,
                      command=self.export_to_pdf).grid(row=0, column=6, padx=5, pady=15)

        # List Area
        self.scroll = ctk.CTkScrollableFrame(self, label_text=f"Schedule for Team {team_id}")
        self.scroll.pack(fill="both", expand=True, padx=30, pady=10)
        
        self.refresh_view()

    def generate_schedule(self):
        # Get team_id automatically from the Leader's profile (Background logic)
        leader_team_id = self.user.get('team_id')
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        
        if not leader_team_id:
            messagebox.showerror("Error", "Leader profile is missing team_id assignment.")
            return

        # Fetch only members belonging to THIS leader's team
        self.db.cursor.execute("SELECT id, full_name FROM users WHERE role = 'member' AND team_id = %s", (leader_team_id,))
        members = self.db.cursor.fetchall()
        
        if not members:
            messagebox.showwarning("Empty", f"No members found in your Team (ID: {leader_team_id})")
            return

        try:
            current_date = start
            while current_date <= end:
                # weekday < 5 skips Saturday(5) and Sunday(6)
                if current_date.weekday() < 5: 
                    for m in members:
                        status = random.choice(['Office', 'WFH'])
                        sql = """INSERT INTO wfh_schedules (user_id, leader_id, schedule_date, status) 
                                 VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE status = VALUES(status)"""
                        self.db.cursor.execute(sql, (m['id'], self.user['id'], current_date, status))
                current_date += timedelta(days=1)
            
            self.db.conn.commit()
            messagebox.showinfo("Success", f"Schedule generated for your team members.")
            self.refresh_view()
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
            
            elements.append(Paragraph(f"Work Schedule: Team {leader_team_id}", styles['Title']))
            elements.append(Paragraph(f"Interval: {start} to {end}", styles['Normal']))
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
            messagebox.showinfo("Success", "PDF Exported")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_view(self):
        for w in self.scroll.winfo_children(): w.destroy()
        leader_team_id = self.user.get('team_id')
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()

        query = """SELECT s.*, u.full_name FROM wfh_schedules s
                   JOIN users u ON s.user_id = u.id 
                   WHERE u.team_id = %s AND s.schedule_date BETWEEN %s AND %s
                   ORDER BY s.schedule_date ASC, u.full_name ASC"""
        self.db.cursor.execute(query, (leader_team_id, start, end))
        rows = self.db.cursor.fetchall()

        for r in rows:
            card = ctk.CTkFrame(self.scroll, fg_color=("#F0F0F0", "#252525"))
            card.pack(fill="x", pady=2, padx=5)
            color = "#27AE60" if r['status'] == 'Office' else "#3498DB"
            day = r['schedule_date'].strftime('%a')
            ctk.CTkLabel(card, text=f"{r['schedule_date']} ({day}) | {r['full_name']}").pack(side="left", padx=15, pady=5)
            ctk.CTkLabel(card, text=r['status'], text_color=color, font=("Arial", 12, "bold")).pack(side="right", padx=15)