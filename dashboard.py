import customtkinter as ctk
from database import Database
from Admin.admin_menu import AdminMenu
from Leader.leader_menu import LeaderMenu
from Member.member_menu import MemberMenu
from attendance_manager import AttendanceManager
from tkinter import messagebox
from member_tracking import MemberTracking
import datetime

class Dashboard(ctk.CTk):
    def __init__(self, user_data):
        super().__init__()
        
        # --- Window Configuration ---
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue")
        self.title("GIC Myanmar Work From Home Tracker")
        
        self.geometry("1100x700")
        self.minsize(1000, 650)
        
        self.db = Database()
        self.user = user_data
        self.tracker = None
        self.att_manager = AttendanceManager(self.db, self.user['id'], self.user['role'])

        # --- Top Header ---
        self.header_frame = ctk.CTkFrame(
            self, height=65, corner_radius=0,
            fg_color=("#FFFFFF", "#181818"),
            border_width=1, border_color=("#E0E0E0", "#2B2B2B")
        )
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)

        # --- Main Body Container ---
        self.container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.container.pack(side="top", expand=True, fill="both")

        # --- Sidebar Layout ---
        self.sidebar_container = ctk.CTkFrame(
            self.container, width=240, corner_radius=0, 
            fg_color=("#FFFFFF", "#1F1F1F"), 
            border_width=1, border_color=("#E0E0E0", "#2B2B2B")
        )
        self.sidebar_container.pack(side="left", fill="y")
        self.sidebar_container.pack_propagate(False)

        # 1. FIXED BOTTOM AREA (Buttons that don't move)
        self.fixed_bottom_sidebar = ctk.CTkFrame(
            self.sidebar_container, 
            fg_color="transparent",
            corner_radius=0
        )
        self.fixed_bottom_sidebar.pack(side="bottom", fill="x", padx=10, pady=(0, 20))

        # 2. SCROLLABLE TOP AREA (Menus)
        self.sidebar_scroll = ctk.CTkScrollableFrame(
            self.sidebar_container, 
            fg_color="transparent", 
            corner_radius=0,
            label_text=""
        )
        self.sidebar_scroll.pack(side="top", fill="both", expand=True)

        # --- Main View Area ---
        self.main_view = ctk.CTkFrame(
            self.container, fg_color=("#F5F7FA", "#181818"), 
            corner_radius=0
        )
        self.main_view.pack(side="right", expand=True, fill="both")

        # --- Initialize Components ---
        self.setup_header()
        self.load_role_content(user_data) 
        self.setup_bottom_sidebar() # Populates the fixed frame
        self.sync_leader_schedule()
        self.update_attendance_ui(self.att_manager.is_checked_in)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_header(self):
        for widget in self.header_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.header_frame, text="GIC Myanmar", 
            font=("Arial", 22, "bold"), 
            text_color=("#1F538D", "#3498DB")
        ).pack(side="left", padx=25)

        role_info = f"👤 {self.user['full_name']}  |  [{self.user['role'].upper()}]"
        ctk.CTkLabel(
            self.header_frame, text=role_info, 
            font=("Arial", 13, "bold"),
            text_color=("#333333", "#D1D1D1")
        ).pack(side="right", padx=25)

        self.create_status_header(self.header_frame)

    def create_status_header(self, parent_frame):
        try: off_count, wfh_count = self.db.get_status_counts()
        except: off_count, wfh_count = 0, 0 

        status_f = ctk.CTkFrame(parent_frame, fg_color="transparent")
        status_f.pack(side="right", padx=30)

        ctk.CTkLabel(status_f, text="🏢 Office:", font=("Arial", 12, "bold"), text_color="#2ECC71").pack(side="left")
        ctk.CTkLabel(status_f, text=str(off_count), font=("Arial", 12, "bold")).pack(side="left", padx=(5, 15))

        ctk.CTkLabel(status_f, text="🏠 WFH:", font=("Arial", 12, "bold"), text_color="#3498DB").pack(side="left")
        ctk.CTkLabel(status_f, text=str(wfh_count), font=("Arial", 12, "bold")).pack(side="left", padx=5)

    def setup_bottom_sidebar(self):
        """Populates the fixed bottom frame that does not scroll"""
        bottom_frame = self.fixed_bottom_sidebar

        # Visual Separator line
        ctk.CTkFrame(bottom_frame, height=2, fg_color=("#E0E0E0", "#2B2B2B")).pack(fill="x", pady=(0, 15))

        # Attendance Section
        ctk.CTkLabel(bottom_frame, text="ATTENDANCE CONTROL", font=("Arial", 10, "bold"), text_color="gray").pack(anchor="w", padx=5)
        
        self.attendance_btn = ctk.CTkButton(
            bottom_frame, text="📍 Check-in Now", 
            fg_color=("#2ECC71", "#27AE60"), text_color="white",
            height=40, font=("Arial", 13, "bold"), command=self.toggle_attendance
        )
        self.attendance_btn.pack(fill="x", pady=(8, 15))

        # Work Mode Section
        ctk.CTkLabel(bottom_frame, text="CURRENT WORK MODE", font=("Arial", 10, "bold"), text_color="gray").pack(anchor="w", padx=5)
        
        self.status_switch = ctk.CTkSegmentedButton(
            bottom_frame, values=["🏢 Office", "🏠 WFH"],
            font=("Arial", 12, "bold"),
            command=self.manual_status_change
        )
        self.status_switch.pack(fill="x", pady=(8, 15))

        # Theme Switch
        self.theme_switch = ctk.CTkSwitch(bottom_frame, text="Dark Mode", font=("Arial", 12), command=self.change_appearance_mode)
        self.theme_switch.select()
        self.theme_switch.pack(pady=5, padx=5, anchor="w")

        # Logout
        self.logout_btn = ctk.CTkButton(
            bottom_frame, text="🚪 Logout Account", 
            fg_color="transparent", border_width=1, border_color="#E74C3C",
            text_color="#E74C3C", hover_color=("#FADBD8", "#2C1A1A"),
            height=35, font=("Arial", 12, "bold"), command=self.logout_event
        )
        self.logout_btn.pack(fill="x", pady=(15, 0))

    def update_attendance_ui(self, is_checked_in):
        if is_checked_in:
            self.attendance_btn.configure(text="🚩 Check-out", fg_color="#E74C3C", hover_color="#C0392B")
            if self.tracker: self.tracker.set_tracking_state(True)
        else:
            self.attendance_btn.configure(text="📍 Check-in Now", fg_color=("#2ECC71", "#27AE60"))
            if self.tracker: self.tracker.set_tracking_state(False)

    def toggle_attendance(self):
        current_val = self.status_switch.get()
        location = "WFH" if "🏠" in current_val or "WFH" in current_val else "Office"
        self.att_manager.handle_toggle(location, self.update_attendance_ui)
        self.setup_header()

    def manual_status_change(self, selected_value):
        if self.user['role'].lower() == 'member': return
        new_status = "Office" if "Office" in selected_value else "WFH"
        try:
            self.db.ensure_connection()
            query = "UPDATE users SET current_status = %s WHERE id = %s"
            self.db.cursor.execute(query, (new_status, self.user['id']))
            self.db.conn.commit()
            self.setup_header() 
        except: pass

    def sync_leader_schedule(self):
        today = datetime.date.today().strftime('%Y-%m-%d')
        try:
            self.db.ensure_connection()
            if self.user['role'].lower() == 'member':
                self.db.cursor.execute(
                    "SELECT status FROM wfh_schedules WHERE user_id = %s AND schedule_date = %s", 
                    (self.user['id'], today)
                )
                res = self.db.cursor.fetchone()
                status = res['status'] if res else "Office"
                self.status_switch.set("🏢 Office" if status == "Office" else "🏠 WFH")
                self.status_switch.configure(state="disabled")
            else:
                self.db.cursor.execute("SELECT current_status FROM users WHERE id = %s", (self.user['id'],))
                res = self.db.cursor.fetchone()
                status = res['current_status'] if res and res['current_status'] else "Office"
                self.status_switch.set("🏢 Office" if status == "Office" else "🏠 WFH")
        except: pass

    def change_appearance_mode(self):
        mode = "dark" if self.theme_switch.get() == 1 else "light"
        ctk.set_appearance_mode(mode)

    def load_role_content(self, user):
        role = user['role'].lower()
        if role == 'admin': 
            self.menu_logic = AdminMenu(self.sidebar_scroll, self.main_view, user)
        elif role == 'leader': 
            self.menu_logic = LeaderMenu(self.sidebar_scroll, self.main_view, user)
        else: 
            self.tracker = MemberTracking(user_id=user['id'], server_url="http://192.168.100.83:5000")
            self.tracker.set_tracking_state(False) 
            self.menu_logic = MemberMenu(self.sidebar_scroll, self.main_view, user)

    def on_closing(self):
        if self.tracker: self.tracker.stop()
        self.destroy()

    def logout_event(self):
        if messagebox.askyesno("Logout", "Are you sure?"):
            self.on_closing()
            from main import LoginApp
            LoginApp().mainloop()