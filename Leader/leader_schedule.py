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
        self.user = user 
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=10)
        ctk.CTkLabel(header, text="Team WFH Scheduler", font=("Arial", 22, "bold")).pack(side="left")

        # Filter & Action Bar
        filter_frame = ctk.CTkFrame(self, corner_radius=10)
        filter_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(filter_frame, text="From:").grid(row=0, column=0, padx=(20, 5), pady=15)
        self.start_cal = DateEntry(filter_frame, width=12, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.start_cal.grid(row=0, column=1, padx=5, pady=15)

        ctk.CTkLabel(filter_frame, text="To:").grid(row=0, column=2, padx=(20, 5), pady=15)
        self.end_cal = DateEntry(filter_frame, width=12, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.end_cal.grid(row=0, column=3, padx=5, pady=15)

        # Buttons
        ctk.CTkButton(filter_frame, text="🔍 Filter", fg_color="#34495E", width=80,
                      command=lambda: self.refresh_view()).grid(row=0, column=4, padx=(20, 5), pady=15)
        
        ctk.CTkButton(filter_frame, text="🎲 Generate", fg_color="#8E44AD", width=100,
                      command=self.generate_schedule).grid(row=0, column=5, padx=5, pady=15)
        
        ctk.CTkButton(filter_frame, text="📄 Export PDF", fg_color="#E74C3C", width=100,
                      command=self.export_to_pdf).grid(row=0, column=6, padx=5, pady=15)

        # Scrollable Area
        self.scroll = ctk.CTkScrollableFrame(self, label_text="Schedule Interval View")
        self.scroll.pack(fill="both", expand=True, padx=30, pady=10)
        
        self.refresh_view()

    def generate_schedule(self):
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        
        if end < start:
            messagebox.showerror("Error", "End date is before Start date!")
            return

        self.db.cursor.execute("SELECT id, full_name FROM users WHERE role = 'Member'")
        members = self.db.cursor.fetchall()
        
        try:
            current_date = start
            while current_date <= end:
                if current_date.weekday() < 5: # Skip Sat/Sun
                    for m in members:
                        status = random.choice(['Office', 'WFH'])
                        sql = """INSERT INTO wfh_schedules (user_id, leader_id, schedule_date, status) 
                                 VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE status = VALUES(status)"""
                        self.db.cursor.execute(sql, (m['id'], self.user['id'], current_date, status))
                current_date += timedelta(days=1)
            
            self.db.conn.commit()
            messagebox.showinfo("Success", "Schedule Generated!")
            self.refresh_view()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_to_pdf(self):
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()
        
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                                 initialfile=f"WFH_Schedule_{start}_to_{end}.pdf",
                                                 filetypes=[("PDF files", "*.pdf")])
        if not file_path: return

        try:
            # Query ONLY the selected interval
            query = """SELECT s.schedule_date, u.full_name, s.status 
                       FROM wfh_schedules s JOIN users u ON s.user_id = u.id 
                       WHERE s.schedule_date BETWEEN %s AND %s 
                       ORDER BY s.schedule_date ASC"""
            self.db.cursor.execute(query, (start, end))
            data = self.db.cursor.fetchall()

            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title & Subtitle
            elements.append(Paragraph("Team Work Schedule Report", styles['Title']))
            elements.append(Paragraph(f"Interval: {start} to {end}", styles['Heading3']))
            elements.append(Spacer(1, 12))
            
            # Table Data
            table_data = [["Date (Day)", "Employee Name", "Work Status"]]
            for r in data:
                day_name = r['schedule_date'].strftime('%a')
                table_data.append([f"{r['schedule_date']} ({day_name})", r['full_name'], r['status']])

            # Table Styling
            t = Table(table_data, colWidths=[130, 200, 100])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
            ]))
            
            elements.append(t)
            doc.build(elements)
            messagebox.showinfo("Success", f"PDF Exported: {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def refresh_view(self):
        for w in self.scroll.winfo_children(): w.destroy()
        start = self.start_cal.get_date()
        end = self.end_cal.get_date()

        query = """SELECT s.*, u.full_name FROM wfh_schedules s
                   JOIN users u ON s.user_id = u.id 
                   WHERE s.schedule_date BETWEEN %s AND %s
                   ORDER BY s.schedule_date ASC, u.full_name ASC"""
        self.db.cursor.execute(query, (start, end))
        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(self.scroll, text="No data found for this period.", text_color="gray").pack(pady=20)
            return

        for r in rows:
            card = ctk.CTkFrame(self.scroll, fg_color=("#F0F0F0", "#252525"))
            card.pack(fill="x", pady=2, padx=5)
            color = "#27AE60" if r['status'] == 'Office' else "#3498DB"
            day = r['schedule_date'].strftime('%a')
            ctk.CTkLabel(card, text=f"{r['schedule_date']} ({day}) | {r['full_name']}").pack(side="left", padx=15, pady=5)
            ctk.CTkLabel(card, text=r['status'], text_color=color, font=("Arial", 12, "bold")).pack(side="right", padx=15)