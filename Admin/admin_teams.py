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
            text="Team Management",
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
            fg_color=self.section_bg,
            corner_radius=12,
            border_width=1,
            border_color=("#D1D5DB", "#3A3A3A")
        )

        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text=" New Team Creation Form ",
            font=("Arial", 16, "bold"),
            text_color=("black", "white")
        )

        self.form_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        # ================= TEAM NAME LABEL =================

        team_name_label_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )

        team_name_label_frame.pack(
            anchor="w",
            padx=15,
            pady=(10, 2)
        )

        ctk.CTkLabel(
            team_name_label_frame,
            text="Team Name",
            font=("Arial", 13, "bold"),
            text_color=("black", "white")
        ).pack(side="left")

        ctk.CTkLabel(
            team_name_label_frame,
            text=" *",
            font=("Arial", 20, "bold"),
            text_color="#EF4444"
        ).pack(side="left")

        # ================= TEAM NAME =================

        self.team_name_entry = ctk.CTkEntry(
            self.form_frame,
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
        
        # ================= INLINE ERROR LABEL =================

        self.team_error_label = ctk.CTkLabel(
            self.form_frame,
            text="",
            text_color="#EF4444",
            font=("Arial", 12)
        )

        self.team_error_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 5)
        )

        # ================= DESCRIPTION LABEL =================

        desc_label_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )

        desc_label_frame.pack(
            anchor="w",
            padx=15,
            pady=(10, 2)
        )

        ctk.CTkLabel(
            desc_label_frame,
            text="Team Description",
            font=("Arial", 13, "bold"),
            text_color=("black", "white")
        ).pack(side="left")

        ctk.CTkLabel(
            desc_label_frame,
            text=" *",
            font=("Arial", 20, "bold"),
            text_color="#EF4444"
        ).pack(side="left")

        # ================= DESCRIPTION =================

        self.team_desc_entry = ctk.CTkTextbox(
            self.form_frame,
            height=40,
            fg_color=("white", "#2B2B2B"),
            text_color=("black", "white"),
            border_color=("#D1D5DB", "#444"),
            border_width=1
        )

        self.team_desc_entry.pack(
            fill="x",
            padx=15,
            pady=5
        )
        
        
        
        # ================= DESCRIPTION ERROR LABEL =================

        self.desc_error_label = ctk.CTkLabel(
            self.form_frame,
            text="",
            text_color="#EF4444",
            font=("Arial", 12)
        )

        self.desc_error_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 5)
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

        # CANCEL BUTTON

        self.cancel_btn = ctk.CTkButton(
            self.form_btn_row,
            text="Clear",
            fg_color="gray40",
            hover_color="gray60",
            command=self.clear_form
        )

        self.cancel_btn.pack(side="left")

        # SAVE BUTTON

        self.save_team_btn = ctk.CTkButton(
            self.form_btn_row,
            text="Submit",
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

        # ================= TEAM LIST =================

        self.table_frame = ctk.CTkScrollableFrame(
            self.table_container,
            label_text="Active Teams",
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

        self.team_name_entry.delete(0, "end")
        

        self.team_desc_entry.delete("1.0", "end")

        self.team_desc_entry.configure(
            text_color=("black", "white")
        )

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

        # Clear inputs
        self.team_name_entry.delete(0, "end")
        self.team_desc_entry.delete("1.0", "end")

        # Reset border colors
        self.team_name_entry.configure(
            border_color=("#D1D5DB", "#444")
        )

        self.team_desc_entry.configure(
            border_color=("#D1D5DB", "#444"),
            text_color=("black", "white")
        )

        # Clear error labels
        self.team_error_label.configure(text="")
        self.desc_error_label.configure(text="")

        # Reset state
        self.edit_mode = False
        self.edit_team_id = None
        self.form_visible = False

        # Reset title/button
        self.form_title.configure(
            text="Create New Team"
        )

        self.save_team_btn.configure(
            text="Submit",
            fg_color="#10B981",
            hover_color="#0E9A6B"
        )

        self.focus()

    # =========================================================
    # SAVE TEAM
    # =========================================================

    def save_team(self):
        team_name = self.team_name_entry.get().strip()
        team_desc = self.team_desc_entry.get("1.0", "end").strip()
        pattern = r"^[A-Z](?=.*\d).{3,}$"

        # 1. Reset all previous validation visuals first
        self.team_name_entry.configure(border_color=("#D1D5DB", "#444"))
        self.team_error_label.configure(text="")
        self.team_desc_entry.configure(border_color=("#D1D5DB", "#444"))
        self.desc_error_label.configure(text="")

        # 2. Track if any validation fails
        has_errors = False

        # --- Team Name Validation ---
        if not team_name:
            self.team_name_entry.configure(border_color="#EF4444")
            self.team_error_label.configure(text="Team name is required.")
            has_errors = True
        elif not re.match(pattern, team_name):
            self.team_name_entry.configure(border_color="#EF4444")
            self.team_error_label.configure(text="Must start with Capital, 4+ chars, include number.")
            has_errors = True

        # --- Team Description Validation ---
        if not team_desc:
            self.team_desc_entry.configure(border_color="#EF4444")
            self.desc_error_label.configure(text="Description is required.")
            has_errors = True

        # 3. STOP execution here if any text input validations failed
        if has_errors:
            return

        try:
            # --- Database Uniqueness Check ---
            existing_teams = self.db.get_all_teams()
            
            # UPDATE TEAM UNIQUE CHECK
            if self.edit_mode:
                for team in existing_teams:
                    if (
                        team['team_name'].lower() == team_name.lower()
                        and team['team_id'] != self.edit_team_id
                    ):
                        self.team_name_entry.configure(border_color="#EF4444")
                        self.show_error_toast("Team name already exists.")
                        return

                updated = self.db.update_team(
                    self.edit_team_id,
                    team_name,
                    team_desc
                )
                if updated:
                    self.show_success_toast(f"{team_name} updated successfully!")

            # CREATE TEAM UNIQUE CHECK
            else:
                for team in existing_teams:
                    if team['team_name'].lower() == team_name.lower():
                        self.team_name_entry.configure(border_color="#EF4444")
                        self.show_error_toast("Team name already exists.")
                        return

                if self.db.create_team(team_name, team_desc):
                    self.show_success_toast(f"{team_name} created successfully!")

            self.reset_form()
            self.load_teams()

        except Exception as e:
            self.show_error_toast("Error", str(e))

    def _show_message(self, message, message_type="info", duration=3000):
        if message_type == "error":
            bg_color = "#E74C3C"
        elif message_type == "warning":
            bg_color = "#F39C12"
        elif message_type == "success":
            bg_color = "#27AE60"
        else:
            bg_color = "#3498DB"

        message_frame = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color=bg_color,
            corner_radius=8
        )
        message_frame.place(relx=1.0, rely=0, x=-20, y=20, anchor="ne")

        ctk.CTkLabel(
            message_frame,
            text=message,
            text_color="white",
            font=("Arial", 12, "bold"),
            wraplength=250
        ).pack(padx=15, pady=10)

        self.after(duration, message_frame.destroy)

    def show_error_toast(self, title_or_message, message=None):
        text = title_or_message if message is None else f"{title_or_message}: {message}"
        self._show_message(text, message_type="error")

    def show_success_toast(self, title_or_message, message=None):
        text = title_or_message if message is None else f"{title_or_message}: {message}"
        self._show_message(text, message_type="success")
    
    
    
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
            desc = team['description']

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

            ctk.CTkLabel(
                info_frame,
                text=desc if desc else "No description",
                font=("Arial", 12),
                text_color=("gray30", "gray70"),
                wraplength=700,
                justify="left",
                anchor="w"
            ).pack(anchor="w", pady=(3, 0))

            # BUTTON FRAME

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
                command=lambda t_id=tid, t_name=tname, t_desc=desc:
                self.load_edit_form(t_id, t_name, t_desc)

            ).pack(
                side="right",
                padx=3
            )
    # =========================================================
    # CLEAR FORM
    # =========================================================

    def clear_form(self):

        self.team_name_entry.delete(0, "end")

        self.team_desc_entry.delete("1.0", "end")


        self.team_desc_entry.configure(
            text_color=("black", "white")
        )

        self.focus()

    # =========================================================
    # LOAD EDIT FORM
    # =========================================================

    def load_edit_form(self, team_id, team_name, team_desc):

        if not self.form_visible:
            self.toggle_form()

        self.edit_mode = True
        self.edit_team_id = team_id

        self.form_title.configure(
            text="Edit Team"
        )

        self.save_team_btn.configure(
            text="Submit",
            fg_color="#10B981",
            hover_color="#0E9A6B",
        )

        self.team_name_entry.delete(0, "end")
        self.team_name_entry.insert(0, team_name)

        self.team_desc_entry.delete("1.0", "end")

        self.team_desc_entry.insert(
            "1.0",
            team_desc if team_desc else ""
        )

        self.team_desc_entry.configure(
            text_color=("black", "white")
        )

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
            # fetch name before deleting so we can include it in the toast
            team_name = self.db.get_team_name(team_id)

            if self.db.delete_team(team_id):
                msg = f"{team_name} deleted successfully."
                self.show_success_toast(msg)

                self.load_teams()

            else:
                self.show_error_toast(
                    "Delete failed."
                )

        except Exception as e:
            self.show_error_toast("Error", str(e))