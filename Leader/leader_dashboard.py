import customtkinter as ctk
from tkinter import ttk
import socketio
from database import Database
from datetime import datetime

class LeaderDashboard(ctk.CTkFrame):
    def __init__(self, parent, user, db=None):
        # 🟢 Global Theme ကို Light သို့မဟုတ် Dark manual သတ်မှတ်လိုပါက အောက်ပါ code ကိုသုံးနိုင်သည်
        # ctk.set_appearance_mode("Light")
        
        # Light mode: White (#FFFFFF), Dark mode: Dark Gray (#1A1A1A)
        super().__init__(parent, fg_color=("#FFFFFF", "#1A1A1A"))
        
        self.user = user  
        self.db = db if db else Database() 
        self.sio = socketio.Client(reconnection=True, reconnection_delay=5)
        
        self.setup_ui()
        self.load_initial_data() 
        self.connect_tracking_server()

    def setup_ui(self):
        # --- Header Section ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        # text_color ကို tuple ပေးထားခြင်းဖြင့် Theme အလိုက် အဖြူ/အနက် auto ပြောင်းမည်
        label_text_color = ("#000000", "#FFFFFF")
        
        ctk.CTkLabel(
            header, 
            text="📊 Team Real-time Monitor", 
            font=("Arial", 24, "bold"),
            text_color=label_text_color
        ).pack(side="left")

        # ctk.CTkLabel(
        #     header, 
        #     text=f"Leader: {self.user['full_name']}", 
        #     font=("Arial", 14),
        #     text_color=label_text_color
        # ).pack(side="right")

        # --- Table Section ---
        # Frame bg ကိုလည်း theme အလိုက် ပြောင်းရန် tuple သုံးပါမည်
        self.table_frame = ctk.CTkFrame(self, fg_color=("#FFFFFF", "#1A1A1A"))
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        
        # Real-time Theme detection
        is_dark = ctk.get_appearance_mode() == "Dark"
        tree_bg = "#2B2B2B" if is_dark else "#FFFFFF"
        tree_fg = "#FFFFFF" if is_dark else "#000000"
        header_bg = "#1A1A1A" if is_dark else "#F0F0F0"

        style.configure("Treeview",
                        background=tree_bg,
                        foreground=tree_fg,
                        fieldbackground=tree_bg,
                        rowheight=45,
                        borderwidth=0)
        
        style.configure("Treeview.Heading", 
                        background=header_bg, 
                        foreground=tree_fg, 
                        relief="flat",
                        font=("Arial", 11, "bold"))
        
        style.map("Treeview", background=[('selected', '#3498DB')])

        columns = ("id", "name", "role", "wfh_office", "check_in", "check_out", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        col_settings = {"id": 80, "name": 200, "role": 100, "wfh_office": 100, "check_in": 120, "check_out": 120, "status": 130}
        for col, width in col_settings.items():
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor="center", width=width)

        self.tree.column("name", anchor="w")
        self.tree.pack(fill="both", expand=True)

        # Status Color Configuration
        self.tree.tag_configure("normal", foreground=tree_fg)
        self.tree.tag_configure("ACTIVE", foreground="#2ECC71")  
        self.tree.tag_configure("AWAY", foreground="#F1C40F")    
        self.tree.tag_configure("OFFLINE", foreground="#E74C3C") 

    def load_initial_data(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            query = """
                SELECT u.employee_id, u.full_name, u.role, u.status,
                COALESCE(a.location_type, 'N/A') AS mode,
                COALESCE(TIME_FORMAT(a.check_in, '%h:%i %p'), '---') AS in_t,
                COALESCE(TIME_FORMAT(a.check_out, '%h:%i %p'), '---') AS out_t
                FROM users u
                LEFT JOIN attendance a ON u.id = a.user_id AND a.attendance_date = CURDATE()
                WHERE u.team_id = (SELECT team_id FROM users WHERE employee_id = %s) AND u.role = 'member'
            """
            self.db.ensure_connection()
            self.db.cursor.execute(query, (self.user['employee_id'],))
            
            # Theme check again for insertion
            is_dark = ctk.get_appearance_mode() == "Dark"
            tree_fg = "#FFFFFF" if is_dark else "#000000"
            self.tree.tag_configure("normal", foreground=tree_fg)

            for m in self.db.cursor.fetchall():
                live = (m['status'] or "OFFLINE").upper()
                icon = "🟢" if live == "ACTIVE" else "🟡" if live == "AWAY" else "🔴"
                self.tree.insert("", "end", values=(
                    m['employee_id'], m['full_name'], m['role'].title(),
                    m['mode'], m['in_t'], m['out_t'], f"{icon} {live}"
                ), tags=("normal", live))
        except Exception as e:
            print(f"❌ Error: {e}")

    def connect_tracking_server(self):
        try:
            if not self.sio.connected:
                # transports ကို websocket တစ်ခုတည်း အရင်စမ်းကြည့်ပါ (ပိုမြန်ပြီး ပိုငြိမ်တတ်သည်)
                self.sio.connect('http://192.168.100.137:5000', transports=['websocket']) 
            
            @self.sio.on("status_update")
            def on_update(data):
                # Widget ရှိနေသေးကြောင်း သေချာစွာ စစ်ဆေးခြင်း
                try:
                    if self.winfo_exists():
                        self.after(0, lambda: self.update_row_only(data))
                except:
                    pass # Window ပိတ်သွားရင် ဘာမှမလုပ်တော့ပါ
        except Exception as e:
            print(f"⚠️ Socket Error: Check if Server is running at 192.168.100.137:5000")

    def update_row_only(self, data):
        # UI update မလုပ်ခင် widget ရှိမရှိ ထပ်စစ်ပါ
        if not self.winfo_exists():
            return
            
        try:
            target_id = str(data.get('user_id'))
            new_status = str(data.get('status')).upper()
            icon = "🟢" if new_status == "ACTIVE" else "🟡" if new_status == "AWAY" else "🔴"
            
            # Treeview မှာ item ရှိမရှိ အရင်စစ်ပါ
            items = self.tree.get_children()
            if not items: return

            for item in items:
                row_values = self.tree.item(item)['values']
                if row_values and str(row_values[0]) == target_id:
                    self.tree.set(item, column="status", value=f"{icon} {new_status}")
                    self.tree.item(item, tags=("normal", new_status))
                    break
        except Exception as e:
            print(f"⚠️ Row Update Error: {e}")

    # def update_row_only(self, data):
    #     try:
    #         if not self.winfo_exists(): return
    #         target_id = str(data.get('user_id'))
    #         new_status = str(data.get('status')).upper()
    #         icon = "🟢" if new_status == "ACTIVE" else "🟡" if new_status == "AWAY" else "🔴"
    #         for item in self.tree.get_children():
    #             if str(self.tree.item(item)['values'][0]) == target_id:
    #                 self.tree.set(item, column="status", value=f"{icon} {new_status}")
    #                 self.tree.item(item, tags=("normal", new_status))
    #                 break
    #     except Exception as e:
    #         print(f"⚠️ Row Update Error: {e}")

    def __del__(self):
        try:
            if hasattr(self, 'sio') and self.sio.connected:
                self.sio.disconnect()
        except:
            pass