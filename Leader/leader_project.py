import customtkinter as ctk
from database import Database
from tkinter import messagebox
# Ensure this import matches your actual file structure for the TaskManager
#from Leader.task_manager import TaskManagerWindow

class LeaderProject(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user

        # --- Header Section ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=30, pady=(20, 10))
        
        ctk.CTkLabel(self.header, text="Project Hub", 
                     font=("Arial", 26, "bold"),
                     text_color=("#1A1A1A", "#FFFFFF")).pack(side="left")

        self.add_btn = ctk.CTkButton(self.header, text="+ New Project", 
                                     fg_color="#10B981", hover_color="#059669",
                                     height=40, font=("Arial", 13, "bold"),
                                     command=self.open_create_project)
        self.add_btn.pack(side="right")

        # --- Project List Area ---
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Ongoing Projects", 
                                                 fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_projects()

    def open_task_manager(self, proj):
        # clear current view (safe way)
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
        # 1. Clear existing cards to prevent duplication
        for w in self.list_frame.winfo_children(): 
            w.destroy()
        
        try:
            # 2. Filter query by team_id so leaders only see their own team's projects
            # This ensures Team 1 projects don't show up for other team leaders
            sql = "SELECT * FROM projects WHERE team_id = %s ORDER BY id DESC"
            self.db.cursor.execute(sql, (self.user['team_id'],))
            projects = self.db.cursor.fetchall()
            
            if not projects:
                ctk.CTkLabel(self.list_frame, text="No projects found for your team.", 
                             text_color="gray", font=("Arial", 14)).pack(pady=40)
                return

            for proj in projects:
                # --- Card Container ---
                card = ctk.CTkFrame(self.list_frame, corner_radius=12, border_width=1, 
                                    fg_color=("#FFFFFF", "#1E1E1E"), 
                                    border_color=("#E0E0E0", "#333333"))
                card.pack(fill="x", pady=8, padx=10)
                
                # --- Left: Info Section ---
                info_f = ctk.CTkFrame(card, fg_color="transparent")
                info_f.pack(side="left", padx=20, pady=15)
                
                ctk.CTkLabel(info_f, text=proj['project_name'], font=("Arial", 16, "bold"),
                             text_color=("#2D3436", "#ECF0F1")).pack(anchor="w")


                #print(f"status = {proj['status']}")

                # Dynamic status color based on progress string
                status_color = "#F1C40F" if "Pending" in proj['status'] else "#2ECC71"
                ctk.CTkLabel(info_f, text=f"● {proj['status']}", font=("Arial", 12),
                             text_color=status_color).pack(anchor="w")

                # --- Right: Action Buttons ---
                btn_f = ctk.CTkFrame(card, fg_color="transparent")
                btn_f.pack(side="right", padx=20)
                
                # 1. Manage Tasks Button
                ctk.CTkButton(
                    btn_f, 
                    text="Manage", 
                    width=80, 
                    height=32, 
                    fg_color="#3498DB", 
                    command=lambda p=proj: self.open_task_manager(p)
                ).pack(side="left", padx=5)

                # 2. Edit Project Button
                ctk.CTkButton(
                    btn_f, 
                    text="Edit", 
                    width=60, 
                    height=32, 
                    fg_color="#F39C12", 
                    hover_color="#D35400",
                    command=lambda p=proj: self.update_project(p['id'], p['project_name'])
                ).pack(side="left", padx=5)

                # 3. Delete Button
                ctk.CTkButton(
                    btn_f, 
                    text="Delete", 
                    width=60, 
                    height=32, 
                    fg_color="#E74C3C",
                    command=lambda pid=proj['id']: self.delete_project(pid)
                ).pack(side="left", padx=5)
                
        except Exception as e:
            print(f"Database Error in refresh_projects: {e}")

    def open_create_project(self):
        """CRUD: Create New Project with Team Association"""
        dialog = ctk.CTkInputDialog(text="Enter Project Name:", title="New Project")
        p_name = dialog.get_input()
        if p_name:
            try:
                # ADDED team_id to the INSERT statement
                sql = "INSERT INTO projects (project_name, created_by, team_id, status) VALUES (%s, %s, %s, %s)"
                
                # Use self.user['team_id'] to lock this project to Team 1, Team 2, etc.
                self.db.cursor.execute(sql, (
                    p_name.strip(), 
                    self.user['full_name'], 
                    self.user['team_id'], 
                    'Pending'
                ))
                
                self.db.conn.commit()
                self.refresh_projects()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def update_project(self, pid, old_name):
        """CRUD: Update Project Name"""
        dialog = ctk.CTkInputDialog(text=f"Update name for '{old_name}':", title="Edit Project")
        new_name = dialog.get_input()
        
        if new_name and new_name.strip() != old_name:
            if messagebox.askyesno("Confirm Update", f"Change project name to '{new_name}'?"):
                try:
                    sql = "UPDATE projects SET project_name = %s WHERE id = %s"
                    self.db.cursor.execute(sql, (new_name.strip(), pid))
                    self.db.conn.commit()
                    messagebox.showinfo("Success", "Project updated successfully!")
                    self.refresh_projects()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def delete_project(self, pid):
        """CRUD: Delete Project"""
        if messagebox.askyesno("Confirm", "Delete this project and all related tasks?"):
            try:
                self.db.cursor.execute("DELETE FROM projects WHERE id=%s", (pid,))
                self.db.conn.commit()
                self.refresh_projects()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete: {e}")