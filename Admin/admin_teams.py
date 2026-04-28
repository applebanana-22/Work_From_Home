import customtkinter as ctk
from tkinter import messagebox
from database import Database
import re


class AdminTeams(ctk.CTkFrame):
    def __init__(self, master, user, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.user = user
        self.db = Database()

        # STATE
        self.form_visible = False
        self.edit_mode = False
        self.edit_team_id = None

        # ================= HEADER =================
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=100, pady=(20, 10))

        ctk.CTkLabel(
            self.header_frame,
            text="🛡️ Team Management",
            font=("Arial", 24, "bold")
        ).pack(side="left")

        self.add_btn = ctk.CTkButton(
            self.header_frame,
            text="+ Create Team",
            fg_color="#2ECC71",
            command=self.toggle_form
        )
        self.add_btn.pack(side="right")

        # ================= FORM =================
        self.form_frame = ctk.CTkFrame(
            self,
            corner_radius=12,
            border_width=1,
            border_color="gray30"
        )

        # Dynamic title
        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="Create New Team",
            font=("Arial", 16, "bold")
        )
        self.form_title.pack(anchor="w", padx=15, pady=(12, 5))

        self.team_name_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Enter team name...",
            height=40
        )
        self.team_name_entry.pack(fill="x", padx=15, pady=5)

        self.form_btn_row = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.form_btn_row.pack(fill="x", padx=15, pady=(5, 15))

        self.cancel_btn = ctk.CTkButton(
            self.form_btn_row,
            text="Cancel",
            fg_color="gray40",
            command=self.reset_form
        )
        self.cancel_btn.pack(side="left")

        self.save_team_btn = ctk.CTkButton(
            self.form_btn_row,
            text="Create Team",
            fg_color="#2ECC71",
            command=self.save_team   # ✅ FIXED
        )
        self.save_team_btn.pack(side="right")

        # ================= TEAM LIST =================
        self.table_container = ctk.CTkFrame(self, fg_color="transparent")
        self.table_container.pack(fill="both", expand=True, padx=100, pady=20)

        self.table_frame = ctk.CTkScrollableFrame(
            self.table_container,
            label_text="Active Teams"
        )
        self.table_frame.pack(fill="both", expand=True)

        self.load_teams()

    # ================= UI CONTROL =================

    def toggle_form(self):
        if not self.form_visible:
            self.form_frame.pack(
                after=self.header_frame,
                fill="x",
                padx=100,
                pady=20
            )
            self.add_btn.configure(text="Cancel", fg_color="#E74C3C")
            self.form_visible = True
        else:
            self.reset_form()

    def reset_form(self):
        self.form_frame.pack_forget()
        self.team_name_entry.delete(0, "end")

        # reset edit state
        self.edit_mode = False
        self.edit_team_id = None

        # reset UI
        self.form_title.configure(text="Create New Team")
        self.save_team_btn.configure(text="Create Team", fg_color="#2ECC71")

        self.add_btn.configure(text="+ Create Team", fg_color="#2ECC71")
        self.form_visible = False

    # ================= SAVE (CREATE + UPDATE) =================

    def save_team(self):
        team_name = self.team_name_entry.get().strip()
        pattern = r"^[A-Z](?=.*\d).{3,}$"

        if not team_name:
            messagebox.showwarning("Input Error", "Team name cannot be empty.")
            return

        if not re.match(pattern, team_name):
            messagebox.showwarning(
                "Format Error",
                "Must start with Capital, 4+ chars, include number (e.g., Team1)"
            )
            return

        try:
            if self.edit_mode:
                # UPDATE
                if self.db.update_team(self.edit_team_id, team_name):
                    messagebox.showinfo("Success", "Team updated!")
            else:
                # CREATE
                if self.db.create_team(team_name):
                    messagebox.showinfo("Success", f"Team '{team_name}' created!")
                else:
                    messagebox.showerror("Error", "Team already exists.")

            self.reset_form()
            self.load_teams()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= LOAD =================

    def load_teams(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        teams = self.db.get_all_teams()

        if not teams:
            ctk.CTkLabel(
                self.table_frame,
                text="🚫 No teams yet\nClick 'Create Team' to start",
                font=("Arial", 13),
                text_color="gray60",
                justify="center"
            ).pack(pady=30)
            return

        for team in teams:
            tid = team['team_id']
            tname = team['team_name']

            row = ctk.CTkFrame(self.table_frame, corner_radius=8)
            row.pack(fill="x", pady=10, padx=10)

            info_frame = ctk.CTkFrame(row, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=12)

            ctk.CTkLabel(
                info_frame,
                text=f"👥 {tname}",
                font=("Arial", 14, "bold"),
                anchor="w"
            ).pack(anchor="w")

            btn_frame = ctk.CTkFrame(row, fg_color="transparent")
            btn_frame.pack(side="right", padx=10)

            # DELETE
            ctk.CTkButton(
                btn_frame,
                text="Delete",
                width=70, height=28,
                fg_color="#E74C3C",
                command=lambda t_id=tid: self.delete_team(t_id)
            ).pack(side="right", padx=3)

            # EDIT (FIXED)
            ctk.CTkButton(
                btn_frame,
                text="Edit",
                width=70, height=28,
                fg_color="#3498DB",
                command=lambda t_id=tid, t_name=tname: self.load_edit_form(t_id, t_name)
            ).pack(side="right", padx=3)

    # ================= LOAD EDIT INTO FORM =================

    def load_edit_form(self, team_id, team_name):
        if not self.form_visible:
            self.toggle_form()

        self.edit_mode = True
        self.edit_team_id = team_id

        self.form_title.configure(text="Edit Team")
        self.save_team_btn.configure(text="Update Team", fg_color="#3498DB")

        self.team_name_entry.delete(0, "end")
        self.team_name_entry.insert(0, team_name)

    # ================= DELETE =================

    def delete_team(self, team_id):
        if messagebox.askyesno(
            "Confirm Delete",
            "Are you sure?\nUsers in this team will be set to 'No Team'."
        ):
            try:
                if self.db.delete_team(team_id):
                    self.load_teams()
                else:
                    messagebox.showerror("Error", "Delete failed.")
            except Exception as e:
                messagebox.showerror("Error", str(e))