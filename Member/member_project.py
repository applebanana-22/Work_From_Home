from datetime import datetime
import customtkinter as ctk
from database import Database
from tkinter import messagebox
from tkcalendar import DateEntry
import tkinter.ttk as ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta,date

class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None):
        super().__init__(master, fg_color="transparent")

        self._date = initial_date or datetime.today().date()
        self._open = False
        max_date = datetime.today().date()

        # -------- STYLE (THIS FIXES YOUR DESIGN) --------
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Custom.Calendar",
            background="#1A1A2E",
            foreground="white",
            headersbackground="#16213E",
            headersforeground="#4FC3F7",
            selectbackground="#3498DB",
            selectforeground="white",
            normalbackground="#1A1A2E",
            normalforeground="#CCCCCC",
            weekendbackground="#1A1A2E",
            weekendforeground="#F39C12",
            othermonthforeground="#555555",
            bordercolor="#2A2A4A",
            relief="flat"
        )

        # -------- INPUT BUTTON --------
        self.btn = ctk.CTkButton(
            self,
            text=self._fmt(),
            width=170,
            height=36,
            corner_radius=10,
            fg_color="#1E2A3A",
            hover_color="#2C3E50",
            border_width=1,
            border_color="#3D5166",
            anchor="w",
            command=self.toggle
        )
        self.btn.pack()

        # -------- FLOATING PANEL --------
        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color="#141E2B",
            corner_radius=12,
            border_width=1,
            border_color="#2A3A4A"
        )

        # -------- REAL CALENDAR --------
        self.cal = Calendar(
            self.panel,
            style="Custom.Calendar",
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            year=self._date.year,
            month=self._date.month,
            day=self._date.day,
            maxdate=max_date,
            showweeknumbers=False,
            firstweekday="monday",
            font=("Arial", 11),
            cursor="hand2"
        )
        self.cal.pack(padx=8, pady=8)

        # 🔥 SELECT IMMEDIATELY (no button)
        self.cal.bind("<<CalendarSelected>>", self._select)

    # -------- FUNCTIONS --------
    def toggle(self):
        if self._open:
            self.panel.place_forget()
        else:
            self.panel.lift()
            self.panel.place(
                in_=self,
                x=0,
                y=self.btn.winfo_height() + 2
            )
        self._open = not self._open

    def _select(self, event):
        selected = self.cal.get_date()
        self._date = datetime.strptime(selected, "%Y-%m-%d").date()
        self.btn.configure(text=self._fmt())
        self.toggle()

    def _fmt(self):
        return f" 📅 {self._date.strftime('%Y-%m-%d')}"

    def get_date(self):
        return self._date

    def set_date(self, d):
        self._date = d
        self.cal.selection_set(d)
        self.btn.configure(text=self._fmt())

    def set_mindate(self, date_val):
        if isinstance(date_val, datetime):
            date_val = date_val.date()
        # This updates the underlying tkcalendar logic
        self.cal.config(mindate=date_val)

        # Normalize self._date
        # current_date = (
        #     self._date.date()
        #     if isinstance(self._date, datetime)
        #     else self._date
        # )

        current_date = self._date

        if isinstance(current_date, datetime):
            current_date = current_date.date()

        # If the current selected date is now illegal, reset it to the mindate
        # if self._date < date_val:
        #     self.set_date(date_val)
        if current_date < date_val:
            self.set_date(date_val)


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

        # ctk.CTkButton(
        #     header,
        #     text="↻ Refresh",
        #     width=100,
        #     fg_color=self.colors["accent_blue"],
        #     hover_color="#2563EB",
        #     text_color=("#2D3436", "#ECF0F1"),
        #     corner_radius=8,
        #     command=self.refresh_tasks
        # ).pack(side="right", padx=10)

        # Scrollable Area
        self.scroll = ctk.CTkScrollableFrame(
            self.layer1, 
            fg_color="transparent",
            scrollbar_button_color="#A0A0A0", # Grey scrollbar
            scrollbar_button_hover_color="#808080"
        )
        
        self.scroll.pack(fill="both", expand=True, anchor="w", padx=20, pady=(10, 0))

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
        is_complete = progress_val >= 1.0
        pbar = ctk.CTkProgressBar(info, width=220, progress_color=self.colors["accent_green"])
        pbar.set(progress_val)
        pbar.pack(anchor="w", pady=(12, 5))
        
        ctk.CTkLabel(info, text=f"{int(progress_val*100)}% Complete", font=("Inter", 12),
                     text_color=self.colors["text_muted"]).pack(anchor="w")

        # Right: Buttons
        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.pack(side="right", padx=20)


        ctk.CTkButton(
            btns, text="📝 Report", state="disabled" if is_complete else "normal", fg_color=self.colors["accent_blue"] if not is_complete else "grey",
            hover_color="#2563EB",text_color=("#2D3436", "#ECF0F1"), width=110, corner_radius=8,
            command=lambda t=task: self.open_report(t)
        ).pack(pady=5)

        ctk.CTkButton(
            btns, text="📜 History", fg_color="transparent", border_width=1,
            border_color=self.colors["border"], text_color=("#2D3436", "#ECF0F1"),
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

        progress_row = ctk.CTkFrame(card, fg_color="transparent")
        progress_row.pack(fill="x", padx=40, pady=(5, 15))

        # LEFT SIDE LABEL CONTAINER
        label_frame = ctk.CTkFrame(progress_row, fg_color="transparent")
        label_frame.pack(side="left")
        # Red Star
        ctk.CTkLabel(label_frame, text="*", font=("Inter", 14, "bold"), text_color=self.colors["accent_red"]).pack(side="left")

        progress_label = ctk.CTkLabel(progress_row, text="PROGRESS (%)", font=("Inter", 12, "bold"), text_color=self.colors["text_muted"])
        progress_label.pack(side="left")

        self.progress_entry = ctk.CTkEntry(progress_row, width=170, height=30, corner_radius=8)
        # self.progress_entry.pack(padx=40, pady=(5, 15))
        self.progress_entry.pack(side="right")

        # ERROR LABEL
        self.showerror = ctk.CTkLabel(card, text="", font=("Inter", 10), text_color=self.colors["accent_red"], wraplength=300, justify="right")
        self.showerror.pack(anchor="e", padx=40, pady=(0, 10))

        date_row = ctk.CTkFrame(card, fg_color="transparent")
        date_row.pack(fill="x", padx=40, pady=(0, 15))

        update_date = ctk.CTkLabel(date_row, text="UPDATE DATE", font=("Inter", 12, "bold"), text_color=self.colors["text_muted"])
        update_date.pack(side="left")

        date_frame = ctk.CTkFrame(date_row, fg_color="transparent")
        date_frame.pack(side="right")
        # self.date_picker = DateEntry(date_frame, date_pattern='yyyy-mm-dd', background='#3B82F6', foreground='white')
        # self.date_picker.pack(fill="x", ipady=5)
        self.date_picker = DatePickerButton(date_frame)
        self.date_picker.pack(fill="x")

        create_label("NOTES")
        self.note_box = ctk.CTkTextbox(card, width=320, height=100, corner_radius=8, border_width=1)
        self.note_box.pack(padx=40, pady=(5, 20))

        btn_f = ctk.CTkFrame(card, fg_color="transparent")
        btn_f.pack(fill="x", padx=40, pady=(0, 30))

        self.submit_btn = ctk.CTkButton(
            btn_f, text="💾 Submit", fg_color=self.colors["accent_green"], 
            hover_color="#059669",text_color=("#2D3436", "#ECF0F1"), height=40, corner_radius=8, command=self.submit_report
        )
        self.submit_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))

        cancel_btn = ctk.CTkButton(
            btn_f, text="Cancel", fg_color="transparent", border_width=1, 
            text_color=self.colors["text_main"], height=40, corner_radius=8, command=self.back_to_main
        )
        cancel_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
    
    def apply_date_limits(self, project_id):
         # 1. Fetch project creation date
        self.db.cursor.execute("SELECT created_at FROM projects WHERE id = %s", (project_id,))
        res = self.db.cursor.fetchone()
        
        if res:
            created_at = res['created_at']
            if isinstance(created_at, str):
                created_at = datetime.strptime(created_at, '%Y-%m-%d').date()
            
            # 2. Define the first allowed date
            #first_allowed = created_at + timedelta(days=1)
            first_allowed = created_at
            
            # 3. Use the new method we added to your custom class
            self.date_picker.set_mindate(first_allowed)
            return first_allowed
        return None

    # =========================================================
    # LAYER 3 - PROGRESS HISTORY
    # =========================================================
    def build_history(self):
        for w in self.layer3.winfo_children():
            w.destroy()

        header = ctk.CTkFrame(self.layer3, fg_color="transparent")
        header.pack(fill="x", pady=10)

        ctk.CTkButton(header, text="← Back", width=100, fg_color=self.colors["accent_blue"], hover_color="#2563EB",
                text_color=("#2D3436", "#ECF0F1"),corner_radius=8, command=self.back_from_history).pack(side="left", padx=10)

        ctk.CTkLabel(header, text="Task History", font=("Inter", 24, "bold")).pack(side="left", padx=20)

        container = ctk.CTkScrollableFrame(self.layer3, fg_color="transparent",
                                            scrollbar_button_color="#A0A0A0", # Grey scrollbar
                                            scrollbar_button_hover_color="#808080")
        container.pack(fill="both", expand=True, padx=20, pady=(10, 0))

        self.db.cursor.execute("""
            SELECT * FROM progress_history WHERE task_id=%s ORDER BY update_date DESC, id DESC
        """, (self.current_task['id'],))
        
        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(
                container, text="No history records found.", 
                font=("Inter", 14), text_color=self.colors["text_muted"]
            ).pack(pady=40)
        else:
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

        ctk.CTkButton(btn_f, text="Edit", width=60, fg_color=self.colors["accent_amber"],text_color=("#2D3436", "#ECF0F1"),
                      command=lambda r=row: self.edit_history(r)).pack(side="left", padx=2)
        ctk.CTkButton(btn_f, text="Delete", width=60, fg_color=self.colors["accent_red"],text_color=("#2D3436", "#ECF0F1"),
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
        self.showerror.configure(text="")

        self.apply_date_limits(task['project_id'])
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
        self.showerror.configure(text="")
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

        # update projects table
        self.db.cursor.execute("""
            SELECT project_id FROM tasks WHERE id = %s
        """, (task_id,))
        proj_row = self.db.cursor.fetchone()
        if proj_row and proj_row['project_id']:
            project_id = proj_row['project_id']
            try:
                self.db.cursor.execute("SELECT progress FROM tasks WHERE project_id = %s", (project_id,))
                rows = self.db.cursor.fetchall()
                avg = int(sum(r['progress'] for r in rows) / len(rows)) if (rows and len(rows) > 0) else 0
                status = "Completed" if avg == 100 else "In Progress"
                self.db.cursor.execute("UPDATE projects SET status = %s WHERE id = %s", 
                                       (f"{status} ({avg}%)", project_id))
                self.db.conn.commit()
            except: pass
        

    def submit_report(self):
        try:
            self.showerror.configure(text="")
            # 1. Basic Input Retrieval and Type Validation
            val_str = self.progress_entry.get().strip()
            if not val_str:
                #messagebox.showerror("Error", "Progress field cannot be empty.")
                self.showerror.configure(text="Progress field cannot be empty.")
                return
                
            val = int(val_str)
            note = self.note_box.get("1.0", "end").strip()
            selected_date = self.date_picker.get_date()
            date_str = selected_date.strftime('%Y-%m-%d')

            # 2. Individual Input Range Check (0-100)
            if val < 0 or val > 100:
                #messagebox.showerror("Invalid Range", "Please enter a value between 0 and 100.")
                self.showerror.configure(text="Please enter a value between 0 and 100.")
                return

            # 3. Database State Check (Current Total Progress)
            self.db.cursor.execute("SELECT progress FROM tasks WHERE id = %s", (self.current_task['id'],))
            # Fetching fresh from DB to ensure accuracy
            task_row = self.db.cursor.fetchone()
            current_total = task_row['progress'] if task_row else 0

            # 4. Mode-Specific Validation (Preventing SUM > 100)
            if self.editing_history_id:
                # --- UPDATE MODE ---
                # Get the value of the record we are currently changing
                self.db.cursor.execute("SELECT progress FROM progress_history WHERE id = %s", (self.editing_history_id,))
                history_row = self.db.cursor.fetchone()
                old_val = history_row['progress'] if history_row else 0
                
                # Theoretical New Total = (Total - Old Record) + New Input
                theoretical_total = current_total - old_val + val
                
                if theoretical_total > 100:
                    max_allowed = 100 - (current_total - old_val)
                    #messagebox.showerror("Limit Exceeded", 
                     #   f"Updating this to {val}% would make the task {theoretical_total}% complete.\n"
                      #  f"The maximum value allowed for this specific entry is {max_allowed}%.")
                    self.showerror.configure(text=(
                        f"Updating this to {val}% would make the task {theoretical_total}% complete.\n"
                        f"The maximum value allowed for this specific entry is {max_allowed}%."))
                    return
                
                # Update existing record
                self.db.cursor.execute(""" 
                    UPDATE progress_history 
                    SET progress=%s, note=%s, update_date=%s 
                    WHERE id=%s 
                """, (val, note, date_str, self.editing_history_id))
                messagebox.showinfo("Success", "Progress updated successfully.")
            else:
                # --- INSERT MODE ---

                # ==================================================
                # CHECK SAME DATE HISTORY
                # ==================================================
                self.db.cursor.execute("""
                    SELECT id, progress
                    FROM progress_history
                    WHERE task_id = %s
                    AND update_date = %s
                """, (
                    self.current_task['id'],
                    date_str
                ))

                existing_row = self.db.cursor.fetchone()

                 # ==================================================
                # IF SAME DATE EXISTS -> UPDATE
                # ==================================================
                if existing_row:

                    existing_id = existing_row['id']

                    self.db.cursor.execute("SELECT progress FROM progress_history WHERE id = %s", (existing_id,))
                    history_row = self.db.cursor.fetchone()
                    old_val = history_row['progress'] if history_row else 0

                    theoretical_total = current_total - old_val + val

                    if theoretical_total > 100:
                        max_allowed = 100 - (current_total - old_val)
                        # messagebox.showerror("Limit Exceeded", 
                        #     f"Updating this to {val}% would make the task {theoretical_total}% complete.\n"
                        #     f"The maximum value allowed for this specific entry is {max_allowed}%.")
                        self.showerror.configure(text=(
                            f"Updating this to {val}% would make the task {theoretical_total}% complete.\n"
                            f"The maximum value allowed for this specific entry is {max_allowed}%."
                        ))
                        return
    

                    self.db.cursor.execute("""
                        UPDATE progress_history
                        SET
                            progress = %s,
                            note = %s
                        WHERE id = %s
                    """, (
                        val,
                        note,
                        existing_id
                    ))

                    messagebox.showinfo(
                        "Updated",
                        f"Existing history for {date_str} updated successfully."
                    )

                # ==================================================
                # IF DATE DOES NOT EXIST -> INSERT
                # ==================================================
                else:

                    if current_total + val > 100:
                        remaining = 100 - current_total
                        # messagebox.showerror("Limit Exceeded", 
                        #     f"Task is already {current_total}% complete.\n"
                        #     f"You can only add a maximum of {remaining}% more.")
                        self.showerror.configure(text=(
                            f"Task is already {current_total}% complete.\n"
                            f"You can only add a maximum of {remaining}% more."
                        ))
                        return

                    self.db.cursor.execute("""
                        INSERT INTO progress_history (
                            task_id,
                            project_id,
                            member_name,
                            progress,
                            note,
                            update_date
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        self.current_task['id'],
                        self.current_task['project_id'],
                        self.user['full_name'],
                        val,
                        note,
                        date_str
                    ))

                    messagebox.showinfo(
                        "Success",
                        "New history record added successfully."
                    )

                # # Insert new record
                # self.db.cursor.execute(""" 
                #     INSERT INTO progress_history (task_id, project_id, member_name, progress, note, update_date) 
                #     VALUES (%s, %s, %s, %s, %s, %s) 
                # """, (self.current_task['id'], self.current_task['project_id'], self.user['full_name'], val, note, date_str))

            # 6. Synchronization and UI Refresh
            # Recalculate task and project table progress values
            self.update_task_progress(self.current_task['id'])
            self.db.conn.commit()
            
            # messagebox.showinfo("Success", "Progress updated successfully.")

            # Determine where to send the user back to
            if self.editing_history_id:
                # Reset state and return to history list
                self.editing_history_id = None 
                self.open_history(self.current_task)
            else:
                # Return to main dashboard and refresh list
                self.back_to_main()
                self.refresh_tasks()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid whole number for progress.")
        except Exception as e:
            print(f"Database Error: {e}")
            messagebox.showerror("Error", f"A database error occurred: {e}")

    def delete_history(self, row):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            self.db.cursor.execute("DELETE FROM progress_history WHERE id=%s", (row['id'],))
            self.update_task_progress(self.current_task['id'])
            self.db.conn.commit()
            messagebox.showinfo("Deleted", "History record deleted successfully.")
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