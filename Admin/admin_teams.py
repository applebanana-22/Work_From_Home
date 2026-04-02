import customtkinter as ctk
from tkinter import messagebox
from database import Database

class AdminTeams(ctk.CTkFrame):
    def __init__(self, master, user, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.user = user
        self.db = Database() 
        
        # --- Header ---
        self.header = ctk.CTkLabel(
            self, text="🛡️ Team Management", 
            font=("Arial", 24, "bold"), 
            text_color=("#2C3E50", "#FFFFFF")
        )
        self.header.pack(pady=(20, 10), padx=30, anchor="w")

        # --- CRUD Action Bar ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=30, pady=10)

        self.add_btn = ctk.CTkButton(
            self.action_frame, text="+ Create Team", 
            command=self.open_create_modal,
            fg_color="#2ECC71", hover_color="#27AE60", text_color="white",
            width=140, font=("Arial", 13, "bold")
        )
        self.add_btn.pack(side="left", padx=(0, 10))

        self.refresh_btn = ctk.CTkButton(
            self.action_frame, text="🔄 Refresh List", 
            command=self.load_teams,
            fg_color=("#E0E0E0", "#333333"),
            text_color=("#333333", "#FFFFFF"),
            hover_color=("#D0D0D0", "#444444"),
            width=120
        )
        self.refresh_btn.pack(side="left")

        # --- Team List Table ---
        self.table_frame = ctk.CTkScrollableFrame(
            self, label_text="Active Teams",
            label_text_color=("#555555", "#AAAAAA"),
            fg_color=("#FFFFFF", "#181818"),
            border_width=1, border_color=("#E0E0E0", "#2B2B2B")
        )
        self.table_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.load_teams()

    def load_teams(self):
        """Fetch and display real data from MySQL without showing IDs"""
        # 1. Clear existing rows
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # 2. Get data from database
        teams = self.db.get_all_teams()
        
        if not teams:
            ctk.CTkLabel(self.table_frame, text="No teams found.", font=("Arial", 12, "italic")).pack(pady=20)
            return

        for team in teams:
            # We still need tid for the buttons to work!
            tid = team['team_id']
            tname = team['team_name']

            row = ctk.CTkFrame(self.table_frame, fg_color=("#F8F9FA", "#2B2B2B"), corner_radius=6)
            row.pack(fill="x", pady=4, padx=5)
            
            # --- DISPLAY: Only show the Team Name ---
            ctk.CTkLabel(
                row, 
                text=f"👥  {tname}", # Added a small icon for style
                font=("Arial", 13, "bold"),
                text_color=("#2C3E50", "#D1D1D1")
            ).pack(side="left", padx=15, pady=8)
            
            # --- LOGIC: Buttons still use tid behind the scenes ---
            # Delete Button
            ctk.CTkButton(
                row, text="🗑️", width=35, height=30, 
                fg_color="#E74C3C", hover_color="#C0392B",
                command=lambda t_id=tid: self.delete_team(t_id)
            ).pack(side="right", padx=5)

            # Edit Button
            ctk.CTkButton(
                row, text="✏️", width=35, height=30, 
                fg_color="#3498DB", hover_color="#2980B9",
                command=lambda t_id=tid, t_name=tname: self.open_edit_modal(t_id, t_name)
            ).pack(side="right", padx=5)

    def open_create_modal(self):
        dialog = ctk.CTkInputDialog(text="Enter New Team Name:", title="Create Team")
        team_name = dialog.get_input()
        if team_name and team_name.strip():
            if self.db.create_team(team_name.strip()):
                messagebox.showinfo("Success", f"Team '{team_name}' created!")
                self.load_teams()
            else:
                messagebox.showerror("Error", "Could not create team. Name might exist.")

    def open_edit_modal(self, team_id, current_name):
        dialog = ctk.CTkInputDialog(text=f"Rename '{current_name}' to:", title="Edit Team")
        new_name = dialog.get_input()
        if new_name and new_name.strip():
            if self.db.update_team(team_id, new_name.strip()):
                self.load_teams()
            else:
                messagebox.showerror("Error", "Update failed.")

    def delete_team(self, team_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure? Users in this team will be set to 'No Team'."):
            if self.db.delete_team(team_id):
                self.load_teams()