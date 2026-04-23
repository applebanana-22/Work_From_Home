from datetime import datetime
import customtkinter as ctk
from database import Database
from tkinter import messagebox
from tkcalendar import DateEntry

class MemberProject(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")

        self.db = Database()
        self.user = user

        # Define Modern Color Palette (Light Mode Color, Dark Mode Color)
        self.colors = {
            "main_bg": ("#F8FAFC", "#0F172A"),
            "card_bg": ("#FFFFFF", "#1E293B"),
            "text_main": ("#1E293B", "#F8FAFC"),
            "text_muted": ("#64748B", "#94A3B8"),
            "accent_blue": "#3B82F6",
            "accent_green": "#10B981",
            "accent_red": "#EF4444",
            "accent_amber": "#F59E0B",
            "border": ("#E2E8F0", "#334155")
        }

        # STATE
        self.current_task = None
        self.editing_history_id = None

        # ---------------- LAYERS ----------------
        self.layer1 = ctk.CTkFrame(self, fg_color="transparent")
        self.layer2 = ctk.CTkFrame(self, fg_color="transparent")
        self.layer3 = ctk.CTkFrame(self, fg_color="transparent")

        self.layer1.pack(fill="both", expand=True)

        self.build_layer1()
        self.build_layer2()

    # =========================================================
    # LAYER SWITCHER
    # =========================================================
    def show_layer(self, layer):
        for l in [self.layer1, self.layer2, self.layer3]:
            l.pack_forget()
        layer.pack(fill="both", expand=True, padx=20, pady=10)

    # =========================================================
    # LAYER 1 - TASK LIST (DASHBOARD)
    # =========================================================
    def build_layer1(self):
        # Header
        header = ctk.CTkFrame(self.layer1, fg_color="transparent")
        header.pack(fill="x", pady=(10, 20))

        ctk.CTkLabel(
            header,
            text="My Assigned Tasks",
            font=("Inter", 28, "bold"),
            text_color=self.colors["text_main"]
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            header,
            text="↻ Refresh",
            width=100,
            fg_color=self.colors["accent_blue"],
            hover_color="#2563EB",
            corner_radius=8,
            command=self.refresh_tasks
        ).pack(side="right", padx=10)

        # Scrollable Area
        self.scroll = ctk.CTkScrollableFrame(
            self.layer1, 
            fg_color="transparent",
            scrollbar_button_color=self.colors["accent_blue"]
        )
        self.scroll.pack(fill="both", expand=True)

        self.refresh_tasks()

    def refresh_tasks(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        # self.db.cursor.execute("""
        #     SELECT t.*, p.project_name
        #     FROM tasks t
        #     JOIN projects p ON t.project_id = p.id
        #     WHERE t.assigned_to = %s
        #     ORDER BY t.id DESC
        # """, (self.user['full_name'],))


        self.db.cursor.execute("""
            SELECT 
                t.*, 
                p.project_name,
                t.status,
                -- Calculate sum from history table for this specific task
                COALESCE((
                    SELECT SUM(h.progress) 
                    FROM progress_history h 
                    WHERE h.task_id = t.id
                ), 0) as total_calculated_progress
            FROM tasks t
            JOIN projects p ON t.project_id = p.id
            WHERE t.assigned_to = %s
            ORDER BY t.id DESC
        """, (self.user['full_name'],))

        tasks = self.db.cursor.fetchall()
        for task in tasks:
            self.create_task_card(task)

    def create_task_card(self, task):
        card = ctk.CTkFrame(
            self.scroll, 
            fg_color=self.colors["card_bg"], 
            corner_radius=12,
            border_width=1,
            border_color=self.colors["border"]
        )
        card.pack(fill="x", pady=8, padx=5)

        # Left: Info
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(info, text=task['project_name'].upper(), font=("Inter", 11, "bold"), 
                     text_color=self.colors["accent_blue"]).pack(anchor="w")
        
        ctk.CTkLabel(info, text="Task Name : "+task['task_name'], font=("Inter", 18, "bold"), 
                     text_color=self.colors["text_main"]).pack(anchor="w")

        ctk.CTkLabel(info, text=f"DeadLine : {task['deadline']}", font=("Inter", 18, "bold"), 
                     text_color=self.colors["text_main"]).pack(anchor="w")

        #progress_val = (task.get("progress") or 0) / 100
        progress_val = task.get('total_calculated_progress', 0) / 100
        pbar = ctk.CTkProgressBar(info, width=220, progress_color=self.colors["accent_green"])
        pbar.set(progress_val)
        pbar.pack(anchor="w", pady=(12, 5))
        
        ctk.CTkLabel(info, text=f"{int(progress_val*100)}% Complete", font=("Inter", 12),
                     text_color=self.colors["text_muted"]).pack(anchor="w")

        # Right: Buttons
        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.pack(side="right", padx=20)

        ctk.CTkButton(
            btns, text="📝 Report", fg_color=self.colors["accent_blue"],
            hover_color="#2563EB", width=110, corner_radius=8,
            command=lambda t=task: self.open_report(t)
        ).pack(pady=5)

        ctk.CTkButton(
            btns, text="📜 History", fg_color="transparent", border_width=1,
            border_color=self.colors["border"], text_color=self.colors["text_main"],
            hover_color=("#F1F5F9", "#334155"), width=110, corner_radius=8,
            command=lambda t=task: self.open_history(t)
        ).pack(pady=5)

    # =========================================================
    # LAYER 2 - REPORT / EDIT FORM
    # =========================================================
    def build_layer2(self):
        # Centering container
        form_wrapper = ctk.CTkFrame(self.layer2, fg_color="transparent")
        form_wrapper.place(relx=0.5, rely=0.5, anchor="center")

        card = ctk.CTkFrame(
            form_wrapper, 
            fg_color=self.colors["card_bg"],
            corner_radius=15,
            border_width=1,
            border_color=self.colors["border"]
        )
        card.pack(padx=20, pady=20)

        self.title_label = ctk.CTkLabel(card, text="Submit Report", font=("Inter", 22, "bold"))
        self.title_label.pack(pady=(25, 20), padx=50)

        def create_label(text):
            ctk.CTkLabel(card, text=text, font=("Inter", 12, "bold"), 
                         text_color=self.colors["text_muted"]).pack(anchor="w", padx=40)

        create_label("PROGRESS (%)")
        self.progress_entry = ctk.CTkEntry(card, width=320, height=40, corner_radius=8)
        self.progress_entry.pack(padx=40, pady=(5, 15))

        create_label("UPDATE DATE")
        date_frame = ctk.CTkFrame(card, fg_color="transparent")
        date_frame.pack(padx=40, pady=(5, 15), fill="x")
        self.date_picker = DateEntry(date_frame, date_pattern='yyyy-mm-dd', background='#3B82F6', foreground='white')
        self.date_picker.pack(fill="x", ipady=5)

        create_label("NOTES")
        self.note_box = ctk.CTkTextbox(card, width=320, height=100, corner_radius=8, border_width=1)
        self.note_box.pack(padx=40, pady=(5, 20))

        btn_f = ctk.CTkFrame(card, fg_color="transparent")
        btn_f.pack(fill="x", padx=40, pady=(0, 30))

        self.submit_btn = ctk.CTkButton(
            btn_f, text="💾 Submit", fg_color=self.colors["accent_green"], 
            hover_color="#059669", height=40, corner_radius=8, command=self.submit_report
        )
        self.submit_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))

        cancel_btn = ctk.CTkButton(
            btn_f, text="Cancel", fg_color="transparent", border_width=1, 
            text_color=self.colors["text_main"], height=40, corner_radius=8, command=self.back_to_main
        )
        cancel_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

    # =========================================================
    # LAYER 3 - PROGRESS HISTORY
    # =========================================================
    def build_history(self):
        for w in self.layer3.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self.layer3, fg_color="transparent")
        header.pack(fill="x", pady=10)

        ctk.CTkButton(header, text="← Back", width=80, fg_color="transparent", 
                      text_color=self.colors["text_main"], command=self.back_from_history).pack(side="left")

        ctk.CTkLabel(header, text="Task History", font=("Inter", 24, "bold")).pack(side="left", padx=20)

        container = ctk.CTkScrollableFrame(self.layer3, fg_color="transparent")
        container.pack(fill="both", expand=True)

        self.db.cursor.execute("""
            SELECT * FROM progress_history WHERE task_id=%s ORDER BY update_date DESC, id DESC
        """, (self.current_task['id'],))
        
        rows = self.db.cursor.fetchall()
        for r in rows:
            self.create_history_card(container, r)

    def create_history_card(self, parent, row):
        card = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=10)
        card.pack(fill="x", pady=5, padx=5)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(info, text=f"{row['update_date']} — {row['progress']}%", 
                     font=("Inter", 14, "bold"), text_color=self.colors["accent_blue"]).pack(anchor="w")
        ctk.CTkLabel(info, text=row['note'], font=("Inter", 12), wraplength=400).pack(anchor="w")

        btn_f = ctk.CTkFrame(card, fg_color="transparent")
        btn_f.pack(side="right", padx=10)

        ctk.CTkButton(btn_f, text="Edit", width=60, fg_color=self.colors["accent_amber"],
                      command=lambda r=row: self.edit_history(r)).pack(side="left", padx=2)
        ctk.CTkButton(btn_f, text="Delete", width=60, fg_color=self.colors["accent_red"],
                      command=lambda r=row: self.delete_history(r)).pack(side="left", padx=2)

    # =========================================================
    # CORE LOGIC
    # =========================================================
    def open_report(self, task):
        self.current_task = task
        self.editing_history_id = None
        self.title_label.configure(text="Submit Report")
        self.submit_btn.configure(text="💾 Submit")
        self.progress_entry.delete(0, "end")
        self.progress_entry.insert(0, 0)

        # Reset Date Picker to TODAY
        self.date_picker.set_date(datetime.now())
        
        self.note_box.delete("1.0", "end")
        self.show_layer(self.layer2)

    def open_history(self, task):
        self.current_task = task
        self.build_history()
        self.show_layer(self.layer3)

    def edit_history(self, row):
        self.editing_history_id = row['id']
        self.title_label.configure(text="Edit History Record")
        self.submit_btn.configure(text="💾 Update")
        self.progress_entry.delete(0, "end")
        self.progress_entry.insert(0, str(row['progress']))

        # Fill Date Correctly
        # If row['update_date'] is already a date object, set_date handles it.
        # If it's a string, we convert it first.
        db_date = row['update_date']
        if isinstance(db_date, str):
            try:
                db_date = datetime.strptime(db_date, '%Y-%m-%d')
            except ValueError:
                db_date = datetime.now() # Fallback
        
        self.date_picker.set_date(db_date)

        self.note_box.delete("1.0", "end")
        self.note_box.insert("1.0", row['note'])
        self.show_layer(self.layer2)

    def update_task_progress(self, task_id):
        self.db.cursor.execute("""
            SELECT COALESCE(SUM(progress), 0) AS total
            FROM progress_history
            WHERE task_id = %s
        """, (task_id,))

        row = self.db.cursor.fetchone()

        # ✅ Safe dictionary access
        total = int(float(row['total'])) if row and row['total'] is not None else 0

        # Clamp to 100
        total = min(total, 100)

        self.db.cursor.execute("""
            UPDATE tasks 
            SET progress = %s 
            WHERE id = %s
        """, (total, task_id))

    def submit_report(self):
        try:
            # Common Data Gathering 
            val = int(self.progress_entry.get() or 0) 
            note = self.note_box.get("1.0", "end").strip() 
            # This fetches the date currently selected in the widget 
            date_str = self.date_picker.get_date().strftime('%Y-%m-%d') 
            if self.editing_history_id: 
                ## ✅ edit MODE
                # --- MODE: EDIT --- 
                self.db.cursor.execute(""" UPDATE progress_history SET progress=%s, note=%s, update_date=%s WHERE id=%s """, 
                (val, note, date_str, self.editing_history_id)) 

                #update progress in tasks table
                self.update_task_progress(self.current_task['id'])
                self.db.conn.commit()

                messagebox.showinfo("Success", "Update complete") 
                self.open_history(self.current_task) # Go back to history list
            else:
                # ✅ CREATE MODE
                # Update main task status 
                #self.db.cursor.execute("UPDATE tasks SET progress=%s WHERE id=%s", 
                #(val, self.current_task['id'])) 
                # Add new history record 
                self.db.cursor.execute(""" INSERT INTO progress_history (task_id, project_id, member_name, progress, note, update_date) 
                VALUES (%s, %s, %s, %s, %s, %s) """, 
                (self.current_task['id'], self.current_task['project_id'], self.user['full_name'], val, note, date_str)) 

                #update progress in tasks table
                self.update_task_progress(self.current_task['id'])
                self.db.conn.commit()

                messagebox.showinfo("Success", "Report added") 
                self.back_to_main() # Go back to task list 
                self.refresh_tasks()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for progress")
        except Exception as e:
            print("REAL ERROR:", e)  # 👈 IMPORTANT DEBUG
            messagebox.showerror("Error", f"Database error: {e}")
    
    def delete_history(self, row):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            self.db.cursor.execute("DELETE FROM progress_history WHERE id=%s", (row['id'],))
            self.db.conn.commit()
            self.build_history()

    def back_to_main(self):
        # If we were editing a history record, go back to the history layer
        if self.editing_history_id:
            self.editing_history_id = None # Clear the state
            self.show_layer(self.layer3)
        else:
            # Otherwise, go back to the main task list
            self.show_layer(self.layer1)

    def back_from_history(self):
        self.show_layer(self.layer1)
        self.refresh_tasks()