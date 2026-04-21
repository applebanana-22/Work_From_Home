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
        
        # Connection ပြတ်ရင် auto ပြန်ချိတ်ရန် reconnection=True ထားပါသည်
        self.sio = socketio.Client(reconnection=True, reconnection_delay=5)
        
        self.setup_ui()
        self.load_initial_data() # ပထမဆုံးအကြိမ်တွင်သာ DB မှ data အကုန်ဆွဲမည်
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

        # Treeview Customization (Modern Dark Look)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2B2B2B",
                        foreground="white",
                        fieldbackground="#2B2B2B",
                        rowheight=45,
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
            self.tree.column(col, anchor="center", width=120)

        self.tree.column("name", width=220, anchor="w")
        self.tree.pack(fill="both", expand=True)

    def load_initial_data(self):
        """ပထမဆုံးအကြိမ် DB မှ Team members များ၏ status ကို refresh လုပ်ခြင်း"""
        try:
            # Table အဟောင်းကို ရှင်းထုတ်ခြင်း
            for item in self.tree.get_children():
                self.tree.delete(item)

            leader_emp_id = self.user['employee_id'] 

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
            
            self.db.ensure_connection() # Connection ရှိမရှိ အရင်စစ်မည်
            self.db.cursor.execute(query, (leader_emp_id,))
            members = self.db.cursor.fetchall()

            for m in members:
                # Icon Logic
                live = (m['live_status'] or "OFFLINE").upper()
                icon = "🟢" if live == "ACTIVE" else "🟡" if live == "AWAY" else "🔴"
                
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
        """Socket Server နှင့် ချိတ်ဆက်ပြီး Real-time Update ယူခြင်း"""
        try:
            if not self.sio.connected:
                # သင့် Server IP ကို ဒီမှာ စစ်ဆေးပါ
                self.sio.connect('http://192.168.100.83:5000', transports=['websocket', 'polling']) 
            
            @self.sio.on("status_update")
            def on_update(data):
                # UI Thread ပေါ်တွင်သာ Update လုပ်ရန် after() သုံးရပါမည်
                if self.winfo_exists():
                    self.after(0, lambda: self.update_row_only(data))
                    
        except Exception as e:
            print(f"⚠️ Tracking Server Connection Failed: {e}")

    def update_row_only(self, data):
        """DB ကို ထပ်မခေါ်တော့ဘဲ UI Table ထဲက Row ကိုပဲ တိုက်ရိုက်ပြင်သဖြင့် စက်မလေးတော့ပါ"""
        try:
            if not self.winfo_exists(): return
            
            target_user_id = str(data.get('user_id'))
            new_status = str(data.get('status')).upper()
            
            # Icon သတ်မှတ်ခြင်း
            icon = "🟢" if new_status == "ACTIVE" else "🟡" if new_status == "AWAY" else "🔴"

            # Treeview ထဲမှာ ပတ်ရှာပြီး သက်ဆိုင်ရာလူကိုပဲ update လုပ်မည်
            for item in self.tree.get_children():
                current_row_values = self.tree.item(item)['values']
                
                # Column index 0 က Employee ID ဖြစ်ရပါမည်
                if str(current_row_values[0]) == target_user_id:
                    self.tree.set(item, column="status", value=f"{icon} {new_status}")
                    print(f"✨ UI Smooth Update: {target_user_id} -> {new_status}")
                    break
        except Exception as e:
            print(f"⚠️ Row Update Error: {e}")

    def __del__(self):
        """Dashboard ကို ပိတ်လိုက်လျှင် socket connection ကို သေချာဖြတ်ရန်"""
        try:
            if hasattr(self, 'sio') and self.sio.connected:
                self.sio.disconnect()
                print("🔌 Dashboard Socket Disconnected Safely.")
        except:
            pass