import customtkinter as ctk
from database import Database
from Admin.admin_menu import AdminMenu
from Leader.leader_menu import LeaderMenu
from Member.member_menu import MemberMenu
from tkinter import messagebox

class Dashboard(ctk.CTk):
    def __init__(self, user_data):
        super().__init__()
        self.title("WorkSync - Modern Dashboard")
        self.geometry("1100x700")
        self.db = Database()
        self.user = user_data

        # --- 1. Top Header ---
        self.setup_header()

        # --- 2. Left Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1F1F1F")
        self.sidebar.pack(side="left", fill="y")
        
        # --- 3. Main Content Area ---
        self.main_view = ctk.CTkFrame(self, fg_color="#181818", corner_radius=0)
        self.main_view.pack(side="right", expand=True, fill="both")

        # --- 4. Sidebar MENU Label ---
        ctk.CTkLabel(self.sidebar, text="MENU", font=("Arial", 11, "bold"), text_color="gray70").pack(anchor="w", padx=20, pady=(30, 10))
        
        # Role Content Load လုပ်ခြင်း
        self.load_role_content(user_data)

        # Bottom Switch & Logout
        self.setup_bottom_sidebar()
        
    def setup_header(self):
        """Header Area with Logo and Status Counts"""
        header_frame = ctk.CTkFrame(self, fg_color="#181818", height=60, corner_radius=0)
        header_frame.pack(side="top", fill="x")

        # Logo (Left Side)
        ctk.CTkLabel(header_frame, text="⚡ WorkSync", font=("Arial", 22, "bold"), text_color="white").pack(side="left", padx=20)

        # User Info (Right Side)
        user_info = f"👤 {self.user['full_name']} | {self.user['role'].upper()}"
        ctk.CTkLabel(header_frame, text=user_info, font=("Arial", 13)).pack(side="right", padx=20)

        # --- Office/WFH Count (Status Header ကို ဒီနေရာမှာ ခေါ်သုံးရပါမယ်) ---
        self.create_status_header(header_frame)

    def create_status_header(self, parent_frame):
        """Image (6) ပါအတိုင်း Office/WFH အရေအတွက်ကို Header မှာ ပြသခြင်း"""
        try:
            # Database မှ data ယူခြင်း (Database class ထဲမှာ get_status_counts ရှိဖို့လိုပါတယ်)
            off_count, wfh_count = self.db.get_status_counts()
        except:
            off_count, wfh_count = 0, 0 # Error တက်ရင် 0 ပြရန်

        # Container Frame
        status_f = ctk.CTkFrame(parent_frame, fg_color="transparent")
        status_f.pack(side="right", padx=30)

        # Office Label
        ctk.CTkLabel(status_f, text="🏢 Office:", font=("Arial", 13, "bold"), text_color="#2ECC71").pack(side="left")
        ctk.CTkLabel(status_f, text=str(off_count), font=("Arial", 13, "bold"), text_color="#2ECC71").pack(side="left", padx=(5, 15))

        # WFH Label
        ctk.CTkLabel(status_f, text="🏠 WFH:", font=("Arial", 13, "bold"), text_color="#3498DB").pack(side="left")
        ctk.CTkLabel(status_f, text=str(wfh_count), font=("Arial", 13, "bold"), text_color="#3498DB").pack(side="left", padx=5)

    def load_role_content(self, user):
        role = user['role'].lower()
        if role == 'admin':
            self.menu_logic = AdminMenu(self.sidebar, self.main_view, user)
        elif role == 'leader':
            self.menu_logic = LeaderMenu(self.sidebar, self.main_view, user)
        else:
            self.menu_logic = MemberMenu(self.sidebar, self.main_view, user)

    def setup_bottom_sidebar(self):
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=20)

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
            text_color="#E74C3C", hover_color="#2b2b2b", anchor="w",
            command=self.logout_event
        )
        self.logout_btn.pack(fill="x")

    def update_status(self, value):
        clean_value = "Office" if "Office" in value else "WFH"
        try:
            self.db.cursor.execute("UPDATE users SET current_status = %s WHERE id = %s", (clean_value, self.user['id']))
            self.db.conn.commit()
            # Status ပြောင်းပြီးရင် အပေါ်က Count တွေကိုပါ Refresh ဖြစ်စေချင်ရင် App ကို ပြန်ပွင့်ခိုင်းလို့ရပါတယ်
        except Exception as e:
            print(f"Update error: {e}")

    def logout_event(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            from main import LoginApp 
            self.destroy()
            app = LoginApp()
            app.mainloop()