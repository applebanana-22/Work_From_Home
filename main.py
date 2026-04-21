import customtkinter as ctk
from database import Database
from dashboard import Dashboard
 
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WFH Tracker - Login")
        self.geometry("400x350") # Increased height slightly for error message
        self.db = Database()
 
        self.label = ctk.CTkLabel(self, text="WFH System Login", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)
 
        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username", width=200)
        self.user_entry.pack(pady=10)
        self.user_entry.bind("<Return>", lambda event: self.login_event())  # ✅ added
 
        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=200)
        self.pass_entry.pack(pady=10)
        self.pass_entry.bind("<Return>", lambda event: self.login_event())  # ✅ added
 
        # Error Label (Initially empty)
        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 12))
        self.error_label.pack(pady=5)
 
        self.login_btn = ctk.CTkButton(self, text="Login", command=self.login_event)
        self.login_btn.pack(pady=10)
 
        # ✅ NEW LINE ADDED
        self.bind("<Return>", lambda event: self.login_event())
 
    def login_event(self):
        # 1. Reset visual states
        self.error_label.configure(text="")
        self.user_entry.configure(border_color=["#979DA2", "#565B5E"]) # Default colors
        self.pass_entry.configure(border_color=["#979DA2", "#565B5E"])
 
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
 
        # 2. Validation Check: Empty Fields
        if not username or not password:
            self.error_label.configure(text="Please fill in all fields.")
            if not username: self.user_entry.configure(border_color="red")
            if not password: self.pass_entry.configure(border_color="red")
            return
 
        # 3. Database Authentication
        user = self.db.authenticate(username, password)
       
        if user:
            self.destroy()  
            app = Dashboard(user)
            app.mainloop()
        else:
            # 4. Validation Check: Invalid Credentials
            self.error_label.configure(text="Invalid Username or Password")
            self.user_entry.configure(border_color="red")
            self.pass_entry.configure(border_color="red")
 
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()