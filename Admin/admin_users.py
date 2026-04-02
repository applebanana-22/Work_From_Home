import customtkinter as ctk
from database import Database
from tkinter import messagebox

class UserRegisterWindow(ctk.CTkToplevel):
    """Window to register new users with Dynamic Team Selection"""
    def __init__(self, parent, db, refresh_callback):
        super().__init__(parent)
        self.title("Register New User")
        self.geometry("500x700") 
        self.db = db
        self.refresh_callback = refresh_callback
        
        # Window Settings
        self.attributes("-topmost", True)
        self.grab_set()

        ctk.CTkLabel(self, text="Create New Account", font=("Arial", 20, "bold")).pack(pady=20)

        # Form Container
        self.f = ctk.CTkFrame(self, fg_color="transparent")
        self.f.pack(fill="both", expand=True, padx=30)

        # Entry Fields
        self.emp_id = ctk.CTkEntry(self.f, placeholder_text="Employee ID", height=40)
        self.emp_id.pack(fill="x", pady=5)

        self.name = ctk.CTkEntry(self.f, placeholder_text="Full Name", height=40)
        self.name.pack(fill="x", pady=5)

        self.uname = ctk.CTkEntry(self.f, placeholder_text="Username", height=40)
        self.uname.pack(fill="x", pady=5)

        self.pwd = ctk.CTkEntry(self.f, placeholder_text="Password", height=40, show="*")
        self.pwd.pack(fill="x", pady=5)

        # --- Role Selection ---
        ctk.CTkLabel(self.f, text="User Role:", font=("Arial", 11)).pack(anchor="w", padx=5, pady=(5, 0))
        self.role = ctk.CTkOptionMenu(
            self.f, 
            values=["admin", "leader", "member"], 
            height=38,
            command=self.update_ui_by_role
        )
        self.role.pack(fill="x", pady=(2, 10))
        self.role.set("member")

        # --- Team Selection (Dynamic) ---
        ctk.CTkLabel(self.f, text="Assign Team:", font=("Arial", 11)).pack(anchor="w", padx=5)
        
        # Fetching current teams from the database
        teams_data = self.db.get_all_teams()
        self.team_map = {t['team_name']: t['team_id'] for t in teams_data}
        team_options = list(self.team_map.keys()) if self.team_map else ["No Teams Found"]

        self.team_dropdown = ctk.CTkOptionMenu(self.f, values=team_options, height=38)
        self.team_dropdown.pack(fill="x", pady=(2, 10))

        # --- Batch Field (Only for members) ---
        self.batch_frame = ctk.CTkFrame(self.f, fg_color="transparent")
        self.batch_frame.pack(fill="x")

        ctk.CTkLabel(self.batch_frame, text="Batch Number:", font=("Arial", 11)).pack(anchor="w", padx=5)
        self.batch = ctk.CTkEntry(self.batch_frame, placeholder_text="e.g. 11, 12", height=40)
        self.batch.pack(fill="x", pady=(2, 10))

        self.save_btn = ctk.CTkButton(self.f, text="Register Account", height=45, 
                                      fg_color="#10B981", font=("Arial", 14, "bold"),
                                      command=self.save_user)
        self.save_btn.pack(fill="x", pady=25)

    def update_ui_by_role(self, choice):
        """Show batch field only if the user is a member"""
        if choice == "member":
            self.batch_frame.pack(fill="x", after=self.team_dropdown)
        else:
            self.batch_frame.pack_forget()

    def save_user(self):
        role_val = self.role.get()
        selected_team = self.team_dropdown.get()
        team_id = self.team_map.get(selected_team)
        
        batch_input = self.batch.get().strip() if role_val == "member" else ""
        formatted_batch = f"Batch {batch_input}" if batch_input else "N/A"
        
        # Validation
        fields = [self.emp_id.get(), self.name.get(), self.uname.get(), self.pwd.get()]
        if not all(fields):
            messagebox.showwarning("Error", "Required fields are empty!")
            return
        
        if not team_id:
            messagebox.showwarning("Error", "Please select a valid team!")
            return

        try:
            sql = """INSERT INTO users (employee_id, full_name, username, password, role, team_id, batch) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            data = (self.emp_id.get(), self.name.get(), self.uname.get(), 
                    self.pwd.get(), role_val, team_id, formatted_batch)
            
            self.db.cursor.execute(sql, data)
            self.db.conn.commit()
            messagebox.showinfo("Success", f"Registered {self.name.get()} to {selected_team}")
            self.refresh_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


class AdminUsers(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user_data

        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(self.header, text="User Management", font=("Arial", 24, "bold")).pack(side="left")

        self.add_btn = ctk.CTkButton(self.header, text="+ Create Account", 
                                     fg_color="#10B981", height=38,
                                     command=self.open_register_window)
        self.add_btn.pack(side="right")

        # Scrollable List
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Active Accounts", 
                                                 fg_color=("#F5F5F5", "#121212"))
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_list()

    def open_register_window(self):
        UserRegisterWindow(self, self.db, self.refresh_list)

    def refresh_list(self):
        """Fetch users and their Team Names using a LEFT JOIN"""
        for w in self.list_frame.winfo_children(): w.destroy()
        
        sql = """
            SELECT u.*, t.team_name 
            FROM users u
            LEFT JOIN teams t ON u.team_id = t.team_id 
            ORDER BY u.id DESC
        """
        self.db.cursor.execute(sql)
        
        for row in self.db.cursor.fetchall():
            card = ctk.CTkFrame(self.list_frame, corner_radius=8, border_width=1, 
                                fg_color=("#FFFFFF", "#252525"))
            card.pack(fill="x", pady=5, padx=10)
            
            # Left: Name and ID
            display_info = f"{row['full_name']} ({row['employee_id']})"
            ctk.CTkLabel(card, text=display_info, font=("Arial", 13, "bold"),
                         text_color=("#2C3E50", "#FFFFFF")).pack(side="left", padx=15, pady=12)
            
            # Center-Left: Team Name (The new feature)
            team_text = row['team_name'] if row['team_name'] else "No Team"
            ctk.CTkLabel(card, text=f"📍 {team_text}", font=("Arial", 11, "italic"),
                         text_color="#3498DB").pack(side="left", padx=10)

            # Center-Right: Role & Batch
            role_badge = f"{row['role'].upper()} | {row['batch']}"
            ctk.CTkLabel(card, text=role_badge, font=("Arial", 11),
                         text_color="#7F8C8D").pack(side="left", padx=10)

            # Right: Delete Button
            ctk.CTkButton(card, text="Delete", width=70, height=28, fg_color="#C0392B", 
                          hover_color="#A93226",
                          command=lambda i=row['id']: self.handle_delete(i)).pack(side="right", padx=15)

    def handle_delete(self, uid):
        if uid == self.user['id']:
            messagebox.showwarning("Denied", "You cannot delete yourself!")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            self.db.cursor.execute("DELETE FROM users WHERE id=%s", (uid,))
            self.db.conn.commit()
            self.refresh_list()