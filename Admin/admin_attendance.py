import customtkinter as ctk
from tkinter import ttk
from database import Database

class AdminAttendance(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.db = Database()
        self.user = user

        # --- UI Header ---
        header_f = ctk.CTkFrame(self, fg_color="transparent")
        header_f.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header_f, text="📋 Employee Attendance Logs", 
            font=("Arial", 22, "bold"),
            text_color=("#2C3E50", "#FFFFFF")
        ).pack(side="left")

        # Search / Filter Box
        self.search_entry = ctk.CTkEntry(header_f, placeholder_text="Search by Name or ID...", width=250)
        self.search_entry.pack(side="right", padx=10)
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_data())

        # --- Table Area ---
        self.create_table()
        self.load_data()

    def create_table(self):
        # Table Container
        table_frame = ctk.CTkFrame(self, fg_color=("#FFFFFF", "#1E1E1E"))
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Styling Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background=("#FFFFFF" if ctk.get_appearance_mode()=="Light" else "#1E1E1E"),
                        foreground=("#000000" if ctk.get_appearance_mode()=="Light" else "#FFFFFF"),
                        fieldbackground=("#FFFFFF" if ctk.get_appearance_mode()=="Light" else "#1E1E1E"),
                        rowheight=35)
        style.map("Treeview", background=[('selected', '#3498DB')])

        # Define Columns
        columns = ("id", "name", "date", "check_in", "check_out", "location")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Headings
        self.tree.heading("id", text="Emp ID")
        self.tree.heading("name", text="Employee Name")
        self.tree.heading("date", text="Date")
        self.tree.heading("check_in", text="Check-In")
        self.tree.heading("check_out", text="Check-Out")
        self.tree.heading("location", text="Location")

        # Column widths
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=200)
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("check_in", width=120, anchor="center")
        self.tree.column("check_out", width=120, anchor="center")
        self.tree.column("location", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def load_data(self):
        # Clear current rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        search_query = self.search_entry.get()
        
        try:
            # Join Query to get Name from Users Table
            sql = """
                SELECT u.id, u.full_name, a.attendance_date, a.check_in_time, a.check_out_time, a.location 
                FROM attendance a
                JOIN users u ON a.user_id = u.id
                WHERE u.full_name LIKE %s OR u.id LIKE %s
                ORDER BY a.attendance_date DESC, a.check_in_time DESC
            """
            self.db.cursor.execute(sql, (f"%{search_query}%", f"%{search_query}%"))
            rows = self.db.cursor.fetchall()

            for row in rows:
                # Format times and dates nicely
                self.tree.insert("", "end", values=(
                    row['id'], 
                    row['full_name'], 
                    row['attendance_date'], 
                    row['check_in_time'], 
                    row['check_out_time'] if row['check_out_time'] else "--:--",
                    row['location']
                ))
        except Exception as e:
            print(f"Fetch Error: {e}")