import customtkinter as ctk
from database import Database
from tkinter import messagebox  

class DailyReportFrame(ctk.CTkFrame):
    def __init__(self, parent, user, **kwargs):
        # Set the background color to black
        super().__init__(parent, fg_color="black", **kwargs)
        self.user = user

        # Center-aligned greeting text label
        self.label = ctk.CTkLabel(
            self, 
            text="hello ei khaing moe fighting ", 
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")