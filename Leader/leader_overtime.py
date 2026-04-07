import customtkinter as ctk
from database import Database
from tkinter import messagebox
from datetime import datetime

class LeaderOvertime(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user  # The Leader

        # --- Header ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Assign Overtime", font=("Arial", 24, "bold")).pack(side="left")

        # --- Layout: Left (Form) | Right (Sent Requests List) ---
        self.main_f = ctk.CTkFrame(self, fg_color="transparent")
        self.main_f.pack(fill="both", expand=True, padx=20)

        self.setup_request_form()
        self.setup_sent_requests_list()

    def setup_request_form(self):
        """Form for Leader to request OT from a member"""
        form_f = ctk.CTkFrame(self.main_f, width=350, corner_radius=12)
        form_f.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(form_f, text="Create OT Request", font=("Arial", 16, "bold")).pack(pady=15)

        # 1. Select Member
        ctk.CTkLabel(form_f, text="Select Member:").pack(anchor="w", padx=20)
        self.db.cursor.execute("SELECT full_name FROM users WHERE role != 'Leader'")
        members = [row['full_name'] for row in self.db.cursor.fetchall()]
        self.member_var = ctk.StringVar(value=members[0] if members else "")
        ctk.CTkOptionMenu(form_f, values=members, variable=self.member_var, width=280).pack(pady=5)

        # 2. Select Project
        ctk.CTkLabel(form_f, text="For Project:").pack(anchor="w", padx=20, pady=(10,0))
        self.db.cursor.execute("SELECT id, project_name FROM projects")
        self.project_map = {row['project_name']: row['id'] for row in self.db.cursor.fetchall()}
        self.proj_var = ctk.StringVar(value=list(self.project_map.keys())[0] if self.project_map else "")
        ctk.CTkOptionMenu(form_f, values=list(self.project_map.keys()), variable=self.proj_var, width=280).pack(pady=5)

        # 3. Hours & Date
        ctk.CTkLabel(form_f, text="Hours Required:").pack(anchor="w", padx=20, pady=(10,0))
        self.hours_ent = ctk.CTkEntry(form_f, placeholder_text="e.g. 2.5", width=280)
        self.hours_ent.pack(pady=5)

        ctk.CTkLabel(form_f, text="Date (YYYY-MM-DD):").pack(anchor="w", padx=20, pady=(10,0))
        self.date_ent = ctk.CTkEntry(form_f, width=280)
        self.date_ent.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_ent.pack(pady=5)

        # 4. Instructions/Reason
        ctk.CTkLabel(form_f, text="Instructions:").pack(anchor="w", padx=20, pady=(10,0))
        self.reason_txt = ctk.CTkTextbox(form_f, height=80, width=280)
        self.reason_txt.pack(pady=5)

        ctk.CTkButton(form_f, text="Send OT Request", fg_color="#3498DB", hover_color="#2980B9",
                      command=self.submit_ot_request).pack(pady=20)

    def setup_sent_requests_list(self):
        """List of requests the leader has sent"""
        self.list_f = ctk.CTkScrollableFrame(self.main_f, label_text="Sent Requests Status")
        self.list_f.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.refresh_sent_list()

    def submit_ot_request(self):
        member = self.member_var.get()
        proj_name = self.proj_var.get()
        hours = self.hours_ent.get()
        date = self.date_ent.get()
        reason = self.reason_txt.get("1.0", "end-1c")

        if not hours or not reason:
            messagebox.showwarning("Input Error", "Please fill in hours and instructions.")
            return

        try:
            pid = self.project_map[proj_name]
            sql = "INSERT INTO overtime (member_name, project_id, ot_date, hours, reason, status) VALUES (%s, %s, %s, %s, %s, 'Pending')"
            self.db.cursor.execute(sql, (member, pid, date, hours, reason))
            self.db.conn.commit()
            
            messagebox.showinfo("Sent", f"Overtime request sent to {member}")
            self.refresh_sent_list()
            self.hours_ent.delete(0, 'end')
            self.reason_txt.delete("1.0", "end")
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def refresh_sent_list(self):
        for w in self.list_f.winfo_children(): w.destroy()
        
        query = """
            SELECT o.*, p.project_name 
            FROM overtime o 
            JOIN projects p ON o.project_id = p.id 
            ORDER BY o.created_at DESC
        """
        self.db.cursor.execute(query)
        rows = self.db.cursor.fetchall()

        for r in rows:
            card = ctk.CTkFrame(self.list_f, fg_color=("#F0F0F0", "#252525"), corner_radius=8)
            card.pack(fill="x", pady=4, padx=5)

            # Color coding for status
            status_colors = {"Pending": "#F39C12", "Accepted": "#10B981", "Declined": "#E74C3C"}
            s_color = status_colors.get(r['status'], "gray")

            info = f"👤 {r['member_name']} | 📅 {r['ot_date']} | ⏳ {r['hours']}h\nProject: {r['project_name']}"
            ctk.CTkLabel(card, text=info, justify="left", font=("Arial", 12)).pack(side="left", padx=10, pady=10)
            
            ctk.CTkLabel(card, text=r['status'], text_color=s_color, font=("Arial", 12, "bold")).pack(side="right", padx=15)