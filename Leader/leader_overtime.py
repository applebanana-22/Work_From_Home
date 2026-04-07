import customtkinter as ctk
from database import Database
from tkinter import messagebox
from datetime import datetime

class LeaderOvertime(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user 

        # Main container that will swap between "List View" and "Create Form View"
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_list_view()

    def clear_view(self):
        """Removes all widgets from the container to switch pages"""
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_list_view(self):
        """PAGE 1: The List of OT Requests"""
        self.clear_view()

        # Header
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Team Overtime Status", font=("Arial", 22, "bold")).pack(side="left")

        # ➕ Create Button (Switch to Form Page)
        ctk.CTkButton(header, text="+ Create OT Request", 
                      fg_color="#10B981", hover_color="#059669",
                      command=self.show_create_view).pack(side="right")

        # Scrollable List
        self.list_f = ctk.CTkScrollableFrame(self.container, label_text="Recent Requests")
        self.list_f.pack(fill="both", expand=True, padx=30, pady=10)
        
        self.refresh_sent_list()

    def show_create_view(self):
        """PAGE 2: The OT Registration Form"""
        self.clear_view()

        # --- Top Navigation (Back Button) ---
        nav = ctk.CTkFrame(self.container, fg_color="transparent")
        nav.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkButton(nav, text="← Back to List", width=100, fg_color="#4A4A4A",
                      command=self.show_list_view).pack(side="left")

        # Form Card
        form_card = ctk.CTkFrame(self.container, fg_color=("#EAEAEA", "#2B2B2B"), corner_radius=12)
        form_card.pack(pady=20, padx=30, fill="x")

        inner_f = ctk.CTkFrame(form_card, fg_color="transparent")
        inner_f.pack(pady=30, padx=30)

        # 1. Fetch Data
        leader_team_id = self.user.get('team_id')
        self.db.cursor.execute("SELECT full_name FROM users WHERE team_id = %s AND role = 'member'", (leader_team_id,))
        members = [row['full_name'] for row in self.db.cursor.fetchall()] or ["No members found"]

        self.db.cursor.execute("SELECT id, project_name FROM projects WHERE team_id = %s", (leader_team_id,))
        self.project_map = {row['project_name']: row['id'] for row in self.db.cursor.fetchall()}
        projs = list(self.project_map.keys()) or ["General"]

        # 2. Form UI
        ctk.CTkLabel(inner_f, text="Select Member:").grid(row=0, column=0, padx=10, sticky="w")
        self.member_var = ctk.StringVar(value=members[0])
        ctk.CTkOptionMenu(inner_f, values=members, variable=self.member_var, width=200).grid(row=1, column=0, padx=10, pady=5)

        ctk.CTkLabel(inner_f, text="Project:").grid(row=0, column=1, padx=10, sticky="w")
        self.proj_var = ctk.StringVar(value=projs[0])
        ctk.CTkOptionMenu(inner_f, values=projs, variable=self.proj_var, width=200).grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(inner_f, text="Hours:").grid(row=2, column=0, padx=10, pady=(15,0), sticky="w")
        self.hours_ent = ctk.CTkEntry(inner_f, placeholder_text="e.g. 2.5", width=200)
        self.hours_ent.grid(row=3, column=0, padx=10, pady=5)

        ctk.CTkLabel(inner_f, text="Task Instructions:").grid(row=4, column=0, padx=10, pady=(15,0), sticky="w")
        self.reason_txt = ctk.CTkTextbox(inner_f, height=80, width=420)
        self.reason_txt.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        ctk.CTkButton(inner_f, text="Submit OT Request", fg_color="#3498DB", height=40,
                      command=self.submit_ot_request).grid(row=6, column=0, columnspan=2, pady=20)

    def submit_ot_request(self):
        """Handles Database Insert and returns to List View"""
        member = self.member_var.get()
        proj_name = self.proj_var.get()
        hours = self.hours_ent.get()
        date = datetime.now().strftime("%Y-%m-%d")
        reason = self.reason_txt.get("1.0", "end-1c")

        if not hours or not reason or member == "No members found":
            messagebox.showwarning("Error", "Fill all fields!")
            return

        try:
            pid = self.project_map.get(proj_name)
            sql = "INSERT INTO overtime (member_name, project_id, ot_date, hours, reason, status) VALUES (%s, %s, %s, %s, %s, 'Pending')"
            self.db.cursor.execute(sql, (member, pid, date, hours, reason))
            self.db.conn.commit()
            
            messagebox.showinfo("Success", "Request Sent!")
            self.show_list_view() # Auto-switch back to the list
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_sent_list(self):
        """Displays the team's OT history"""
        for w in self.list_f.winfo_children(): w.destroy()
        
        leader_team_id = self.user.get('team_id')
        query = """
            SELECT o.*, p.project_name FROM overtime o 
            JOIN projects p ON o.project_id = p.id 
            JOIN users u ON o.member_name = u.full_name
            WHERE u.team_id = %s ORDER BY o.id DESC
        """
        self.db.cursor.execute(query, (leader_team_id,))
        for r in self.db.cursor.fetchall():
            card = ctk.CTkFrame(self.list_f, fg_color=("#F0F0F0", "#252525"), corner_radius=8)
            card.pack(fill="x", pady=5, padx=10)

            status_colors = {"Pending": "#F39C12", "Accepted": "#27AE60", "Rejected": "#E74C3C", "Approved": "#2980B9"}
            
            info = f"👤 {r['member_name']} | 📅 {r['ot_date']} | ⏳ {r['hours']}h\nProject: {r['project_name']}"
            ctk.CTkLabel(card, text=info, justify="left").pack(side="left", padx=15, pady=10)
            ctk.CTkLabel(card, text=r['status'], text_color=status_colors.get(r['status'], "gray"), 
                         font=("Arial", 12, "bold")).pack(side="right", padx=15)