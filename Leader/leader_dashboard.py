import customtkinter as ctk
from tkinter import ttk
import socketio
from database import Database
from datetime import datetime

class LeaderDashboard(ctk.CTkFrame):
    def __init__(self, parent, user, db=None):
        super().__init__(parent, fg_color="transparent")
        self.user = user
        # Use existing DB connection or create a new one
        self.db = db if db else Database() 
        self.sio = socketio.Client()
        
        self.setup_ui()
        self.connect_tracking_server()
        self.load_initial_data()

    def setup_ui(self):
        # --- Header Section ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header, 
            text=f"Team Monitor: {self.user['full_name']}", 
            font=("Arial", 24, "bold")
        ).pack(side="left")

        # --- Table Section ---
        self.table_frame = ctk.CTkFrame(self, fg_color=("#DBDBDB", "#2B2B2B"))
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Configure Treeview Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2B2B2B",
                        foreground="white",
                        fieldbackground="#2B2B2B",
                        rowheight=35,
                        borderwidth=0)
        style.map("Treeview", background=[('selected', '#3498DB')])
        style.configure("Treeview.Heading", 
                        background="#1A1A1A", 
                        foreground="white", 
                        relief="flat",
                        font=("Arial", 12, "bold"))

        columns = ("id", "name", "wfh_office", "attendance", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        # Define Headings
        self.tree.heading("id", text="Employee ID")
        self.tree.heading("name", text="Full Name")
        self.tree.heading("wfh_office", text="Work Mode")
        self.tree.heading("attendance", text="Check-in Time")
        self.tree.heading("status", text="Live Status")

        # Define Column Widths
        self.tree.column("id", width=100, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("wfh_office", width=120, anchor="center")
        self.tree.column("attendance", width=150, anchor="center")
        self.tree.column("status", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True)

    def load_initial_data(self):
        """Fetch current team status from Database"""
        try:
            # Clear existing rows
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Join users with attendance to see who checked in today
            query = """
                SELECT u.employee_id, u.full_name, u.current_status, u.status as live_stat, a.check_in_time
                FROM users u
                LEFT JOIN attendance a ON u.id = a.user_id AND a.attendance_date = CURDATE()
                WHERE u.team_id = %s AND u.role = 'member'
            """
            self.db.cursor.execute(query, (self.user['team_id'],))
            members = self.db.cursor.fetchall()

            for m in members:
                live = (m['live_stat'] or "OFFLINE").upper()
                # Status Icons
                if live == "ACTIVE": icon = "🟢"
                elif live == "AWAY": icon = "🟡"
                else: icon = "🔴"
                
                check_in = m['check_in_time'] if m['check_in_time'] else "Not Yet"
                mode = m['current_status'] if m['current_status'] else "Office"
                
                self.tree.insert("", "end", values=(
                    m['employee_id'],
                    m['full_name'],
                    "🏠 WFH" if mode == "WFH" else "🏢 Office",
                    check_in,
                    f"{icon} {live}"
                ))
        except Exception as e:
            print(f"Error loading initial data: {e}")

    def connect_tracking_server(self):
        """Connect to SocketIO server for real-time status updates"""
        try:
            # URL should match tracking_server.py address
            self.sio.connect('http://localhost:5000') 
            
            @self.sio.on("status_update")
            def on_update(data):
                # When a member's status changes, refresh the table
                print(f"Received update for User {data['user_id']}")
                self.load_initial_data()
                
        except Exception as e:
            print(f"Tracking Server Connection Failed: {e}")

    def __del__(self):
        """Ensure socket is closed when dashboard is destroyed"""
        try:
            if self.sio.connected:
                self.sio.disconnect()
        except:
            pass