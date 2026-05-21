import customtkinter as ctk
from tkinter import ttk
import socketio
from database import Database

class LeaderDashboard(ctk.CTkFrame):
    def __init__(self, parent, user, db=None):
        # Auto-updating background for the frame itself
        super().__init__(parent, fg_color=("#FFFFFF", "#000000"))
        
        self.user = user  
        self.db = db if db else Database() 
        self.sio = socketio.Client(reconnection=True, reconnection_delay=5)
        
        self.setup_ui()
        self.load_initial_data() 
        self.connect_tracking_server()

        # FORCE REFRESH ON THEME CHANGE
        # This detects the mode change immediately and updates the Treeview colors
        self.bind("<Expose>", lambda e: self.apply_treeview_style())

    def setup_ui(self):
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=30, pady=(30, 10))
        
        ctk.CTkLabel(
            self.header, 
            text="Team Real-time Monitor", 
            font=("Segoe UI", 28, "bold"),
            text_color=("#000000", "#FFFFFF")
        ).pack(side="left")

        self.table_container = ctk.CTkFrame(
            self, fg_color=("#FFFFFF", "#000000"), corner_radius=15,
            border_width=1, border_color=("#D1D1D1", "#2B2B2B")
        )
        self.table_container.pack(fill="both", expand=True, padx=30, pady=20)

        info_cols = ("id", "name", "role", "wfh_office", "check_in", "check_out")
        self.info_tree = ttk.Treeview(self.table_container, columns=info_cols, show="headings")
        self.status_tree = ttk.Treeview(self.table_container, columns=("status",), show="headings")

        for col in info_cols:
            self.info_tree.heading(col, text=col.replace("_", " ").upper())
            self.info_tree.column(col, anchor="center", width=110)
        
        self.status_tree.heading("status", text="STATUS")
        self.status_tree.column("status", anchor="center", width=140)

        self.info_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        self.status_tree.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.apply_treeview_style()
        self.sync_scroll()

    def apply_treeview_style(self):
        """Redraws the Treeview style based on the current mode instantly."""
        style = ttk.Style()
        
        # Use 'clam' as it allows for better color overriding than 'default'
        style.theme_use("clam")

        is_dark = ctk.get_appearance_mode() == "Dark"
        
        tree_bg = "#000000" if is_dark else "#FFFFFF"
        tree_fg = "#FFFFFF" if is_dark else "#000000"
        header_bg = "#1A1A1A" if is_dark else "#F0F0F0"
        border_color = "#2B2B2B" if is_dark else "#D1D1D1"

        style.configure("Treeview", 
                        background=tree_bg, 
                        foreground=tree_fg, 
                        fieldbackground=tree_bg, 
                        rowheight=50, 
                        borderwidth=0)
        
        style.configure("Treeview.Heading", 
                        background=header_bg, 
                        foreground=tree_fg, 
                        relief="flat", 
                        font=("Segoe UI", 10, "bold"))
        
        # Override the border color for the widget
        style.configure("Treeview", bordercolor=border_color, lightcolor=tree_bg, darkcolor=tree_bg)

        # Selection colors
        style.map("Treeview", 
                  background=[('selected', '#2980B9')], 
                  foreground=[('selected', '#FFFFFF')])

        # Refresh status tags
        self.status_tree.tag_configure("ACTIVE", foreground="#2ECC71", font=("Segoe UI", 11, "bold")) 
        self.status_tree.tag_configure("AWAY", foreground="#F1C40F", font=("Segoe UI", 11, "bold"))    
        self.status_tree.tag_configure("OFFLINE", foreground="#E74C3C", font=("Segoe UI", 11, "bold"))

    def load_initial_data(self):
        try:
            for tree in [self.info_tree, self.status_tree]:
                tree.delete(*tree.get_children())
            
            # UPDATED QUERY: Fetches all members of the team OR anyone who is a team leader
            query = """
                SELECT u.id, u.employee_id, u.full_name, u.role, u.status,
                COALESCE(s.status, u.current_status, 'Office') AS mode,
                COALESCE(TIME_FORMAT(a.check_in, '%h:%i %p'), '---') AS in_t,
                COALESCE(TIME_FORMAT(a.check_out, '%h:%i %p'), '---') AS out_t
                FROM users u
                LEFT JOIN attendance a ON u.id = a.user_id AND a.attendance_date = CURDATE()
                LEFT JOIN wfh_schedules s ON u.id = s.user_id AND s.schedule_date = CURDATE()
                WHERE (u.team_id = (SELECT team_id FROM users WHERE employee_id = %s) AND u.role = 'member')
                   OR u.role = 'leader'
            """
            self.db.ensure_connection()
            self.db.cursor.execute(query, (self.user['employee_id'],))
            
            for m in self.db.cursor.fetchall():
                live = (m['status'] or "OFFLINE").upper()
                self.info_tree.insert("", "end", iid=str(m['id']), values=(m['employee_id'], m['full_name'], m['role'].upper(), m['mode'], m['in_t'], m['out_t']))
                self.status_tree.insert("", "end", iid=f"status_{m['id']}", values=(f"● {live}",), tags=(live,))
        except Exception as e:
            print(f"❌ Error: {e}")

    def update_row_only(self, data):
        if not self.winfo_exists(): return
        try:
            target_id = str(data.get('user_id'))
            new_status = str(data.get('status')).upper()
            status_iid = f"status_{target_id}"
            if self.status_tree.exists(status_iid):
                self.status_tree.set(status_iid, column="status", value=f"● {new_status}")
                self.status_tree.item(status_iid, tags=(new_status,))
        except: pass

    def sync_scroll(self):
        def on_tree_scroll(*args):
            self.info_tree.yview(*args)
            self.status_tree.yview(*args)
        self.scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=on_tree_scroll)
        self.info_tree.configure(yscrollcommand=self.scrollbar.set)
        self.status_tree.configure(yscrollcommand=self.scrollbar.set)

    def connect_tracking_server(self):
        try:
            if not self.sio.connected:
                self.sio.connect('http://192.168.100.45:5000', transports=['websocket']) 
            @self.sio.on("status_update")
            def on_update(data):
                # UI Destroy ဖြစ်မဖြစ်ကို အရင်စစ်ပြီးမှ အလုပ်ဆက်လုပ်ပါမယ်
                if hasattr(self, '_is_destroyed') and not self._is_destroyed:
                    try:
                        self.after(0, lambda: self.update_row_only(data))
                    except Exception:
                        pass
        except Exception as e: 
            print(f"Socket connection error: {e}")