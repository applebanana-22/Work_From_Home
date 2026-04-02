import customtkinter as ctk
from database import Database
from Admin.admin_menu import AdminMenu
from Leader.leader_menu import LeaderMenu
from Member.member_menu import MemberMenu
from tkinter import messagebox

class Dashboard(ctk.CTk):
    def __init__(self, user_data):
        super().__init__()
        
        # --- Default Theme Settings ---
        # Starts in Dark Mode, but can be changed by the user
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue")
        
        self.title("WorkSync - Modern Dashboard")
        self.geometry("1100x700")
        self.db = Database()
        self.user = user_data
        
        # --- 1. Top Header ---
        self.setup_header()

        # --- 2. Left Sidebar ---
        # Using adaptive colors: Light mode (#FFFFFF) / Dark mode (#1F1F1F)
        self.sidebar = ctk.CTkFrame(
            self, width=220, corner_radius=0, 
            fg_color=("#FFFFFF", "#1F1F1F"), 
            border_width=1, border_color=("#E0E0E0", "#2B2B2B")
        )
        self.sidebar.pack(side="left", fill="y")
        
        # --- 3. Main Content Area ---
        # Using adaptive colors: Light mode (#F5F7FA) / Dark mode (#181818)
        self.main_view = ctk.CTkFrame(self, fg_color=("#F5F7FA", "#181818"), corner_radius=0)
        self.main_view.pack(side="right", expand=True, fill="both")

        # Sidebar MENU Label
        ctk.CTkLabel(
            self.sidebar, text="MAIN MENU", 
            font=("Arial", 11, "bold"), text_color="gray70"
        ).pack(anchor="w", padx=25, pady=(30, 10))
        
        # Role Content Load
        self.load_role_content(user_data)

        # Bottom Switch, Theme Toggle & Logout
        self.setup_bottom_sidebar()
        
    def setup_header(self):
        """Header Area with Adaptive Colors"""
        header_frame = ctk.CTkFrame(
            self, height=60, corner_radius=0,
            fg_color=("#FFFFFF", "#181818"),
            border_width=1, border_color=("#E0E0E0", "#2B2B2B")
        )
        header_frame.pack(side="top", fill="x")

        # Logo
        ctk.CTkLabel(
            header_frame, text="⚡ WorkSync", 
            font=("Arial", 22, "bold"), text_color=("#3498DB", "white")
        ).pack(side="left", padx=25)

        # User Info
        user_info = f"👤 {self.user['full_name']} | {self.user['role'].upper()}"
        ctk.CTkLabel(
            header_frame, text=user_info, 
            font=("Arial", 13, "bold")
        ).pack(side="right", padx=25)

        self.create_status_header(header_frame)

    def create_status_header(self, parent_frame):
        try:
            off_count, wfh_count = self.db.get_status_counts()
        except:
            off_count, wfh_count = 0, 0 

        status_f = ctk.CTkFrame(parent_frame, fg_color="transparent")
        status_f.pack(side="right", padx=30)

        ctk.CTkLabel(status_f, text="🏢 Office:", font=("Arial", 13, "bold"), text_color="#2ECC71").pack(side="left")
        ctk.CTkLabel(status_f, text=str(off_count), font=("Arial", 13, "bold")).pack(side="left", padx=(5, 15))

        ctk.CTkLabel(status_f, text="🏠 WFH:", font=("Arial", 13, "bold"), text_color="#3498DB").pack(side="left")
        ctk.CTkLabel(status_f, text=str(wfh_count), font=("Arial", 13, "bold")).pack(side="left", padx=5)

    def setup_bottom_sidebar(self):
        """Includes the Mode Switcher and Logout"""
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", padx=15, pady=20)

        # --- THEME SWITCHER ---
        ctk.CTkLabel(bottom_frame, text="Appearance", font=("Arial", 11, "bold"), text_color="gray70").pack(anchor="w", padx=5)
        
        self.theme_switch = ctk.CTkSwitch(
            bottom_frame, text="Dark Mode", 
            command=self.change_appearance_mode,
            progress_color="#3498DB"
        )
        self.theme_switch.select() # Default to Dark
        self.theme_switch.pack(pady=(5, 15), padx=5, anchor="w")

        # --- STATUS SWITCHER ---
        ctk.CTkLabel(bottom_frame, text="Your Status", font=("Arial", 11, "bold"), text_color="gray70").pack(anchor="w", padx=5)
        
        self.status_switch = ctk.CTkSegmentedButton(
            bottom_frame, 
            values=["🏢 Office", "🏠 WFH"],
            command=self.update_status,
            selected_color="#1E8449"
        )
        self.status_switch.pack(fill="x", pady=(5, 15))
        
        current = self.user.get('current_status', 'Office')
        self.status_switch.set("🏢 Office" if current == "Office" else "🏠 WFH")

        self.logout_btn = ctk.CTkButton(
            bottom_frame, text="🚪 Logout", fg_color="transparent", 
            text_color="#E74C3C", hover_color=("#FADBD8", "#2B2B2B"), anchor="w",
            command=self.logout_event
        )
        self.logout_btn.pack(fill="x")

    def change_appearance_mode(self):
        """Switches between Light and Dark mode"""
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="Light Mode")

    def load_role_content(self, user):
        role = user['role'].lower()
        if role == 'admin':
            self.menu_logic = AdminMenu(self.sidebar, self.main_view, user)
        elif role == 'leader':
            self.menu_logic = LeaderMenu(self.sidebar, self.main_view, user)
        else:
            self.menu_logic = MemberMenu(self.sidebar, self.main_view, user)

    def update_status(self, value):
        clean_value = "Office" if "Office" in value else "WFH"
        try:
            self.db.cursor.execute("UPDATE users SET current_status = %s WHERE id = %s", (clean_value, self.user['id']))
            self.db.conn.commit()
        except Exception as e:
            print(f"Update error: {e}")

    def logout_event(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            from main import LoginApp 
            self.destroy()
            app = LoginApp()
            app.mainloop()