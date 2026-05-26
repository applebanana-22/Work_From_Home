import customtkinter as ctk
from database import Database
from tkinter import messagebox
from tkcalendar import DateEntry  # Required for calendar selector
from tkinter import ttk # for calendar styling
from datetime import datetime, timedelta
from tkcalendar import Calendar
import calendar

class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None):
        super().__init__(master, fg_color="transparent")

        today = datetime.today().date()
        tomorrow = today + timedelta(days=1)
        if initial_date and initial_date > today:
            self._date = initial_date
        else:
            self._date = tomorrow

        self._open = False

        # -------- STYLE --------
        style = ttk.Style()
        style.theme_use("clam")

        appearance = ctk.get_appearance_mode()
        if appearance == "Light":
            cal_bg = "#FFFFFF"
            cal_fg = "black"
            h_bg = "#EAECEE"
            h_fg = "#2471A3"
        else:
            cal_bg = "#1A1A2E"
            cal_fg = "white"
            h_bg = "#16213E"
            h_fg = "#4FC3F7" 

        style.configure("Custom.Calendar",
            background=cal_bg,
            foreground=cal_fg,
            headersbackground=h_bg,
            headersforeground=h_fg,
            selectbackground="#3498DB",
            selectforeground="white",
            normalbackground=cal_bg,
            normalforeground=cal_fg,
            weekendbackground=cal_bg,
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
            height=34, # Perfectly aligned baseline height
            corner_radius=10,
            fg_color=("#EAECEE", "#1E2A3A"),
            hover_color=("#D5D8DC", "#2C3E50"),
            border_width=1,
            border_color=("#ABB2B9", "#3D5166"),
            text_color=("#475569", "#8899AA"),
            anchor="w",
            command=self.toggle
        )
        self.btn.pack()

        # -------- FLOATING PANEL --------
        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color=("#FFFFFF", "#141E2B"),
            corner_radius=12,
            border_width=1,
            border_color=("#ABB2B9", "#2A3A4A")
        )

        # -------- REAL CALENDAR --------
        self.cal = Calendar(
            self.panel,
            style="Custom.Calendar",
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            mindate = tomorrow,
            year=self._date.year,
            month=self._date.month,
            day=self._date.day,
            showweeknumbers=False,
            firstweekday="monday",
            font=("Arial", 11),
            cursor="hand2"
        )
        self.cal.pack(padx=8, pady=8)

        self.cal.bind("<<CalendarSelected>>", self._select)

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
        today = datetime.today().date()
        tomorrow = today + timedelta(days=1)

        if d < tomorrow:
            d = tomorrow
        self._date = d
        self.cal.selection_set(d)
        self.btn.configure(text=self._fmt())


