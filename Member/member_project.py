import customtkinter as ctk
from database import Database
from tkinter import messagebox
from functools import partial

class MemberProject(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(self.header, text="My Assigned Tasks", 
                     font=("Arial", 24, "bold"),
                     text_color=("#1A1A1A", "#FFFFFF")).pack(side="left")

        # --- Scrollable Task List ---
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text="Your Workload")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_member_tasks()

    def validate_percent(self, value):
        """Restricts input to numbers 0-100"""
        if value == "":
            return True
        if value.isdigit() and 0 <= int(value) <= 100:
            return True
        return False

    def refresh_member_tasks(self):
        for w in self.scroll.winfo_children(): w.destroy()
        
        try:
            query = """
                SELECT t.*, p.project_name 
                FROM tasks t 
                JOIN projects p ON t.project_id = p.id 
                WHERE t.assigned_to = %s 
                ORDER BY t.id DESC
            """
            self.db.cursor.execute(query, (self.user['full_name'],))
            my_tasks = self.db.cursor.fetchall()

            if not my_tasks:
                ctk.CTkLabel(self.scroll, text="No tasks assigned yet.", text_color="gray").pack(pady=30)
                return

            for task in my_tasks:
                card = ctk.CTkFrame(self.scroll, corner_radius=12, border_width=1, 
                                    fg_color=("#FFFFFF", "#1E1E1E"), 
                                    border_color=("#E0E0E0", "#333333"))
                card.pack(fill="x", pady=8, padx=10)

                # --- Left Side: Info ---
                info_f = ctk.CTkFrame(card, fg_color="transparent")
                info_f.pack(side="left", padx=20, pady=15)
                
                ctk.CTkLabel(info_f, text=task['task_name'], font=("Arial", 15, "bold"),
                             text_color=("#2D3436", "#ECF0F1")).pack(anchor="w")
                
                ctk.CTkLabel(info_f, text=f"📂 Project: {task['project_name']}", 
                             font=("Arial", 11), text_color="#3498DB").pack(anchor="w")
                
                deadline = task.get('deadline', 'No Deadline')
                ctk.CTkLabel(info_f, text=f"📅 Due: {deadline}", 
                             font=("Arial", 11), text_color="#E74C3C").pack(anchor="w")

                # --- Right Side: Progress Area (Visual Spinbox) ---
                prog_f = ctk.CTkFrame(card, fg_color="transparent")
                prog_f.pack(side="right", padx=20)

                try:
                    p_val = int(task.get('progress') or 0)
                except:
                    p_val = 0

                # 1. Percentage Label
                display_text = "Not started" if p_val == 0 else f"{p_val}%"
                color = "#95A5A6" if p_val == 0 else "#10B981"
                p_lbl = ctk.CTkLabel(prog_f, text=display_text, font=("Arial", 13, "bold"), text_color=color)
                p_lbl.pack(side="right", padx=10)

                # 2. Spinbox Container (Entry + Buttons)
                spin_f = ctk.CTkFrame(prog_f, fg_color="transparent")
                spin_f.pack(side="right", padx=5)

                vcmd = (self.register(self.validate_percent), "%P")
                p_entry = ctk.CTkEntry(spin_f, width=55, height=32, justify="center", validate="key", validatecommand=vcmd)
                p_entry.insert(0, "" if p_val == 0 else str(p_val))
                p_entry.grid(row=0, column=0, rowspan=2, padx=(0, 2))

                # Visual UP Arrow
                ctk.CTkButton(spin_f, text="▲", width=20, height=15, font=("Arial", 7),
                              fg_color=("#E0E0E0", "#2B2B2B"), text_color=("#333", "#EEE"),
                              hover_color="#10B981",
                              command=lambda tid=task['id'], pid=task['project_id'], ent=p_entry, lbl=p_lbl: 
                              self.change_val_by_arrow(tid, pid, ent, lbl, 1)).grid(row=0, column=1, pady=(0, 1))

                # Visual DOWN Arrow
                ctk.CTkButton(spin_f, text="▼", width=20, height=15, font=("Arial", 7),
                              fg_color=("#E0E0E0", "#2B2B2B"), text_color=("#333", "#EEE"),
                              hover_color="#E74C3C",
                              command=lambda tid=task['id'], pid=task['project_id'], ent=p_entry, lbl=p_lbl: 
                              self.change_val_by_arrow(tid, pid, ent, lbl, -1)).grid(row=1, column=1)

                # Bindings for manual typing and keyboard arrows
                p_entry.bind("<KeyRelease>", partial(self.update_my_progress, task['id'], task['project_id'], p_entry, p_lbl))
                p_entry.bind("<Up>", lambda e, tid=task['id'], pid=task['project_id'], ent=p_entry, lbl=p_lbl: self.change_val_by_arrow(tid, pid, ent, lbl, 1))
                p_entry.bind("<Down>", lambda e, tid=task['id'], pid=task['project_id'], ent=p_entry, lbl=p_lbl: self.change_val_by_arrow(tid, pid, ent, lbl, -1))

        except Exception as e:
            print(f"Member Task Error: {e}")

    def update_my_progress(self, tid, pid, entry, lbl, event=None):
        """Updates UI and Database in real-time"""
        try:
            val = entry.get().strip()
            v = int(val) if val.isdigit() else 0

            # Update Label Visuals
            if v == 0:
                lbl.configure(text="Not started", text_color="#95A5A6")
            else:
                lbl.configure(text=f"{v}%", text_color="#10B981")

            if v < 0 or v > 100: return

            # 1. Update individual task
            self.db.cursor.execute("UPDATE tasks SET progress = %s WHERE id = %s", (v, tid))

            # 2. Update overall project status based on all tasks
            self.db.cursor.execute("SELECT progress FROM tasks WHERE project_id = %s", (pid,))
            all_p = self.db.cursor.fetchall()
            
            avg_p = int(sum(int(r['progress']) for r in all_p) / len(all_p)) if all_p else 0
            status = f"In Progress ({avg_p}%)" if avg_p < 100 else "Completed (100%)"
            
            self.db.cursor.execute("UPDATE projects SET status = %s WHERE id = %s", (status, pid))
            self.db.conn.commit()

        except Exception as e:
            print("Database Update Error:", e)
        
    def change_val_by_arrow(self, tid, pid, entry, lbl, delta):
        """Handles Up/Down (Buttons or Keyboard) to update percentage"""
        try:
            current_val = entry.get().strip()
            v = int(current_val) if current_val.isdigit() else 0
            new_v = max(0, min(100, v + delta))
            
            entry.delete(0, 'end')
            entry.insert(0, str(new_v) if new_v > 0 else "")
            
            # Sync with database and label
            self.update_my_progress(tid, pid, entry, lbl)
        except Exception as e:
            print(f"Arrow Interaction Error: {e}")