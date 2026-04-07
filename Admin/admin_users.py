import customtkinter as ctk
from database import Database
from tkinter import messagebox

class UserRegisterFrame(ctk.CTkFrame):
    """The Registration Form UI - Now a Frame instead of a Toplevel"""
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
        self.f = ctk.CTkFrame(self, fg_color="transparent")
        self.f.pack(fill="both", expand=True, padx=40)

        # Entry Fields
        self.emp_id = ctk.CTkEntry(self.f, placeholder_text="Employee ID", height=45)
        self.emp_id.pack(fill="x", pady=8)

        self.name = ctk.CTkEntry(self.f, placeholder_text="Full Name", height=45)
        self.name.pack(fill="x", pady=8)

        self.uname = ctk.CTkEntry(self.f, placeholder_text="Username", height=45)
        self.uname.pack(fill="x", pady=8)

        self.pwd = ctk.CTkEntry(self.f, placeholder_text="Password", height=45, show="*")
        self.pwd.pack(fill="x", pady=8)

        # Role Selection
        ctk.CTkLabel(self.f, text="User Role:", font=("Arial", 12)).pack(anchor="w", padx=5, pady=(10, 0))
        self.role = ctk.CTkOptionMenu(
            self.f, values=["admin", "leader", "member"], 
            height=40, command=self.update_ui_by_role
        )
        self.role.pack(fill="x", pady=(2, 12))
        self.role.set("member")

        # Team Selection
        ctk.CTkLabel(self.f, text="Assign Team:", font=("Arial", 12)).pack(anchor="w", padx=5)
        teams_data = self.db.get_all_teams()
        self.team_map = {t['team_name']: t['team_id'] for t in teams_data}
        team_options = list(self.team_map.keys()) if self.team_map else ["No Teams Found"]

        self.team_dropdown = ctk.CTkOptionMenu(self.f, values=team_options, height=40)
        self.team_dropdown.pack(fill="x", pady=(2, 12))

        # Batch Field
        self.batch_frame = ctk.CTkFrame(self.f, fg_color="transparent")
        self.batch_frame.pack(fill="x")
        ctk.CTkLabel(self.batch_frame, text="Batch Number:", font=("Arial", 12)).pack(anchor="w", padx=5)
        self.batch = ctk.CTkEntry(self.batch_frame, placeholder_text="e.g. 11, 12", height=45)
        self.batch.pack(fill="x", pady=(2, 10))

        self.save_btn = ctk.CTkButton(
            self.f, text="Save Account", height=50, 
            fg_color="#10B981", hover_color="#059669", 
            font=("Arial", 15, "bold"), command=self.save_user
        )
        self.save_btn.pack(fill="x", pady=30)

    def update_ui_by_role(self, choice):
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

        if not all([self.emp_id.get(), self.name.get(), self.uname.get(), self.pwd.get()]):
            messagebox.showwarning("Error", "Required fields are empty!")
            return

        try:
            sql = """INSERT INTO users (employee_id, full_name, username, password, role, team_id, batch) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            data = (self.emp_id.get(), self.name.get(), self.uname.get(), 
                    self.pwd.get(), role_val, team_id, formatted_batch)
            
            self.db.cursor.execute(sql, data)
            self.db.conn.commit()
            messagebox.showinfo("Success", f"User {self.name.get()} created!")
            self.back_callback() # Switch back to list view
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


class AdminUsers(ctk.CTkFrame):
    """The Main Controller - Manages switching between List and Register form"""
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user_data

        # Single container that we clear and refill
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_list_view()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_list_view(self):
        self.clear_container()

        # Header
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="User Management", font=("Arial", 24, "bold")).pack(side="left")

        self.add_btn = ctk.CTkButton(
            header, text="+ Create Account", fg_color="#10B981", 
            height=38, command=self.show_register_view
        )
        self.add_btn.pack(side="right")

        # List
        self.list_frame = ctk.CTkScrollableFrame(self.container, label_text="Active Accounts")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.refresh_list()

    def show_register_view(self):
        self.clear_container()
        # Create form and tell it to call 'show_list_view' when finished/canceled
        reg_form = UserRegisterFrame(self.container, self.db, self.show_list_view)
        reg_form.pack(fill="both", expand=True)

    def refresh_list(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        
        sql = """
            SELECT u.*, t.team_name 
            FROM users u
            LEFT JOIN teams t ON u.team_id = t.team_id 
            ORDER BY u.id DESC
        """
        self.db.cursor.execute(sql)
        
        for row in self.db.cursor.fetchall():
            card = ctk.CTkFrame(self.list_frame, corner_radius=8, border_width=1, fg_color=("#FFFFFF", "#252525"))
            card.pack(fill="x", pady=5, padx=10)
            
            display_info = f"{row['full_name']} ({row['employee_id']})"
            ctk.CTkLabel(card, text=display_info, font=("Arial", 13, "bold")).pack(side="left", padx=15, pady=12)
            
            team_text = row['team_name'] if row['team_name'] else "No Team"
            ctk.CTkLabel(card, text=f"📍 {team_text}", font=("Arial", 11, "italic"), text_color="#3498DB").pack(side="left", padx=10)

            ctk.CTkButton(
                card, text="Delete", width=70, height=28, fg_color="#C0392B", 
                command=lambda i=row['id']: self.handle_delete(i)
            ).pack(side="right", padx=15)

    def handle_delete(self, uid):
        if uid == self.user['id']:
            messagebox.showwarning("Denied", "You cannot delete yourself!")
            return
        if messagebox.askyesno("Confirm", "Are you sure?"):
            self.db.cursor.execute("DELETE FROM users WHERE id=%s", (uid,))
            self.db.conn.commit()
            self.refresh_list()