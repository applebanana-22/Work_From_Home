import customtkinter as ctk
from database import Database
from dashboard import Dashboard

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WFH Tracker - Login")
        self.geometry("400x300")
        self.db = Database()

        self.label = ctk.CTkLabel(self, text="WFH System Login", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.pass_entry.pack(pady=10)

        self.login_btn = ctk.CTkButton(self, text="Login", command=self.login_event)
        self.login_btn.pack(pady=20)

    def login_event(self):
        user = self.db.authenticate(self.user_entry.get(), self.pass_entry.get())
        if user:
            self.destroy()  # Close login window
            app = Dashboard(user) # Pass user data to dashboard
            app.mainloop()
        else:
            print("Invalid Login")
            

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()