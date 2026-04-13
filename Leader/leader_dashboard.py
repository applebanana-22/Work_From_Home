import customtkinter as ctk
from tkinter import ttk
import socketio
from database import Database
from datetime import datetime

class LeaderDashboard(ctk.CTkFrame):
    def __init__(self, parent, user, db=None):
        super().__init__(parent, fg_color="transparent")
        self.user = user  # ဝင်ထားတဲ့ user object (dictionary ဖြစ်ရပါမယ်)
        self.db = db if db else Database() 
        self.sio = socketio.Client()
        
        self.setup_ui()
        self.connect_tracking_server()
        self.load_initial_data()

    def setup_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header, 
            text=f"Team Monitor: {self.user['full_name']}", 
            font=("Arial", 24, "bold")
        ).pack(side="left")

        self.table_frame = ctk.CTkFrame(self, fg_color=("#DBDBDB", "#2B2B2B"))
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

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

        self.tree.heading("id", text="Employee ID")
        self.tree.heading("name", text="Full Name")
        self.tree.heading("wfh_office", text="Work Mode")
        self.tree.heading("attendance", text="Check-in Time")
        self.tree.heading("status", text="Live Status")

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

            # Leader ရဲ့ employee_id ကို သတ်မှတ်ပါ
            leader_emp_id = self.user['employee_id'] 

            # Database query - Table structure အမှန်အတိုင်း ပြင်ထားပါသည်
            query = f"""
                SELECT 
                    u.employee_id, 
                    u.full_name, 
                    u.status AS live_status,
                    COALESCE(a.location_type, 'N/A') AS work_mode,
                    COALESCE(a.check_in, 'Not Yet') AS check_in_time
                FROM users u
                LEFT JOIN attendance a ON u.id = a.user_id 
                    AND a.attendance_date = CURDATE()
                WHERE u.team_id = (SELECT team_id FROM users WHERE employee_id = %s)
                AND u.role = 'member'
            """
            
            # self.db.cursor.execute ကို သုံးပြီး leader_id ကို safe ဖြစ်အောင် pass လုပ်ပါ
            self.db.cursor.execute(query, (leader_emp_id,))
            members = self.db.cursor.fetchall()

            for m in members:
                # Live Status Icons
                live = (m['live_status'] or "OFFLINE").upper()
                if live == "ACTIVE": icon = "🟢"
                elif live == "AWAY": icon = "🟡"
                else: icon = "🔴"
                
                # Work Mode Display
                mode = m['work_mode']
                display_mode = "🏠 WFH" if mode == "WFH" else "🏢 Office" if mode == "Office" else "N/A"
                
                self.tree.insert("", "end", values=(
                    m['employee_id'],
                    m['full_name'],
                    display_mode,
                    m['check_in_time'],
                    f"{icon} {live}"
                ))
        except Exception as e:
            print(f"Error loading initial data: {e}")

    def connect_tracking_server(self):
        try:
            self.sio.connect('http://localhost:5000') 
            
            @self.sio.on("status_update")
            def on_update(data):
                # UI thread မှာ refresh ဖြစ်အောင် schedule လုပ်ပါ
                self.after(100, self.load_initial_data)
                
        except Exception as e:
            print(f"Tracking Server Connection Failed: {e}")

    def __del__(self):
        try:
            if hasattr(self, 'sio') and self.sio.connected:
                self.sio.disconnect()
        except:
            pass