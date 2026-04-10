import customtkinter as ctk
from tkinter import ttk
import socketio
from database import Database
from datetime import datetime

class LeaderDashboard(ctk.CTkFrame):
    def __init__(self, parent, user, db=None):
        super().__init__(parent, fg_color="transparent")
        self.user = user
        self.db = Database() # database.py မှ class ကို သုံးခြင်း
        self.sio = socketio.Client()
        
        self.setup_ui()
        self.connect_tracking_server()
        self.load_initial_data()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(header, text=f"Team Monitor: {self.user['full_name']}", font=("Arial", 24, "bold")).pack(side="left")

        # Table Section
        self.table_frame = ctk.CTkFrame(self, fg_color=("#DBDBDB", "#2B2B2B"))
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("id", "name", "wfh_office", "attendance", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("id", text="Emp ID")
        self.tree.heading("name", text="Member Name")
        self.tree.heading("wfh_office", text="Work Mode")
        self.tree.heading("attendance", text="Check-In")
        self.tree.heading("status", text="Live Status")

        self.tree.column("status", width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_initial_data(self):
        """Database မှ မိမိ Team Member များကို ဆွဲထုတ်ပြသခြင်း"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # users table နှင့် attendance table ကို Join လုပ်ပြီး ယနေ့အတွက် status ယူခြင်း
            query = """
                SELECT u.employee_id, u.full_name, u.current_status, u.status as live_stat, a.check_in
                FROM users u
                LEFT JOIN attendance a ON u.id = a.user_id AND a.attendance_date = CURDATE()
                WHERE u.team_id = %s AND u.role = 'member'
            """
            self.db.cursor.execute(query, (self.user['team_id'],))
            members = self.db.cursor.fetchall()

            for m in members:
                live = m['live_stat'].upper() if m['live_stat'] else "OFFLINE"
                icon = "🟢" if live == "ACTIVE" else "🟡" if live == "AWAY" else "🔴"
                
                self.tree.insert("", "end", values=(
                    m['employee_id'],
                    m['full_name'],
                    m['current_status'],
                    m['check_in'] if m['check_in'] else "Not Yet",
                    f"{icon} {live}"
                ))
        except Exception as e:
            print(f"Error loading data: {e}")

    def connect_tracking_server(self):
        @self.sio.on("status_update")
        def on_update(data):
            # Server မှ data အသစ်ရောက်လာတိုင်း Table ကို refresh လုပ်ပေးသည်
            self.load_initial_data()

        try:
            # သင့် Server IP သို့ ပြောင်းလဲပါ
            self.sio.connect("http://192.168.100.174:5000")
        except:
            pass