class TaskManager(ctk.CTkFrame):
    def __init__(self, master, project_id, project_name, user, back_callback):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.project_id = project_id
        self.project_name = project_name
        self.user = user
        self.back_callback = back_callback

        #_____________state declare_____________
        self.form_visible = False
        self.mode = "add"
        self.editing_task_id = None
            
        # --- Header ---
        self.header_f = ctk.CTkFrame(self, fg_color="transparent")
        self.header_f.pack(fill="x", padx=80, pady=15)

        ctk.CTkButton(self.header_f, text="← Back", width=80, fg_color=("#DBDBDB", "#333333"),
         text_color=("black", "white"), corner_radius=8,
         command=self.back_callback).pack(side="left", padx=10)

        ctk.CTkLabel(self.header_f, text=f"Project: {project_name}", 
                     font=("Arial", 22, "bold")).pack(side="left")

        self.overall_lbl = ctk.CTkLabel(self.header_f, text="Overall: 0%", 
                                        font=("Arial", 18, "bold"), text_color="#10B981")
        self.overall_lbl.pack(side="right", padx=10)

        # Fetch layout status restriction details
        sql = "SELECT * FROM projects WHERE id = %s ORDER BY id DESC"
        self.db.cursor.execute(sql, (self.project_id,))
        projects = self.db.cursor.fetchone()

        is_complete = 1 if "100" in projects['status'] else 0

        # =========================================================
        # CONTROL WRAPPER (SEARCH + BUTTON + FORM)
        # =========================================================
        self.control_wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self.control_wrapper.pack(fill="x", padx=80, pady=5)

        # ---------------- SEARCH (always visible) ----------------
        self.search_entry = ctk.CTkEntry(
            self.control_wrapper,
            placeholder_text="🔍 Search...",
            width=200
        )
        self.search_entry.pack(side="left", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_tasks())

        # ---------------- TOGGLE BUTTON ----------------
        self.toggle_form_btn = ctk.CTkButton(
            self.control_wrapper,
            text="+ Add Task",
            state = "disabled" if is_complete else "normal",
            fg_color="#10B981" if not is_complete else "grey",
            width=140, height=36,
            hover_color="#059669",
            command=self.toggle_form
        )
        self.toggle_form_btn.pack(side="left", padx=10)

        # =========================================================
        # COMBINED SHARED INLINE FORM (ADD & EDIT IN ONE PLACE)
        # =========================================================
        self.control_f = ctk.CTkFrame(self, fg_color=("#EAEAEA", "#1E1E1E"), corner_radius=12)

        # Single Flat Row Container (Ensures layout alignment)
        form_row = ctk.CTkFrame(self.control_f, fg_color="transparent")
        form_row.pack(fill="x", padx=20, pady=(20, 5))

        # --- Input 1: Task Entry Box ---
        ctk.CTkLabel(form_row, text="Task Name", font=("Arial", 12, "bold")).pack(side="left", anchor="center")
        ctk.CTkLabel(form_row, text="*", text_color="red", font=("Arial", 16, "bold")).pack(side="left", padx=(0, 5), anchor="center")
        
        self.task_entry = ctk.CTkEntry(form_row, placeholder_text="Task Name", width=160, height=34)
        self.task_entry.pack(side="left", padx=(0, 15), fill="x", anchor="center")

        # --- Input 2: Deadline Dropdown Picker ---
        ctk.CTkLabel(form_row, text="Deadline: ", font=("Arial", 12, "bold")).pack(side="left", padx=(0, 5), anchor="center")
        self.deadline_picker = DatePickerButton(
            form_row,
            initial_date=datetime.today().date() + timedelta(days=1)
        )
        self.deadline_picker.pack(side="left", padx=(0, 15), anchor="center")

        # --- Input 3: Team Dropdown Menu ---
        ctk.CTkLabel(form_row, text="Member", font=("Arial", 12, "bold")).pack(side="left", anchor="center")
        ctk.CTkLabel(form_row, text="*", text_color="red", font=("Arial", 16, "bold")).pack(side="left", padx=(0, 5), anchor="center")

        members = self.get_team_members()
        self.member_dropdown = ctk.CTkOptionMenu(
            form_row,
            values=members if members else ["No Member"],
            width=150,
            height=34
        )
        self.member_dropdown.set("Select Member")
        self.member_dropdown.pack(side="left", padx=(0, 15), anchor="center")

        # --- Form Row Interactive Submission Button ---
        self.action_btn = ctk.CTkButton(
            form_row,
            text="Add",
            fg_color="#10B981",
            hover_color="#059669",
            width=60,
            height=30,
            font=("Arial", 12, "bold"),
            text_color=("#2D3436", "#ECF0F1"),
            command=self.add_task_with_confirm
        )
        self.action_btn.pack(side="left", anchor="center")

        # --- Inline Error Diagnostic Outputs ---
        error_row = ctk.CTkFrame(self.control_f, fg_color="transparent")
        error_row.pack(fill="x", padx=20, pady=(0, 15))

        self.task_error = ctk.CTkLabel(error_row, text="", text_color="red", font=("Arial", 11))
        self.task_error.pack(side="left", padx=(80, 0))

        self.member_error = ctk.CTkLabel(error_row, text="", text_color="#EF4444", font=("Arial", 11))
        self.member_error.pack(side="left", padx=(360, 0))

        # =========================================================
        # TASK CARDS SCROLL LIST FRAME
        # =========================================================
        self.list_frame = ctk.CTkScrollableFrame(
            self,
            label_text="Task Breakdown",
            fg_color=("#F5F5F5", "#121212")
        )
        self.list_frame.pack(fill="both", expand=True, padx=80, pady=10)

        self.refresh_tasks()


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
        message_frame.place(relx=1.0, rely=0, x=-20, y=70, anchor="ne")
         
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
            self.control_f.pack_forget()
            self.form_visible = False
            self.toggle_form_btn.configure(text="+ Add Task")
        else:
            self.list_frame.pack_forget()
            self.control_f.pack(fill="x", padx=80, pady=5)
            self.list_frame.pack(fill="both", expand=True, padx=80, pady=10)
            
            self.form_visible = True
            self.toggle_form_btn.configure(text="✖ Close")
            self.set_mode("add")
            self.task_error.configure(text="")
            self.member_error.configure(text="")

    def set_mode(self, mode, task_id=None):
        self.mode = mode
        self.editing_task_id = task_id

        if mode == "add":
            self.action_btn.configure(
                text="Add",
                fg_color="#10B981",
                hover_color="#059669",
                command=self.add_task_with_confirm
            )
        elif mode == "edit":
            self.action_btn.configure(
                text="Update",
                fg_color="#F39C12",
                hover_color="#D68910",
                command=self.save_edit_task
            )

    def reset_form(self):
        self.mode = "add"
        self.editing_task_id = None
        self.task_error.configure(text="")
        self.member_error.configure(text="")
        self.task_entry.delete(0, "end")
        self.member_dropdown.set("Select Member")
        tomorrow = datetime.today().date() + timedelta(days=1)
        self.deadline_picker.set_date(tomorrow)

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
                ctk.CTkLabel(info_f, text=row['task_name'], font=("Arial", 15, "bold")).pack(anchor="w")
                ctk.CTkLabel(info_f, text=f"👤 Assigned to: {row['assigned_to']}\n📅 Deadline: {deadline}", 
                             font=("Arial", 13), text_color="gray").pack(anchor="w")

                actions_f = ctk.CTkFrame(card, fg_color="transparent")
                actions_f.pack(side="right", padx=10)

                p_val = row['progress']
                color = self.get_status_color(p_val)
                ctk.CTkLabel(actions_f, text=f"{p_val}%", font=("Arial", 14, "bold"), 
                             text_color=color, width=50).pack(side="right", padx=15)

                is_complete = 1 if row['progress'] == 100 else 0

                # Edit Button (Triggers your original inline loading sequence!)
                ctk.CTkButton(actions_f, text="Edit", state = "disabled" if is_complete else "normal", width=60, height=30,
                              fg_color="#F39C12" if not is_complete else "grey", hover_color="#D35400", font=("Arial", 12), text_color=("#2D3436", "#ECF0F1"),
                              command=lambda r=row: self.start_edit_task(r)).pack(side="left", padx=5)

                # Delete Button
                ctk.CTkButton(actions_f, text="Delete", state = "disabled" if is_complete else "normal", width=60, height=30,
                              fg_color="#C0392B" if not is_complete else "grey", hover_color="#A93226", text_color=("#2D3436", "#ECF0F1"),
                              command=lambda tid=row['id']: self.delete_task_with_confirm(tid)).pack(side="left", padx=5)
                
                # History Button
                ctk.CTkButton(actions_f, text="History", width=60, height=30,
                                fg_color="#2980B9", text_color=("#2D3436", "#ECF0F1"),
                                command=lambda tid=row['id']: self.view_history(tid)).pack(side="left", padx=5)
                
            self.calculate_project_progress()
        except Exception as e: 
            self._show_message(f"Refresh Error: {e}", "error")

    def start_edit_task(self, row):
        """SUCCESSFULLY RESTORED INLINE LOGIC MODE CHANGING CODE ✅"""
        self.task_error.configure(text="")
        self.member_error.configure(text="")

        if not self.form_visible:
            self.toggle_form()

        # Switches button function mappings over to update queries instead
        self.set_mode("edit", row["id"])

        # Inject existing database variables clean back into your inline view inputs
        self.task_entry.delete(0, "end")
        self.task_entry.insert(0, row["task_name"])
        self.member_dropdown.set(row["assigned_to"])

        try:
            d = datetime.strptime(str(row["deadline"]), "%Y-%m-%d").date()
        except:
            d = datetime.today().date()
        
        self.deadline_picker.set_date(d)

    def save_edit_task(self):
        self.task_error.configure(text="")
        self.member_error.configure(text="")
        try:
            name = self.task_entry.get().strip()
            member = self.member_dropdown.get()
            deadline = self.deadline_picker.get_date().strftime('%Y-%m-%d')

            has_error = False
            if not name:
                self.task_error.configure(text="Please enter task name")
                has_error = True
            
            if member in ["Select Member", "No Member"]:
                self.member_error.configure(text="Please select a member")
                has_error = True

            if has_error: return

            sql = "UPDATE tasks SET task_name=%s, assigned_to=%s, deadline=%s WHERE id=%s"
            self.db.cursor.execute(sql, (name, member, deadline, self.editing_task_id))
            self.db.conn.commit()
            
            self.refresh_tasks()
            self.reset_form()
            self.toggle_form()
            self._show_message("Task updated successfully!", "success")
        except Exception as e:
            self._show_message(f"Update Error: {str(e)}", "error")

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
        self.task_error.configure(text="")
        self.member_error.configure(text="")

        name = self.task_entry.get().strip()
        member = self.member_dropdown.get()
        deadline = self.deadline_picker.get_date().strftime('%Y-%m-%d')
        
        has_error = False
        if not name:
            self.task_error.configure(text="Task name is required")
            has_error = True

        if member in ["Select Member", "No Member"]:
            self.member_error.configure(text="Please select member")
            has_error = True

        if has_error: return

        if messagebox.askyesno("Confirm", f"Do you want to assign task '{name}' to {member} with a deadline of {deadline}?", parent=self):
            try:
                sql = "INSERT INTO tasks (project_id, task_name, assigned_to, deadline, progress) VALUES (%s, %s, %s, %s, 0)"
                self.db.cursor.execute(sql, (self.project_id, name, member, deadline))
                self.db.conn.commit()
                self.refresh_tasks()
                self.reset_form()
                self.toggle_form()
                self._show_message("Task added successfully!", "success")
            except Exception as e: 
                self._show_message(f"Database Error: {e}", "error")

    def delete_task_with_confirm(self, task_id):
        if messagebox.askyesno("Confirm Delete", "Permanently delete this task?", parent=self): 
            try:
                self.db.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                self.db.conn.commit()
                self.refresh_tasks()
                self._show_message("Task deleted completely.", "success")
            except Exception as e: 
                self._show_message(f"Error: {e}", "error")
        
    def view_history(self, task_id):
        win = ctk.CTkToplevel(self)
        win.title("Progress History")
        width, height = 500, 400

        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        win.geometry(f"{width}x{height}+{x}+{y}")
        
        win.transient(self)
        win.lift()
        win.attributes("-topmost", True)
        win.grab_set()
        
        ctk.CTkLabel(win, text="📊 Progress History", font=("Arial", 18, "bold")).pack(pady=10)

        try:
            self.db.cursor.execute("""
                SELECT * FROM progress_history 
                WHERE task_id = %s ORDER BY update_date DESC
            """, (task_id,))   
            rows = self.db.cursor.fetchall()

            frame = ctk.CTkScrollableFrame(win)
            frame.pack(fill="both", expand=True, padx=10, pady=10)      

            if rows:
                member_name = rows[0]["member_name"]
                if member_name:
                    ctk.CTkLabel(win, text=f"👤 {member_name}", font=("Arial", 14, "bold")).pack(pady=(0,10))
          
            header = ctk.CTkFrame(frame, fg_color="transparent")
            header.pack(fill="x", padx=15, pady=(5,5))

            ctk.CTkLabel(header, text="Date", width=120, font=("Arial", 13, "bold")).pack(side="left")
            ctk.CTkLabel(header, text="Progress", width=80, font=("Arial", 13, "bold")).pack(side="left")
            ctk.CTkLabel(header, text="Note", font=("Arial", 13, "bold")).pack(side="left")

            ctk.CTkFrame(frame, height=2, fg_color="gray").pack(fill="x", padx=15, pady=5)

            if not rows:
                ctk.CTkLabel(frame, text="No history yet", font=("Arial", 18, "bold")).pack(pady=20)
            else:
                for i, record in enumerate(rows):
                    bg = "#2b2b2b" if i % 2 == 0 else "transparent"
                    row = ctk.CTkFrame(frame, fg_color=bg)
                    row.pack(fill="x", padx=15, pady=2)

                    ctk.CTkLabel(row, text=str(record["update_date"]), width=120, anchor="w").pack(side="left")
                    ctk.CTkLabel(row, text=f'{record["progress"]}%', width=80, anchor="w").pack(side="left")
                    note_text = record["note"] if record["note"] else "-"
                    ctk.CTkLabel(row, text=note_text, anchor="w").pack(side="left")               
        except Exception as e:
            self._show_message(f"History tracking failure: {e}", "error")