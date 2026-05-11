import customtkinter as ctk
from tkinter import messagebox
from database import Database
import re


class AdminTeams(ctk.CTkFrame):

    def __init__(self, master, user, **kwargs):
        super().__init__(
            master,
            fg_color=("#F3F4F6", "#121212"),
            **kwargs
        )

        self.user = user
        self.db = Database()

        # ================= STATE =================

        self.form_visible = False
        self.edit_mode = False
        self.edit_team_id = None

        # ================= SAME BG COLOR =================

        self.section_bg = ("#E5E7EB", "#1E1E1E")

        # ================= HEADER =================

        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.header_frame.pack(
            fill="x",
            padx=80,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            self.header_frame,
            text="🛡️ Team Management",
            font=("Arial", 24, "bold"),
            text_color=("black", "white")
        ).pack(side="left")

        self.add_btn = ctk.CTkButton(
            self.header_frame,
            text="+ Create Team",
            fg_color="#10B981",
            hover_color="#0E9A6B",
            command=self.toggle_form
        )

        self.add_btn.pack(side="right")

        # ================= FORM FRAME =================

        self.form_frame = ctk.CTkFrame(
            self,

            # SAME COLOR
            fg_color=self.section_bg,

            corner_radius=12,

            border_width=1,

            border_color=("#D1D5DB", "#3A3A3A")
        )

        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="Create New Team",
            font=("Arial", 16, "bold"),
            text_color=("black", "white")
        )

        self.form_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        # ================= ENTRY =================

        self.team_name_entry = ctk.CTkEntry(
            self.form_frame,

            placeholder_text="Enter team name...",

            height=40,

            fg_color=("white", "#2B2B2B"),

            text_color=("black", "white"),

            border_color=("#D1D5DB", "#444")
        )

        self.team_name_entry.pack(
            fill="x",
            padx=15,
            pady=5
        )

        # ================= BUTTON ROW =================

        self.form_btn_row = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )

        self.form_btn_row.pack(
            fill="x",
            padx=15,
            pady=(5, 15)
        )

        # CANCEL

        self.cancel_btn = ctk.CTkButton(
            self.form_btn_row,
            text="Cancel",
            fg_color="gray40",
            hover_color="gray60",
            command=self.reset_form
        )

        self.cancel_btn.pack(side="left")

        # SAVE

        self.save_team_btn = ctk.CTkButton(
            self.form_btn_row,
            text="Create Team",
            fg_color="#10B981",
            hover_color="#0E9A6B",
            command=self.save_team
        )

        self.save_team_btn.pack(side="right")

        # ================= TABLE CONTAINER =================

        self.table_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.table_container.pack(
            fill="both",
            expand=True,
            padx=80,
            pady=20
        )

        # ================= SCROLLABLE TEAM LIST =================

        self.table_frame = ctk.CTkScrollableFrame(
            self.table_container,

            label_text="Active Teams",

            # SAME COLOR
            fg_color=self.section_bg,

            label_fg_color=("#D1D5DB", "#2B2B2B"),

            label_text_color=("black", "white"),

            corner_radius=12
        )

        self.table_frame.pack(
            fill="both",
            expand=True
        )

        self.load_teams()

    # =========================================================
    # TOGGLE FORM
    # =========================================================

    def toggle_form(self):

        if self.form_visible:
            self.reset_form()
            return

        self.form_frame.pack(
            after=self.header_frame,
            fill="x",
            padx=80,
            pady=20
        )

        self.form_visible = True

    # =========================================================
    # RESET FORM
    # =========================================================

    def reset_form(self):

        self.form_frame.pack_forget()

        self.team_name_entry.delete(0, "end")

        self.edit_mode = False
        self.edit_team_id = None
        self.form_visible = False

    # =========================================================
    # SAVE TEAM
    # =========================================================

    def save_team(self):

        team_name = self.team_name_entry.get().strip()

        pattern = r"^[A-Z](?=.*\d).{3,}$"

        if not team_name:
            messagebox.showwarning(
                "Input Error",
                "Team name cannot be empty."
            )
            return

        if not re.match(pattern, team_name):

            messagebox.showwarning(
                "Format Error",
                "Must start with Capital, 4+ chars, include number (e.g., Team1)"
            )

            return

        try:

            # UPDATE

            if self.edit_mode:

                if self.db.update_team(
                    self.edit_team_id,
                    team_name
                ):

                    messagebox.showinfo(
                        "Success",
                        "Team updated!"
                    )

            # CREATE

            else:

                if self.db.create_team(team_name):

                    messagebox.showinfo(
                        "Success",
                        f"Team '{team_name}' created!"
                    )

                else:

                    messagebox.showerror(
                        "Error",
                        "Team already exists."
                    )

            self.reset_form()
            self.load_teams()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =========================================================
    # LOAD TEAMS
    # =========================================================

    def load_teams(self):

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        teams = self.db.get_all_teams()

        if not teams:

            ctk.CTkLabel(
                self.table_frame,

                text="🚫 No teams yet\nClick 'Create Team' to start",

                font=("Arial", 13),

                text_color=("gray40", "gray70"),

                justify="center"
            ).pack(pady=30)

            return

        # ================= TEAM ROWS =================

        for team in teams:

            tid = team['team_id']
            tname = team['team_name']

            # ROW

            row = ctk.CTkFrame(
                self.table_frame,

                fg_color=("#F3F4F6", "#2B2B2B"),

                corner_radius=10,

                border_width=1,

                border_color=("#D1D5DB", "#444")
            )

            row.pack(
                fill="x",
                pady=8,
                padx=10
            )

            # INFO

            info_frame = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            info_frame.pack(
                side="left",
                fill="both",
                expand=True,
                padx=15,
                pady=12
            )

            ctk.CTkLabel(
                info_frame,

                text=f"👥 {tname}",

                font=("Arial", 14, "bold"),

                text_color=("black", "white"),

                anchor="w"
            ).pack(anchor="w")

            # BUTTON AREA

            btn_frame = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            btn_frame.pack(
                side="right",
                padx=10
            )

            # DELETE BUTTON

            ctk.CTkButton(
                btn_frame,

                text="Delete",

                width=70,
                height=30,

                fg_color="#E74C3C",

                hover_color="#C0392B",

                command=lambda t_id=tid:
                self.delete_team(t_id)

            ).pack(
                side="right",
                padx=3
            )

            # EDIT BUTTON

            ctk.CTkButton(
                btn_frame,

                text="Edit",

                width=70,
                height=30,

                fg_color="#F39C12",

                hover_color="#D68910",

                command=lambda t_id=tid, t_name=tname:
                self.load_edit_form(t_id, t_name)

            ).pack(
                side="right",
                padx=3
            )

    # =========================================================
    # LOAD EDIT FORM
    # =========================================================

    def load_edit_form(self, team_id, team_name):

        if not self.form_visible:
            self.toggle_form()

        self.edit_mode = True
        self.edit_team_id = team_id

        self.form_title.configure(
            text="Edit Team"
        )

        self.save_team_btn.configure(
            text="Update Team",
            fg_color="#3498DB",
            hover_color="#2980B9"
        )

        self.team_name_entry.delete(0, "end")
        self.team_name_entry.insert(0, team_name)

    # =========================================================
    # DELETE TEAM
    # =========================================================

    def delete_team(self, team_id):

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure?\nUsers in this team will be set to 'No Team'."
        )

        if not confirm:
            return

        try:

            if self.db.delete_team(team_id):

                messagebox.showinfo(
                    "Success",
                    "Team deleted successfully."
                )

                self.load_teams()

            else:

                messagebox.showerror(
                    "Error",
                    "Delete failed."
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )