import customtkinter as ctk
from database import Database
from tkinter import messagebox
from tkcalendar import DateEntry  # Required for calendar selector

class TaskManagerWindow(ctk.CTkToplevel):
    def __init__(self, parent, project_id, project_name, user_data):
        super().__init__(parent)
        self.title(f"Tasks: {project_name}")
        self.geometry("900x750")
        self.db = Database()
        self.project_id = project_id
        self.project_name = project_name
        self.user = user_data 
        
        self.attributes("-topmost", True)
        self.grab_set()

        # --- Header ---
        self.header_f = ctk.CTkFrame(self, fg_color="transparent")
        self.header_f.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(self.header_f, text=f"Project: {project_name}", 
                     font=("Arial", 22, "bold")).pack(side="left")

        self.overall_lbl = ctk.CTkLabel(self.header_f, text="Overall: 0%", 
                                        font=("Arial", 18, "bold"), text_color="#10B981")
        self.overall_lbl.pack(side="right", padx=10)

        # --- Control Panel ---
        control_f = ctk.CTkFrame(self, fg_color=("#EAEAEA", "#1E1E1E"), corner_radius=12)
        control_f.pack(fill="x", padx=20, pady=5)

        self.search_entry = ctk.CTkEntry(control_f, placeholder_text="🔍 Search...", width=150)
        self.search_entry.pack(side="left", padx=10, pady=15)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_tasks())

        self.task_entry = ctk.CTkEntry(control_f, placeholder_text="Task Name", width=150)
        self.task_entry.pack(side="left", padx=5)

        # CALENDAR SELECTOR
        ctk.CTkLabel(control_f, text="📅").pack(side="left", padx=(5, 0))
        self.deadline_picker = DateEntry(control_f, width=12, background='darkblue',
                                         foreground='white', borderwidth=2, 
                                         date_pattern='yyyy-mm-dd')
        self.deadline_picker.pack(side="left", padx=5, pady=15)

        members = self.get_team_members()
        self.member_dropdown = ctk.CTkOptionMenu(control_f, values=members if members else ["No Member"], width=140)
        self.member_dropdown.set("Select Member")
        self.member_dropdown.pack(side="left", padx=5)

        ctk.CTkButton(control_f, text="Add", fg_color="#10B981", hover_color="#059669", width=70,
                      font=("Arial", 12, "bold"), command=self.add_task_with_confirm).pack(side="left", padx=10)

        # --- Task List Area ---
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Task Breakdown", fg_color=("#F5F5F5", "#121212"))
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_tasks()

    def get_team_members(self):
        try:
            query = "SELECT full_name FROM users WHERE role='member' AND team_id = %s"
            self.db.cursor.execute(query, (self.user['team_id'],))
            return [row['full_name'] for row in self.db.cursor.fetchall()]
        except: return []

    def get_status_color(self, progress):
        if progress == 100: return "#10B981"
        if progress >= 50: return "#F39C12"
        return "#3498DB"

    def refresh_tasks(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        search_query = self.search_entry.get().lower()
        
        try:
            sql = "SELECT * FROM tasks WHERE project_id = %s ORDER BY id DESC"
            self.db.cursor.execute(sql, (self.project_id,))
            tasks = self.db.cursor.fetchall()

            for row in tasks:
                if search_query and search_query not in row['task_name'].lower(): continue

                card = ctk.CTkFrame(self.list_frame, fg_color=("#FFFFFF", "#252525"), corner_radius=8)
                card.pack(fill="x", pady=4, padx=5)

                info_f = ctk.CTkFrame(card, fg_color="transparent")
                info_f.pack(side="left", padx=15, pady=8)
                
                deadline = row.get('deadline', 'No deadline')
                ctk.CTkLabel(info_f, text=row['task_name'], font=("Arial", 13, "bold")).pack(anchor="w")
                ctk.CTkLabel(info_f, text=f"👤 {row['assigned_to']}  |  📅 {deadline}", 
                             font=("Arial", 11), text_color="gray").pack(anchor="w")

                actions_f = ctk.CTkFrame(card, fg_color="transparent")
                actions_f.pack(side="right", padx=10)

                p_val = row['progress']
                color = self.get_status_color(p_val)
                ctk.CTkLabel(actions_f, text=f"{p_val}%", font=("Arial", 14, "bold"), 
                             text_color=color, width=50).pack(side="right", padx=15)

                # Edit Button (Orange Style)
                ctk.CTkButton(actions_f, text="Edit", width=60, height=30,
                              fg_color="#F39C12", hover_color="#D35400", font=("Arial", 12),
                              command=lambda r=row: self.open_edit_dialog(r)).pack(side="right", padx=5)

                # Delete Button (Red Style)
                ctk.CTkButton(actions_f, text="🗑", width=35, height=30,
                              fg_color="#C0392B", hover_color="#A93226",
                              command=lambda tid=row['id']: self.delete_task_with_confirm(tid)).pack(side="right", padx=5)
            
            self.calculate_project_progress()
        except Exception as e: print(f"Refresh Error: {e}")

    def open_edit_dialog(self, task_row):
        """Fixed: Popup window to edit Name, Deadline, and Member (Progress removed)"""
        edit_win = ctk.CTkToplevel(self)
        edit_win.title("Edit Task")
        edit_win.geometry("350x480") # Adjusted height
        edit_win.attributes("-topmost", True)
        edit_win.grab_set()

        ctk.CTkLabel(edit_win, text="Update Task Details", font=("Arial", 16, "bold")).pack(pady=15)

        # 1. Edit Task Name
        ctk.CTkLabel(edit_win, text="Task Name:").pack(anchor="w", padx=50)
        name_ent = ctk.CTkEntry(edit_win, placeholder_text="Task Name", width=250)
        name_ent.insert(0, task_row['task_name'])
        name_ent.pack(pady=5)

        # 2. Reassign Member
        ctk.CTkLabel(edit_win, text="Assign To:").pack(anchor="w", padx=50, pady=(10, 0))
        members = self.get_team_members()
        member_var = ctk.StringVar(value=task_row['assigned_to'])
        member_dropdown = ctk.CTkOptionMenu(edit_win, values=members, variable=member_var, width=250)
        member_dropdown.pack(pady=5)

        # 3. Edit Deadline
        ctk.CTkLabel(edit_win, text="Deadline:").pack(pady=(10, 0))
        new_cal = DateEntry(edit_win, date_pattern='yyyy-mm-dd', width=20)
        try:
            new_cal.set_date(task_row['deadline'])
        except:
            pass 
        new_cal.pack(pady=10)

        def save_changes():
            try:
                new_name = name_ent.get().strip() or task_row['task_name']
                new_member = member_var.get()
                new_date = new_cal.get_date().strftime('%Y-%m-%d')
                
                # SQL UPDATE: Progress (%s) removed from here
                sql = """
                    UPDATE tasks 
                    SET task_name=%s, deadline=%s, assigned_to=%s 
                    WHERE id=%s
                """
                self.db.cursor.execute(sql, (
                    new_name, 
                    new_date, 
                    new_member, 
                    task_row['id']
                ))
                
                self.db.conn.commit()
                
                # Refresh main task screen
                self.refresh_tasks() 
                edit_win.destroy()
                messagebox.showinfo("Success", "Task updated successfully!")
                
            except Exception as e:
                messagebox.showerror("Update Error", str(e))

        ctk.CTkButton(edit_win, text="Save Changes", command=save_changes, 
                      fg_color="#10B981", hover_color="#059669").pack(pady=25)

    def calculate_project_progress(self):
        try:
            self.db.cursor.execute("SELECT progress FROM tasks WHERE project_id = %s", (self.project_id,))
            rows = self.db.cursor.fetchall()
            avg = int(sum(r['progress'] for r in rows) / len(rows)) if rows else 0
            self.overall_lbl.configure(text=f"Overall: {avg}%")
            status = "Completed" if avg == 100 else "In Progress"
            self.db.cursor.execute("UPDATE projects SET status = %s WHERE id = %s", 
                                   (f"{status} ({avg}%)", self.project_id))
            self.db.conn.commit()
        except: pass

    def add_task_with_confirm(self):
        name = self.task_entry.get().strip()
        member = self.member_dropdown.get()
        deadline = self.deadline_picker.get_date().strftime('%Y-%m-%d')
        
        if not name or member in ["Select Member", "No Member"]:
            messagebox.showwarning("Missing Info", "Enter task name and select a member.")
            return

        if messagebox.askyesno("Confirm", f"Assign '{name}' to {member}?", parent=self):
            try:
                sql = "INSERT INTO tasks (project_id, task_name, assigned_to, deadline, progress) VALUES (%s, %s, %s, %s, 0)"
                self.db.cursor.execute(sql, (self.project_id, name, member, deadline))
                self.db.conn.commit()
                self.task_entry.delete(0, 'end')
                self.refresh_tasks()
            except Exception as e: messagebox.showerror("Database Error", str(e), parent=self)

    def delete_task_with_confirm(self, task_id):
        if messagebox.askyesno("Confirm Delete", "Permanently delete this task?", parent=self): 
            try:
                self.db.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                self.db.conn.commit()
                self.refresh_tasks()
            except Exception as e: messagebox.showerror("Error", str(e), parent=self)