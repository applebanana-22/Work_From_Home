import customtkinter as ctk
from database import Database
from tkinter import messagebox

class UserRegisterWindow(ctk.CTkToplevel):
    """အကောင့်သစ်ဖွင့်ရန် သီးသန့်ပေါ်လာမည့် Window အသစ်"""
    def __init__(self, parent, db, refresh_callback):
        super().__init__(parent)
        self.title("Register New User")
        self.geometry("500x650") 
        self.db = db
        self.refresh_callback = refresh_callback
        
        # Window Settings
        self.attributes("-topmost", True)
        self.grab_set()

        ctk.CTkLabel(self, text="Create New Account", font=("Arial", 20, "bold")).pack(pady=20)

        # Form Container
        self.f = ctk.CTkFrame(self, fg_color="transparent")
        self.f.pack(fill="both", expand=True, padx=30)

        # Entry Fields (Common)
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
            command=self.update_ui_by_role # Role ပြောင်းတိုင်း UI update လုပ်ရန်
        )
        self.role.pack(fill="x", pady=(2, 10))
        self.role.set("member")

        # --- Batch Field Container (Dynamic) ---
        self.batch_frame = ctk.CTkFrame(self.f, fg_color="transparent")
        # အစကတည်းက member ဖြစ်နေလို့ ချက်ချင်းပြထားပါမယ်
        self.batch_frame.pack(fill="x")

        ctk.CTkLabel(self.batch_frame, text="Batch Number (Manual Entry):", font=("Arial", 11)).pack(anchor="w", padx=5)
        self.batch = ctk.CTkEntry(self.batch_frame, placeholder_text="e.g. 11, 12", height=40)
        self.batch.pack(fill="x", pady=(2, 10))

        # --- Department Selection ---
        ctk.CTkLabel(self.f, text="Department:", font=("Arial", 11)).pack(anchor="w", padx=5)
        self.dept = ctk.CTkOptionMenu(self.f, values=["IT", "HR", "Sales", "Design"], height=38)
        self.dept.pack(fill="x", pady=(2, 10))
        self.dept.set("IT")

        self.save_btn = ctk.CTkButton(self.f, text="Register Account", height=45, 
                                      fg_color="#10B981", font=("Arial", 14, "bold"),
                                      command=self.save_user)
        self.save_btn.pack(fill="x", pady=25)

    def update_ui_by_role(self, choice):
        """Role ကိုကြည့်ပြီး Batch field ကို ပြသခြင်း/ဖျောက်ခြင်း logic အမှန်"""
        if choice == "member":
            # Batch field ကို Role ရဲ့ အောက်မှာ နေရာမှန်အောင် အမြဲပြန် pack ပါတယ်
            self.batch_frame.pack(fill="x", after=self.role)
        else:
            # member မဟုတ်ရင် UI ကနေ လုံးဝဖျောက်လိုက်ပါတယ်
            self.batch_frame.pack_forget()

    def save_user(self):
        role_val = self.role.get()
        # Role က member ဖြစ်နေမှသာ batch ကို စစ်ဆေးပါမယ်
        batch_input = self.batch.get().strip() if role_val == "member" else ""
        
        if role_val == "member" and not batch_input:
            messagebox.showwarning("Error", "Batch number is required for members!")
            return

        formatted_batch = f"Batch {batch_input}" if role_val == "member" else "N/A"
        
        # ... (ကျန်တဲ့ database save logic များ)

        data = (
            self.emp_id.get(), self.name.get(), self.uname.get(), 
            self.pwd.get(), role_val, self.dept.get(), formatted_batch
        )
        
        if not all(data[:4]):
            messagebox.showwarning("Error", "Required fields are empty!")
            return

        try:
            sql = """INSERT INTO users (employee_id, full_name, username, password, role, department, batch) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            self.db.cursor.execute(sql, data)
            self.db.conn.commit()
            messagebox.showinfo("Success", f"Successfully registered {data[1]}")
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
        for w in self.list_frame.winfo_children(): w.destroy()
        
        self.db.cursor.execute("SELECT * FROM users ORDER BY id DESC")
        for row in self.db.cursor.fetchall():
            # Modern Card Design
            card = ctk.CTkFrame(self.list_frame, corner_radius=8, border_width=1, 
                                fg_color=("#FFFFFF", "#252525"))
            card.pack(fill="x", pady=5, padx=10)
            
            # Text Visibility Fix (Tuple color used)
            display_info = f"{row['full_name']} ({row['employee_id']})"
            ctk.CTkLabel(card, text=display_info, font=("Arial", 13, "bold"),
                         text_color=("black", "white")).pack(side="left", padx=15, pady=12)
            
            # Batch Info Badge (If exists)
            if row.get('batch') and row['batch'] != "N/A":
                ctk.CTkLabel(card, text=row['batch'], font=("Arial", 11),
                             text_color="#3498DB").pack(side="left", padx=5)

            # Delete Action
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