import customtkinter as ctk
from database import Database

class LeaderProject(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user

        # ------------- State Declaration -------------
        self.form_visible = False
        self.mode = "add"
        self.editing_task_id = None

        # --- Header Section ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=80, pady=(20, 10))
        
        ctk.CTkLabel(self.header, text="Project Hub", 
                     font=("Arial", 26, "bold"),
                     text_color=("#1A1A1A", "#FFFFFF")).pack(side="left")

        # ---------------- Toggle Button ----------------
        self.add_btn = ctk.CTkButton(
            self.header,
            text="+ New Project",
            fg_color="#10B981",
            width=140, height=36,
            text_color=("#2D3436", "#ECF0F1"),
            hover_color="#059669",
            font=("Arial", 13, "bold"),
            command=self.toggle_form
        )
        self.add_btn.pack(side="right")

        # =========================================================
        # CONTROL WRAPPER (FORM CONTAINER - DYNAMIC PACKING)
        # =========================================================
        self.control_wrapper = ctk.CTkFrame(self, fg_color="transparent")

        # =========================================================
        # FORM UI (PERFECTLY ALIGNED INLINE STYLE)
        # =========================================================
        self.control_f = ctk.CTkFrame(self.control_wrapper, fg_color=("#EAEAEA", "#1E1E1E"), corner_radius=12)
        self.control_f.pack(fill="x", pady=(5, 10))

        form_row = ctk.CTkFrame(self.control_f, fg_color="transparent")
        form_row.pack(fill="x", padx=20, pady=(20, 10))

        # --- Element 1: Label ---
        self.lbl_text = ctk.CTkLabel(form_row, text="Project Name", font=("Arial", 13, "bold"))
        self.lbl_text.pack(side="left", anchor="center")
        
        self.lbl_star = ctk.CTkLabel(form_row, text=" *", text_color="red", font=("Arial", 14, "bold"))
        self.lbl_star.pack(side="left", padx=(0, 15), anchor="center")

        # --- Element 2: Entry Textbox ---
        self.task_entry = ctk.CTkEntry(form_row, placeholder_text="Enter project name...", width=200, height=34)
        self.task_entry.pack(side="left", fill="x", padx=(0, 15), anchor="center")

        # --- Element 3: Action Button ---
        self.action_btn = ctk.CTkButton(
            form_row,
            text="Create Project",
            fg_color="#10B981",
            hover_color="#059669",
            width=60, 
            height=30,
            font=("Arial", 12, "bold"),
            text_color=("#2D3436", "#ECF0F1"),
            command=self.open_create_project
        )
        self.action_btn.pack(side="left", anchor="center")

        # --- Error Label (Placed strictly below the row) ---
        error_row = ctk.CTkFrame(self.control_f, fg_color="transparent")
        error_row.pack(fill="x", padx=20, pady=(0, 15))
        
        self.task_error = ctk.CTkLabel(error_row, text="", text_color="red", font=("Arial", 11))
        self.task_error.pack(anchor="w", padx=(105, 0)) 

        # --- Project List Area ---
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Ongoing Projects", 
                                                 fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=80, pady=(10, 20))

        self.refresh_projects()

    # --- Toast Message Box Logic ---
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
        # Adjusted y coordinate to 20 so it doesn't cover top navigation elements
        message_frame.place(relx=1.0, rely=0, x=-20, y=20, anchor="ne")
         
        ctk.CTkLabel(
            message_frame,
            text=message,
            text_color="white",
            font=("Arial", 12, "bold"),
            wraplength=250
        ).pack(padx=15, pady=10)
         
        self.after(duration, message_frame.destroy)

    def toggle_form(self):
        if self.form_visible:
            self.reset_form()
            self.control_wrapper.pack_forget()
            self.form_visible = False
            self.add_btn.configure(text="+ New Project", fg_color="#10B981", hover_color="#059669")
        else:
            self.list_frame.pack_forget()
            self.control_wrapper.pack(fill="x", padx=80)
            self.list_frame.pack(fill="both", expand=True, padx=80, pady=(10, 20))
            
            self.form_visible = True
            self.add_btn.configure(text="✖ Close", fg_color="#E74C3C", hover_color="#C0392B")
            self.set_mode("add")

    def reset_form(self):
        self.mode = "add"
        self.editing_task_id = None
        self.task_error.configure(text="")
        self.task_entry.delete(0, "end")

    def set_mode(self, mode, task_id=None):
        self.mode = mode
        self.editing_task_id = task_id

        if mode == "add":
            self.action_btn.configure(
                text="Create Project",
                fg_color="#10B981",
                hover_color="#059669",
                command=self.open_create_project
            )
        elif mode == "edit":
            self.action_btn.configure(
                text="Update",
                fg_color="#F39C12",
                hover_color="#D68910",
                command=lambda: self.update_project(self.editing_task_id)
            )

    def start_edit_task(self, row):
        self.task_error.configure(text="")

        if not self.form_visible:
            self.list_frame.pack_forget()
            self.control_wrapper.pack(fill="x", padx=80)
            self.list_frame.pack(fill="both", expand=True, padx=80, pady=(10, 20))
            
            self.form_visible = True
            self.add_btn.configure(text="✖ Close", fg_color="#E74C3C", hover_color="#C0392B")

        self.set_mode("edit", row["id"])
        self.task_entry.delete(0, "end")
        self.task_entry.insert(0, row["project_name"])

    def open_task_manager(self, proj):
        for w in self.master.winfo_children():
            w.destroy()

        from Leader.task_manager import TaskManager

        TaskManager(
            self.master,
            proj['id'],
            proj['project_name'],
            self.user,
            back_callback=self.back_to_projects
        ).pack(fill="both", expand=True)

    def back_to_projects(self):
        for w in self.master.winfo_children():
            w.destroy()

        LeaderProject(self.master, self.user).pack(fill="both", expand=True)

    def refresh_projects(self):
        """Clears and re-populates the project list filtered by the leader's team_id"""
        for w in self.list_frame.winfo_children(): 
            w.destroy()
        
        try:
            sql = "SELECT * FROM projects WHERE team_id = %s ORDER BY id DESC"
            self.db.cursor.execute(sql, (self.user['team_id'],))
            projects = self.db.cursor.fetchall()
            
            if not projects:
                ctk.CTkLabel(self.list_frame, text="No projects found for your team.", 
                             text_color="gray", font=("Arial", 14)).pack(pady=40)
                return

            for proj in projects:
                card = ctk.CTkFrame(self.list_frame, corner_radius=12, border_width=1, 
                                    fg_color=("#FFFFFF", "#1E1E1E"), 
                                    border_color=("#E0E0E0", "#333333"))
                card.pack(fill="x", pady=6, padx=10)
                
                info_f = ctk.CTkFrame(card, fg_color="transparent")
                info_f.pack(side="left", padx=20, pady=12)
                
                ctk.CTkLabel(info_f, text=proj['project_name'], font=("Arial", 16, "bold"),
                             text_color=("#2D3436", "#ECF0F1")).pack(anchor="w")

                is_complete = 1 if "100" in proj['status'] or "Pending" in proj['status'] else 0
                status_color = "#F1C40F" if "Pending" in proj['status'] else "#2ECC71"
                
                ctk.CTkLabel(info_f, text=f"● {proj['status']}", font=("Arial", 12),
                             text_color=status_color).pack(anchor="w")

                btn_f = ctk.CTkFrame(card, fg_color="transparent")
                btn_f.pack(side="right", padx=20)
                
                ctk.CTkButton(
                    btn_f, 
                    text="Manage", 
                    width=80, 
                    height=32, 
                    fg_color="#3498DB", 
                    text_color=("#2D3436", "#ECF0F1"),
                    command=lambda p=proj: self.open_task_manager(p)
                ).pack(side="left", padx=5)

                ctk.CTkButton(
                    btn_f, 
                    text="Edit", 
                    state="disabled" if is_complete else "normal",
                    width=60, 
                    height=32, 
                    fg_color="#F39C12" if not is_complete else "grey",
                    text_color=("#2D3436", "#ECF0F1"),
                    hover_color="#D35400",
                    command=lambda p=proj: self.start_edit_task(p)
                ).pack(side="left", padx=5)

                ctk.CTkButton(
                    btn_f, 
                    text="Delete", 
                    state="disabled" if not is_complete else "normal",
                    width=60, 
                    height=32, 
                    fg_color="#E74C3C" if is_complete else "grey",
                    text_color=("#2D3436", "#ECF0F1"),
                    command=lambda pid=proj['id']: self.delete_project(pid)
                ).pack(side="left", padx=5)
                
        except Exception as e:
            self._show_message(f"Database Error: {e}", "error")

    def open_create_project(self):
        self.task_error.configure(text="")
        project_name = self.task_entry.get().strip()

        if not project_name:
            self.task_error.configure(text="Project name is required.")
            return

        try:
            sql = "INSERT INTO projects (project_name, created_by, team_id, status) VALUES (%s, %s, %s, %s)"
            self.db.cursor.execute(sql, (
                project_name, 
                self.user['full_name'], 
                self.user['team_id'], 
                'Pending'
            ))
            self.db.conn.commit()
            self.refresh_projects()
            self.toggle_form()  
            self._show_message("Project created successfully!", "success")
        except Exception as e:
            self._show_message(str(e), "error")

    def update_project(self, pid):
        self.task_error.configure(text="")
        new_name = self.task_entry.get().strip()

        if not new_name:
            self.task_error.configure(text="Project name cannot be empty.")
            return

        try:
            sql = "UPDATE projects SET project_name = %s WHERE id = %s"
            self.db.cursor.execute(sql, (new_name, pid))
            self.db.conn.commit()
            self.refresh_projects()
            self.toggle_form()
            self._show_message("Project updated successfully!", "success")
        except Exception as e:
            self._show_message(str(e), "error")

    def delete_project(self, pid):
        # NOTE: Keeping simple confirmation since users can misclick delete buttons easily.
        # This uses your parent frame window seamlessly.
        from tkinter import messagebox
        if messagebox.askyesno("Confirm Action", "Are you sure you want to delete this project and all connected tasks?"):
            try:
                self.db.cursor.execute("DELETE FROM projects WHERE id=%s", (pid,))
                self.db.conn.commit()
                self.refresh_projects()
                self._show_message("Project deleted completely.", "success")
            except Exception as e:
                self._show_message(f"Could not delete: {e}", "error")