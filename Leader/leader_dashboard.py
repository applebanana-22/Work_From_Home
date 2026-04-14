import customtkinter as ctk
from tkinter import ttk
import socketio
from database import Database
from datetime import datetime

class LeaderDashboard(ctk.CTkFrame):
    def __init__(self, parent, user, db=None):
        super().__init__(parent, fg_color="transparent")
        self.user = user  
        self.db = db if db else Database() 
        self.sio = socketio.Client(reconnection=True) # Connection ပြတ်ရင် auto ပြန်ချိတ်ရန်
        
        self.setup_ui()
        self.load_initial_data() # အရင်ဆုံး data အဟောင်းကို ဆွဲထုတ်ထားမည်
        self.connect_tracking_server()

    def setup_ui(self):
        # --- Header Section ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header, 
            text=f"📊 Team Real-time Monitor", 
            font=("Arial", 22, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            header, 
            text=f"Leader: {self.user['full_name']}", 
            font=("Arial", 14)
        ).pack(side="right")

        # --- Table Section ---
        self.table_frame = ctk.CTkFrame(self, fg_color=("#DBDBDB", "#2B2B2B"))
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview Customization
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2B2B2B",
                        foreground="white",
                        fieldbackground="#2B2B2B",
                        rowheight=40,
                        borderwidth=0)
        style.map("Treeview", background=[('selected', '#3498DB')])
        style.configure("Treeview.Heading", 
                        background="#1A1A1A", 
                        foreground="white", 
                        relief="flat",
                        font=("Arial", 11, "bold"))

        columns = ("id", "name", "wfh_office", "attendance", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        # Column Headings
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor="center")

        self.tree.column("name", width=200, anchor="w") # Name ကို ဘယ်ဘက်ကပ်ထားရန်
        self.tree.pack(fill="both", expand=True)

    def load_initial_data(self):
        """Database မှ Team members များ၏ status ကို refresh လုပ်ခြင်း"""
        try:
            # Table အဟောင်းကို ရှင်းထုတ်ခြင်း
            for item in self.tree.get_children():
                self.tree.delete(item)

            leader_emp_id = self.user['employee_id'] 

            # Query ကို ပိုမိုကောင်းမွန်အောင် ပြင်ထားပါသည် (Team တွင်းမှ member များသာ)
            query = """
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
            
            self.db.cursor.execute(query, (leader_emp_id,))
            members = self.db.cursor.fetchall()

            for m in members:
                # Live Status Icons Logic
                live = (m['live_status'] or "OFFLINE").upper()
                if live == "ACTIVE": icon = "🟢"
                elif live == "AWAY": icon = "🟡"
                else: icon = "🔴"
                
                # Work Mode Formatting
                mode = m['work_mode']
                display_mode = "🏠 WFH" if mode == "WFH" else "🏢 Office" if mode == "Office" else "⚪ N/A"
                
                self.tree.insert("", "end", values=(
                    m['employee_id'],
                    m['full_name'],
                    display_mode,
                    m['check_in_time'],
                    f"{icon} {live}"
                ))
        except Exception as e:
            print(f"❌ Error loading initial data: {e}")

    def connect_tracking_server(self):
        try:
            if not self.sio.connected:
                # Localhost နေရာမှာ သင့် Server IP (192.168.43.100) ပြောင်းထည့်ဖို့ မမေ့ပါနဲ့
                self.sio.connect('http://192.168.43.100:5000') 
            
            @self.sio.on("status_update")
            def on_update(data):
                print(f"🔄 Member Status Updated: {data}")
                
                # အရေးကြီးဆုံးအပိုင်း - UI frame တကယ်ရှိသေးမှ update လုပ်ရန်
                def safe_update():
                    try:
                        if self.winfo_exists(): # Frame ရှိမရှိ အရင်စစ်မယ်
                            self.load_initial_data()
                    except Exception:
                        pass # မရှိတော့ရင် ဘာမှမလုပ်ဘဲ ကျော်သွားမယ်

                self.after(0, safe_update)
                
        except Exception as e:
            print(f"⚠️ Tracking Server Connection Failed: {e}")

    def __del__(self):
        """Dashboard ကို ပိတ်လိုက်လျှင် socket connection ဖြတ်ရန်"""
        try:
            if hasattr(self, 'sio') and self.sio.connected:
                self.sio.disconnect()
        except:
            pass