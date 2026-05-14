import customtkinter as ctk

class DailyReportFrame(ctk.CTkFrame):
    def __init__(self, parent, user, **kwargs):
        # Set the background color to black
        super().__init__(parent, fg_color="black", **kwargs)
        self.user = user

        # Center-aligned greeting text label
        self.label = ctk.CTkLabel(
            self, 
            text="Hello Ei Khaing Moe Fighting  💪", 
            font=("Arial", 24, "bold"),
            text_color="Pink"
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")