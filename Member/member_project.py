import customtkinter as ctk
from database import Database
from tkinter import messagebox

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

                info_f = ctk.CTkFrame(card, fg_color="transparent")
                info_f.pack(side="left", padx=20, pady=15)
                
                ctk.CTkLabel(info_f, text=task['task_name'], font=("Arial", 15, "bold"),
                             text_color=("#2D3436", "#ECF0F1")).pack(anchor="w")
                
                ctk.CTkLabel(info_f, text=f"📂 Project: {task['project_name']}", 
                             font=("Arial", 11), text_color="#3498DB").pack(anchor="w")

                prog_f = ctk.CTkFrame(card, fg_color="transparent")
                prog_f.pack(side="right", padx=20)

                p_val = task['progress']
                p_lbl = ctk.CTkLabel(prog_f, text=f"{p_val}%", font=("Arial", 13, "bold"), text_color="#10B981")
                p_lbl.pack(side="right", padx=10)

                slider = ctk.CTkSlider(prog_f, from_=0, to=100, width=150,
                                       command=lambda v, tid=task['id'], pid=task['project_id'], lbl=p_lbl: 
                                       self.update_my_progress(tid, pid, v, lbl))
                slider.set(p_val)
                slider.pack(side="right", padx=10)

        except Exception as e:
            print(f"Member Task Error: {e}")

    def update_my_progress(self, tid, pid, val, lbl):
        """Task % ရော Project Overall % ကိုပါ Update လုပ်ခြင်း"""
        v = int(val)
        lbl.configure(text=f"{v}%")
        try:
            # 1. Update Task Progress
            self.db.cursor.execute("UPDATE tasks SET progress = %s WHERE id = %s", (v, tid))
            
            # 2. Recalculate Project Overall Progress
            self.db.cursor.execute("SELECT progress FROM tasks WHERE project_id = %s", (pid,))
            all_p = self.db.cursor.fetchall()
            avg_p = int(sum(r['progress'] for r in all_p) / len(all_p)) if all_p else 0
            
            status = f"In Progress ({avg_p}%)" if avg_p < 100 else "Completed (100%)"
            self.db.cursor.execute("UPDATE projects SET status = %s WHERE id = %s", (status, pid))
            
            self.db.conn.commit()
        except Exception as e:
            print(f"Update error: {e}")