import re
import customtkinter as ctk
from database import Database
from tkinter import messagebox

class UserRegisterFrame(ctk.CTkFrame):
    """The Registration Form UI - Handles dynamic visibility and auto-increment ID"""
    def __init__(self, parent, db, back_callback):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self.back_callback = back_callback
        
        # --- Top Navigation ---
        self.nav_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_bar.pack(fill="x", padx=20, pady=10)
        
        self.back_btn = ctk.CTkButton(
            self.nav_bar, text="← Back to Users", width=100,
            fg_color="#4A4A4A", hover_color="#333333",
            command=self.back_callback
        )
        self.back_btn.pack(side="left")

        ctk.CTkLabel(self, text="Register New Account", font=("Arial", 22, "bold")).pack(pady=15)

        # Form Container
        self.main_container = ctk.CTkFrame(
            self, 
            fg_color=("#F9F9F9", "#252525"), # <--- Light mode: Light Grey | Dark mode: Dark Grey
            border_width=1, 
            border_color=("#DBDBDB", "#333333"), # <--- Added borders so it stands out in Light Mode
            corner_radius=10
        )
        self.main_container.pack(fill="both", expand=True, padx=100, pady=(10, 40))

        # --- The Grid Form ---
        self.f = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.f.pack(expand=True, padx=50, pady=30)
        
        self.f.grid_columnconfigure(0, weight=1, minsize=150)
        self.f.grid_columnconfigure(1, weight=1)

        # 1. Employee ID (Auto-generated & Disabled)
        ctk.CTkLabel(self.f, text="Employee ID:", font=("Arial", 13)).grid(row=0, column=0, padx=15, pady=10, sticky="e")
        self.emp_id = ctk.CTkEntry(self.f, height=40, width=400, fg_color="#a59d9d")
        self.emp_id.grid(row=0, column=1, padx=15, pady=10, sticky="w")
        
        next_id = self.get_next_emp_id()
        self.emp_id.insert(0, str(next_id))
        self.emp_id.configure(state="disabled")

        # 2. Full Name
        ctk.CTkLabel(self.f, text="Full Name:", font=("Arial", 13)).grid(row=1, column=0, padx=15, pady=10, sticky="e")
        self.name = ctk.CTkEntry(self.f, height=40, width=400)
        self.name.grid(row=1, column=1, padx=15, pady=10, sticky="w")

        # 3. Username
        ctk.CTkLabel(self.f, text="Username:", font=("Arial", 13)).grid(row=2, column=0, padx=15, pady=10, sticky="e")
        self.uname = ctk.CTkEntry(self.f, height=40, width=400)
        self.uname.grid(row=2, column=1, padx=15, pady=10, sticky="w")

        # 4. Password
        ctk.CTkLabel(self.f, text="Password:", font=("Arial", 13)).grid(row=3, column=0, padx=15, pady=10, sticky="e")
        self.pwd = ctk.CTkEntry(self.f, height=40, width=400, show="*")
        self.pwd.grid(row=3, column=1, padx=15, pady=10, sticky="w")

        # 5. Role Selection
        ctk.CTkLabel(self.f, text="User Role:", font=("Arial", 13)).grid(row=4, column=0, padx=15, pady=10, sticky="e")
        self.role = ctk.CTkOptionMenu(
            self.f, 
            values=["Choose Role", "admin", "leader", "member"],
            height=40, width=400,
            command=self.update_ui_by_role
        )
        self.role.grid(row=4, column=1, padx=15, pady=10, sticky="w")
        self.role.set("Choose Role")

        # 6. Team Selection (Hidden by default until role is chosen)
        self.team_label = ctk.CTkLabel(self.f, text="Assign Team:", font=("Arial", 13))
        
        teams_data = self.db.get_all_teams()
        self.team_map = {t['team_name']: t['team_id'] for t in teams_data}
        team_options = ["Choose Team"] + list(self.team_map.keys()) if self.team_map else ["Choose Team", "No Teams Found"]
        self.team_dropdown = ctk.CTkOptionMenu(self.f, values=team_options, height=40, width=400)
        self.team_dropdown.set("Choose Team")

        # 7. Batch Selection (Hidden by default)
        self.batch_label = ctk.CTkLabel(self.f, text="Batch Number:", font=("Arial", 13))
        self.batch = ctk.CTkEntry(self.f, height=45, width=400)

        # 8. Save Button
        self.save_btn = ctk.CTkButton(self.f, text="Register", width=150, height=40, fg_color="#10B981", command=self.save_user)
        self.save_btn.grid(row=10, column=0, columnspan=2, pady=30)

    def get_next_emp_id(self):
        try:
            self.db.cursor.execute("SELECT MAX(CAST(employee_id AS UNSIGNED)) as max_id FROM users")
            result = self.db.cursor.fetchone()
            return (int(result['max_id']) + 1) if result and result['max_id'] else 1001
        except:
            return 1001

    def update_ui_by_role(self, choice):
        """Hides/Shows fields based on Role"""
        # Hide everything dynamic first
        self.batch_label.grid_forget()
        self.batch.grid_forget()
        self.team_label.grid_forget()
        self.team_dropdown.grid_forget()

        if choice == "leader":
            self.team_label.grid(row=5, column=0, padx=15, pady=10, sticky="e")
            self.team_dropdown.grid(row=5, column=1, padx=15, pady=10, sticky="w")
        elif choice == "member":
            self.team_label.grid(row=5, column=0, padx=15, pady=10, sticky="e")
            self.team_dropdown.grid(row=5, column=1, padx=15, pady=10, sticky="w")
            self.batch_label.grid(row=6, column=0, padx=15, pady=10, sticky="e")
            self.batch.grid(row=6, column=1, padx=15, pady=10, sticky="w")
        # 'admin' remains with them hidden

    def validate_inputs(self):
        full_name = self.name.get().strip()
        username = self.uname.get().strip()
        password = self.pwd.get().strip()
        role_val = self.role.get()
        batch_val = self.batch.get().strip()

        if not all([full_name, username, password]): 
            return False, "All core fields are required!"
        if full_name.isdigit():
            return False, "Full Name cannot be numeric."
        if len(full_name) < 2:
            return False, "Full Name is too short."
        if username.isdigit():
            return False, "User Name cannot be numeric."
        if " " in username:
            return False, "Username cannot contain spaces."
        if len(username) < 4:
            return False, "Username must be at least 4 characters."
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"\d", password):
            return False, "Password must contain uppercase, lowercase, and a number."
        if len(password) > 20:
            return False, "Password is too long."
        if role_val == "Choose Role":
            return False, "Please select a valid User Role."
        if role_val != "admin":
            if self.team_dropdown.get() == "Choose Team":
                return False, "Please select a valid Team."
       
        batch_val = self.batch.get().strip()
 
        # 1. Basic empty check for core fields
        if not all([full_name, username, password]):          
            return False, "All fields are required!"
 
        # ... (other validations)
 
        # 2. Batch Number specific validation
        if batch_val:
            # Check if it contains ONLY numbers
            if not batch_val.isdigit():
                return False, "Batch Number must contain only numbers (no letters or characters)."
           
            # Check range
            if int(batch_val) < 1 or int(batch_val) > 100:
                return False, "Batch Number must be between 1 and 100."
       
        # 3. Required check for members
        if role_val == "member" and not batch_val:
            return False, "Batch Number is required for members."
        return True, "Success"

    def save_user(self):
        is_valid, msg = self.validate_inputs()
        if not is_valid:
            messagebox.showwarning("Validation Error", msg)
            return

        role_val = self.role.get()
        # Admin gets no team, others get selected team
        team_id = self.team_map.get(self.team_dropdown.get()) if role_val != "admin" else None
        
        # Batch formatting
        batch_input = self.batch.get().strip()
        formatted_batch = f"Batch {batch_input}" if (role_val == "member" and batch_input) else "N/A"

        try:
            sql = """INSERT INTO users (employee_id, full_name, username, password, role, team_id, batch) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            data = (
                self.emp_id.get(), 
                self.name.get().strip(), 
                self.uname.get().strip(), 
                self.pwd.get(), 
                role_val, 
                team_id, 
                formatted_batch
            )
            self.db.cursor.execute(sql, data)
            self.db.conn.commit()
            messagebox.showinfo("Success", f"User {self.name.get()} created successfully!")
            self.back_callback()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
            
class UserUpdateFrame(ctk.CTkFrame):
    """The Update Form UI - Pre-fills data and updates existing records"""
    def __init__(self, parent, db, user_id, back_callback):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self.user_id = user_id
        self.back_callback = back_callback
        
        # --- UI Setup ---
        self.nav_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_bar.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(self.nav_bar, text="← Back", width=100,
                      fg_color="#4A4A4A", command=self.back_callback).pack(side="left")

        ctk.CTkLabel(self, text="Update User Account",
                     font=("Arial", 22, "bold")).pack(pady=15)

        self.main_container = ctk.CTkFrame(
        self, 
            fg_color=("#F9F9F9", "#252525"), # <--- Light mode: Light Grey | Dark mode: Dark Grey
            border_width=1, 
            border_color=("#DBDBDB", "#333333"), # <--- Added borders so it stands out in Light Mode
            corner_radius=10
        )
        self.main_container.pack(fill="both", expand=True, padx=100, pady=(10, 40))

        self.f = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.f.pack(expand=True, padx=50, pady=30)

        # --- Fields ---
        ctk.CTkLabel(self.f, text="Full Name:").grid(row=0, column=0, padx=15, pady=10, sticky="e")
        self.name = ctk.CTkEntry(self.f, height=40, width=400)
        self.name.grid(row=0, column=1, padx=15, pady=10)

        ctk.CTkLabel(self.f, text="Username:").grid(row=1, column=0, padx=15, pady=10, sticky="e")
        self.uname = ctk.CTkEntry(self.f, height=40, width=400)
        self.uname.grid(row=1, column=1, padx=15, pady=10)

        ctk.CTkLabel(self.f, text="User Role:").grid(row=2, column=0, padx=15, pady=10, sticky="e")
        self.role = ctk.CTkOptionMenu(
            self.f,
            values=["admin", "leader", "member"],
            height=40,
            width=400,
            command=self.update_ui_by_role
        )
        self.role.grid(row=2, column=1, padx=15, pady=10)

        # --- Team ---
        self.team_label = ctk.CTkLabel(self.f, text="Team:")
        self.team_dropdown = ctk.CTkOptionMenu(self.f, values=[], height=40, width=400)

        # --- Batch ---
        self.batch_label = ctk.CTkLabel(self.f, text="Batch:")
        self.batch = ctk.CTkEntry(self.f, height=40, width=400)

        # --- Load Teams ---
        teams_data = self.db.get_all_teams()
        self.team_map = {t['team_name']: t['team_id'] for t in teams_data}
        team_options = ["Select Team"] + list(self.team_map.keys()) if self.team_map else ["No Teams"]
        self.team_dropdown.configure(values=team_options)
        self.team_dropdown.set("Select Team")  # ✅ FIXED DEFAULT

        # --- Button ---
        self.update_btn = ctk.CTkButton(
            self.f, text="Save Changes",
            fg_color="#166DBF",
            command=self.perform_update
        )
        self.update_btn.grid(row=6, column=0, columnspan=2, pady=30)

        self.load_user_data()

    def update_ui_by_role(self, role):
        """Show/hide fields dynamically"""
        self.team_label.grid_forget()
        self.team_dropdown.grid_forget()
        self.batch_label.grid_forget()
        self.batch.grid_forget()
        
        

        if role == "leader":
            self.team_label.grid(row=3, column=0, padx=15, pady=10, sticky="e")
            self.team_dropdown.grid(row=3, column=1, padx=15, pady=10)

        elif role == "member":
            self.team_label.grid(row=3, column=0, padx=15, pady=10, sticky="e")
            self.team_dropdown.grid(row=3, column=1, padx=15, pady=10)

            self.batch_label.grid(row=4, column=0, padx=15, pady=10, sticky="e")
            self.batch.grid(row=4, column=1, padx=15, pady=10)

    def load_user_data(self):
        self.db.cursor.execute("SELECT * FROM users WHERE id=%s", (self.user_id,))
        user = self.db.cursor.fetchone()

        if user:
            self.name.insert(0, user['full_name'])
            self.uname.insert(0, user['username'])
            self.role.set(user['role'])

            self.update_ui_by_role(user['role'])

            if user['team_id']:
                for name, tid in self.team_map.items():
                    if tid == user['team_id']:
                        self.team_dropdown.set(name)

            if user['batch'] and user['batch'] != "N/A":
                self.batch.insert(0, user['batch'].replace("Batch ", ""))

    def perform_update(self):
        try:
            role = self.role.get()
            team_name = self.team_dropdown.get()
            batch_input = self.batch.get().strip()

            # ✅ VALIDATION
            if role != "admin":
                if team_name == "Select Team" or team_name not in self.team_map:
                    messagebox.showwarning("Validation Error", "Please select a valid Team.")
                    return

            if role == "member":
                if not batch_input:
                    messagebox.showwarning("Validation Error", "Batch Number is required for members.")
                    return

                if not batch_input.isdigit():
                    messagebox.showwarning("Validation Error", "Batch must be numeric.")
                    return

                if int(batch_input) < 1 or int(batch_input) > 100:
                    messagebox.showwarning("Validation Error", "Batch must be between 1 and 100.")
                    return

            # ✅ PROCESS
            team_id = self.team_map.get(team_name) if role != "admin" else None
            batch_val = f"Batch {batch_input}" if role == "member" else "N/A"

            sql = """
            UPDATE users 
            SET full_name=%s, username=%s, role=%s, team_id=%s, batch=%s 
            WHERE id=%s
            """

            val = (
                self.name.get().strip(),
                self.uname.get().strip(),
                role,
                team_id,
                batch_val,
                self.user_id
            )

            self.db.cursor.execute(sql, val)
            self.db.conn.commit()

            messagebox.showinfo("Success", "User updated successfully!")
            self.back_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            
            
class AdminUsers(ctk.CTkFrame):
    """Main User Management View"""
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user_data
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.show_list_view()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_list_view(self):
        self.clear_container()
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=100, pady=20)
        
        ctk.CTkLabel(header, text="User Management", font=("Arial", 24, "bold")).pack(side="left")
        
        # --- FILTER BAR ---
        filter_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        filter_frame.pack(fill="x", padx=100, pady=(0, 10))

        self.search_id = ctk.CTkEntry(filter_frame, placeholder_text="Employee ID", width=120)
        self.search_id.pack(side="left", padx=5)

        self.search_name = ctk.CTkEntry(filter_frame, placeholder_text="Full Name", width=150)
        self.search_name.pack(side="left", padx=5)

        self.search_role = ctk.CTkOptionMenu(
            filter_frame,
            values=["All", "admin", "leader", "member"],
            width=120
        )
        self.search_role.set("All")
        self.search_role.pack(side="left", padx=5)

        teams = ["All"] + self.get_team_names()
        self.search_team = ctk.CTkOptionMenu(filter_frame, values=teams, width=120)
        self.search_team.set("All")
        self.search_team.pack(side="left", padx=5)

        self.search_batch = ctk.CTkEntry(filter_frame, placeholder_text="Batch", width=100)
        self.search_batch.pack(side="left", padx=5)

        ctk.CTkButton(filter_frame, text="Filter", width=90, command=self.filter_users).pack(side="left", padx=5)
        ctk.CTkButton(filter_frame, text="Reset", fg_color="#6B7280", width=90, command=self.reset_filters).pack(side="left", padx=5)
        
        ctk.CTkButton(
            header, text="+ Create Account", 
            fg_color="#10B981", height=38, 
            command=self.show_register_view
        ).pack(side="right")
        
        self.list_frame = ctk.CTkScrollableFrame(self.container, label_text="Our Members",label_font=("Arial", 16, "bold"), label_text_color=("#0E0E0E", "#AAAAAA"), fg_color=("#FFFFFF", "#181818"), border_width=1, border_color=("#E0E0E0", "#2B2B2B"))
        self.list_frame.pack(fill="both", expand=True, padx=100, pady=10)
        self.refresh_list()

    def show_register_view(self):
        self.clear_container()
        reg_form = UserRegisterFrame(self.container, self.db, self.show_list_view)
        reg_form.pack(fill="both", expand=True)
        
    def get_team_names(self):
        self.db.cursor.execute("SELECT team_name FROM teams")
        return [t['team_name'] for t in self.db.cursor.fetchall()]

    def refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        sql = """
        SELECT u.*, t.team_name 
        FROM users u 
        LEFT JOIN teams t ON u.team_id = t.team_id 
        ORDER BY u.id DESC
        """
        self.db.cursor.execute(sql)
        rows = self.db.cursor.fetchall()

        # --- TABLE HEADER ---
        headers = ["Employee ID", "Full Name", "Role", "Team", "Batch", "Actions"]

        for col, header in enumerate(headers):
            ctk.CTkLabel(
                self.list_frame,
                text=header,
                font=("Arial", 13, "bold")
            ).grid(row=0, column=col, padx=10, pady=10, sticky="w")

        # --- TABLE ROWS ---
        for i, row in enumerate(rows, start=1):
            emp_id = row['employee_id']
            name = row['full_name']
            role = row['role']
            team = row['team_name'] if row['team_name'] else "No Team"
            batch = row['batch'] if row['batch'] else "N/A"

            ctk.CTkLabel(self.list_frame, text=emp_id).grid(row=i, column=0, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(self.list_frame, text=name).grid(row=i, column=1, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(self.list_frame, text=role).grid(row=i, column=2, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(self.list_frame, text=team).grid(row=i, column=3, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(self.list_frame, text=batch).grid(row=i, column=4, padx=10, pady=8, sticky="w")

            # --- ACTION BUTTONS ---
            btn_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            btn_frame.grid(row=i, column=5, padx=10, pady=5)

            ctk.CTkButton(
                btn_frame, text="Update", width=70, height=28,
                fg_color="#166DBF",
                command=lambda uid=row['id']: self.handle_update(uid)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                btn_frame, text="Delete", width=70, height=28,
                fg_color="#C0392B",
                command=lambda uid=row['id']: self.handle_delete(uid)
            ).pack(side="left", padx=5)
    def filter_users(self):
        
        if self.search_id.get() and not self.search_id.get().isdigit():
            messagebox.showwarning("Invalid Input", "Employee ID filter must contain only numbers.")
            self.search_id.focus()
            return
        
        for w in self.list_frame.winfo_children():
            w.destroy()

        conditions = []
        params = []

        if self.search_id.get():
            conditions.append("u.employee_id LIKE %s")
            params.append(f"%{self.search_id.get()}%")

        if self.search_name.get():
            if self.search_name.get().isdigit():
                messagebox.showwarning("Invalid Input", "Full Name filter cannot be numeric.")
                self.search_name.focus()
                return
            else:
                conditions.append("u.full_name LIKE %s")
                params.append(f"%{self.search_name.get()}%")

        if self.search_role.get() != "All":
            conditions.append("u.role = %s")
            params.append(self.search_role.get())

        if self.search_team.get() != "All":
            conditions.append("t.team_name = %s")
            params.append(self.search_team.get())

        if self.search_batch.get():
            if not self.search_batch.get().isdigit():
                messagebox.showwarning("Invalid Input", "Batch filter must contain only numbers.")
                self.search_batch.focus()
                return
            else:
                conditions.append("u.batch LIKE %s")
                params.append(f"%{self.search_batch.get()}%")

        where_clause = " AND ".join(conditions)
        if where_clause:
            where_clause = "WHERE " + where_clause

        sql = f"""
        SELECT u.*, t.team_name 
        FROM users u
        LEFT JOIN teams t ON u.team_id = t.team_id
        {where_clause}
        ORDER BY u.id DESC
        """

        self.db.cursor.execute(sql, tuple(params))
        rows = self.db.cursor.fetchall()

        # ✅ MUST BE INSIDE FUNCTION (same indentation level)
        if not rows:
            ctk.CTkLabel(
                self.list_frame,
                text="This member is not exist.",
                font=("Arial", 16, "bold"),
                text_color="red"
            ).pack(pady=50)
            return  # ✅ NOW CORRECT

        self.render_table(rows)
    def reset_filters(self):
        # Clear text fields
        self.search_id.delete(0, "end" )
        self.search_name.delete(0, "end" )
        self.search_batch.delete(0, "end")

        # Reset dropdowns
        self.search_role.set("All")
        self.search_team.set("All")
        
        self.search_id.focus()
        self.search_name.focus()
        self.search_batch.focus()
        self.focus()  # Set focus back to the main frame

    # Reload full list
        self.refresh_list()
        
    def render_table(self, rows):
    # --- TABLE HEADER ---
        headers = ["Employee ID", "Full Name", "Role", "Team", "Batch", "Actions"]

        for col, header in enumerate(headers):
            ctk.CTkLabel(
                self.list_frame,
                text=header,
                font=("Arial", 13, "bold")
            ).grid(row=0, column=col, padx=10, pady=10, sticky="w")

        # --- TABLE ROWS ---
        for i, row in enumerate(rows, start=1):
            emp_id = row['employee_id']
            name = row['full_name']
            role = row['role']
            team = row['team_name'] if row['team_name'] else "No Team"
            batch = row['batch'] if row['batch'] else "N/A"

            ctk.CTkLabel(self.list_frame, text=emp_id).grid(row=i, column=0, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(self.list_frame, text=name).grid(row=i, column=1, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(self.list_frame, text=role).grid(row=i, column=2, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(self.list_frame, text=team).grid(row=i, column=3, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(self.list_frame, text=batch).grid(row=i, column=4, padx=10, pady=8, sticky="w")

            btn_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            btn_frame.grid(row=i, column=5, padx=10, pady=5)

            ctk.CTkButton(
                btn_frame, text="Update", width=70, height=28,
                fg_color="#166DBF",
                command=lambda uid=row['id']: self.handle_update(uid)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                btn_frame, text="Delete", width=70, height=28,
                fg_color="#C0392B",
                command=lambda uid=row['id']: self.handle_delete(uid)
            ).pack(side="left", padx=5)
        
    def handle_update(self, uid):
        self.clear_container()

        update_form = UserUpdateFrame(
            self.container,
            self.db,
            uid,
            self.show_list_view
        )

        update_form.pack(fill="both", expand=True)

    def handle_delete(self, uid):
        if uid == self.user['id']:
            messagebox.showwarning("Denied", "You cannot delete yourself!")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            self.db.cursor.execute("DELETE FROM users WHERE id=%s", (uid,))
            self.db.conn.commit()
            self.refresh_list()