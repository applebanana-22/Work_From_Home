import customtkinter as ctk
from database import Database
from tkinter import messagebox

class TaskManagerWindow(ctk.CTkToplevel):
    def __init__(self, parent, project_id, project_name):
        super().__init__(parent)
        self.title(f"Tasks: {project_name}")
        self.geometry("750x650")
        self.db = Database()
        self.project_id = project_id
        self.project_name = project_name
        
        self.attributes("-topmost", True)
        self.grab_set()

        # --- Header & Overall Progress ---
        self.header_f = ctk.CTkFrame(self, fg_color="transparent")
        self.header_f.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(self.header_f, text=f"Project: {project_name}", 
                     font=("Arial", 20, "bold")).pack(side="left")

        # Overall Percentage Label (Dynamic)
        self.overall_lbl = ctk.CTkLabel(self.header_f, text="Overall: 0%", 
                                        font=("Arial", 16, "bold"), text_color="#10B981")
        self.overall_lbl.pack(side="right", padx=10)

        # --- Task Input Area ---
        input_f = ctk.CTkFrame(self, fg_color=("#EAEAEA", "#1E1E1E"), corner_radius=10)
        input_f.pack(fill="x", padx=20, pady=10)

        self.task_entry = ctk.CTkEntry(input_f, placeholder_text="Enter Task Name", width=250, height=35)
        self.task_entry.pack(side="left", padx=15, pady=15)

        self.db.cursor.execute("SELECT full_name FROM users WHERE role='member'")
        members = [row['full_name'] for row in self.db.cursor.fetchall()]
        
        self.member_dropdown = ctk.CTkOptionMenu(input_f, values=members if members else ["No Member"], height=35)
        self.member_dropdown.pack(side="left", padx=5)

        ctk.CTkButton(input_f, text="Add Task", fg_color="#10B981", width=90, height=35,
                      font=("Arial", 12, "bold"), command=self.add_task_with_confirm).pack(side="left", padx=10)

        # --- Task List Area ---
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Project Tasks", fg_color=("#F5F5F5", "#121212"))
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_tasks()

    def calculate_project_progress(self):
        """Task အားလုံးရဲ့ percentage ကို ပျမ်းမျှတွက်ချက်ပြီး Project status ကို update လုပ်ခြင်း"""
        try:
            self.db.cursor.execute("SELECT progress FROM tasks WHERE project_id = %s", (self.project_id,))
            all_progress = self.db.cursor.fetchall()
            
            if not all_progress:
                total_avg = 0
            else:
                total_sum = sum(row['progress'] for row in all_progress)
                total_avg = int(total_sum / len(all_progress))

            # UI Update
            self.overall_lbl.configure(text=f"Overall: {total_avg}%")

            # Database Update (Project table ထဲမှာ status သို့မဟုတ် percentage သိမ်းလိုပါက)
            status = "Completed" if total_avg == 100 else "In Progress"
            sql = "UPDATE projects SET status = %s WHERE id = %s"
            self.db.cursor.execute(sql, (f"{status} ({total_avg}%)", self.project_id))
            self.db.conn.commit()
            
        except Exception as e:
            print(f"Calculation Error: {e}")

    def add_task_with_confirm(self):
        """CRUD Create: Confirmation with Parent focus"""
        name = self.task_entry.get().strip()
        member = self.member_dropdown.get()
        if not name: return

        if messagebox.askyesno("Confirm", 
                               f"Add task '{name}' and assign to {member}?", 
                               parent=self):
            try:
                sql = "INSERT INTO tasks (project_id, task_name, assigned_to, progress) VALUES (%s, %s, %s, 0)"
                self.db.cursor.execute(sql, (self.project_id, name, member))
                self.db.conn.commit()
                self.task_entry.delete(0, 'end')
                self.refresh_tasks()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def refresh_tasks(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        
        self.db.cursor.execute("SELECT * FROM tasks WHERE project_id = %s", (self.project_id,))
        for row in self.db.cursor.fetchall():
            card = ctk.CTkFrame(self.list_frame, fg_color=("#FFFFFF", "#252525"), corner_radius=8)
            card.pack(fill="x", pady=5, padx=5)

            info = f"{row['task_name']} \nAssign: {row['assigned_to']}"
            ctk.CTkLabel(card, text=info, justify="left", font=("Arial", 12, "bold")).pack(side="left", padx=15, pady=10)

            # Percentage Label that updates in real-time
            p_val = row['progress']
            p_lbl = ctk.CTkLabel(card, text=f"{p_val}%", font=("Arial", 12, "bold"), text_color="#3498DB")
            p_lbl.pack(side="right", padx=15)

            # Update Slider
            slider = ctk.CTkSlider(card, from_=0, to=100, width=150, 
                                   command=lambda v, tid=row['id'], lbl=p_lbl: self.update_progress_logic(tid, v, lbl))
            slider.set(p_val)
            slider.pack(side="right", padx=10)

            # Delete with Confirmation
            ctk.CTkButton(card, text="🗑", width=30, fg_color="#C0392B", hover_color="#A93226",
                          command=lambda tid=row['id']: self.delete_task_with_confirm(tid)).pack(side="right", padx=5)
        
        # Refresh တိုင်း overall progress ကိုပါ တွက်ချက်မည်
        self.calculate_project_progress()

    def update_progress_logic(self, task_id, value, lbl):
        """CRUD Update: Real-time calculation on slider move"""
        v = int(value)
        lbl.configure(text=f"{v}%")
        try:
            self.db.cursor.execute("UPDATE tasks SET progress = %s WHERE id = %s", (v, task_id))
            self.db.conn.commit()
            # Slider ရွှေ့လိုက်တိုင်း overall progress ကိုပါ ပြန်တွက်ချက်ရန်
            self.calculate_project_progress()
        except: pass

    def delete_task_with_confirm(self, task_id):
        """CRUD Delete: Confirmation box ကို TaskManager window အပေါ်မှာပဲ ပြသခြင်း"""
        # parent=self ထည့်ပေးခြင်းဖြင့် confirmation box သည် ဤ window ပေါ်တွင်သာ ပေါ်မည်
        if messagebox.askyesno("Confirm Delete", 
                               "Are you sure you want to delete this task?", 
                               parent=self): 
            try:
                self.db.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                self.db.conn.commit()
                self.refresh_tasks()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)