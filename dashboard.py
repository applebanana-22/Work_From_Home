import customtkinter as ctk
from database import Database
from Admin.admin_menu import AdminMenu
from Leader.leader_menu import LeaderMenu
from Member.member_menu import MemberMenu
from attendance_manager import AttendanceManager
from tkinter import messagebox
import datetime

class Dashboard(ctk.CTk):
    def __init__(self, user_data):
        super().__init__()
        
        # --- Window & Theme Configuration ---
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue")
        self.title("WorkSync - Modern Dashboard")
        self.geometry("1100x700")
        
        self.db = Database()
        self.user = user_data
        self.att_manager = AttendanceManager(self.db, self.user['id'])

        # --- Layout Structure (Matching Screenshot Position) ---
        
        # 1. Top Header Bar (Window တစ်ခုလုံး၏ အပေါ်ဆုံးတွင် ပုံသေထားရှိခြင်း)
        self.header_frame = ctk.CTkFrame(
            self, height=60, corner_radius=0,
            fg_color=("#FFFFFF", "#181818"),
            border_width=1, border_color=("#E0E0E0", "#2B2B2B")
        )
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)

        # 2. Main Container (Sidebar နှင့် Content အတွက်)
        self.container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.container.pack(side="top", expand=True, fill="both")

        # 3. Sidebar (ဘယ်ဘက်ခြမ်းတွင် အပေါ်မှအောက်ခြေထိ နေရာယူခြင်း)
        self.sidebar = ctk.CTkFrame(
            self.container, width=220, corner_radius=0, 
            fg_color=("#FFFFFF", "#1F1F1F"), 
            border_width=1, border_color=("#E0E0E0", "#2B2B2B")
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # 4. Content Area (ညာဘက်ခြမ်း Dynamic View အတွက်)
        self.main_view = ctk.CTkFrame(
            self.container, fg_color=("#F5F7FA", "#181818"), 
            corner_radius=0
        )
        self.main_view.pack(side="right", expand=True, fill="both")

        # --- Initialize Components ---
        self.setup_header()
        self.load_role_content(user_data)
        self.setup_bottom_sidebar()
        self.sync_leader_schedule()

    def setup_header(self):
        """Header Widgets များကို Refresh လုပ်ရုံသာပြုလုပ်ပြီး Position မရွေ့စေရန် Fix လုပ်ထားပါသည်"""
        for widget in self.header_frame.winfo_children():
            widget.destroy()

        # Logo Section
        ctk.CTkLabel(
            self.header_frame, text="⚡ WorkSync", 
            font=("Arial", 22, "bold"), 
            text_color=("#3498DB", "#FFFFFF")
        ).pack(side="left", padx=25)

        # Right Side Info
        user_info = f"👤 {self.user['full_name']} | {self.user['role'].upper()}"
        ctk.CTkLabel(
            self.header_frame, text=user_info, 
            font=("Arial", 13, "bold"),
            text_color=("#1A1A1A", "#FFFFFF")
        ).pack(side="right", padx=25)

        # Live Status Counters (Screenshot အတိုင်း အရောင်ခွဲထားပါသည်)
        self.create_status_header(self.header_frame)

    def create_status_header(self, parent_frame):
        try: off_count, wfh_count = self.db.get_status_counts()
        except: off_count, wfh_count = 0, 0 

        status_f = ctk.CTkFrame(parent_frame, fg_color="transparent")
        status_f.pack(side="right", padx=30)

        ctk.CTkLabel(status_f, text="🏢 Office:", font=("Arial", 13, "bold"), text_color="#2ECC71").pack(side="left")
        ctk.CTkLabel(status_f, text=str(off_count), font=("Arial", 13, "bold"), text_color="#2ECC71").pack(side="left", padx=(5, 15))

        ctk.CTkLabel(status_f, text="🏠 WFH:", font=("Arial", 13, "bold"), text_color="#3498DB").pack(side="left")
        ctk.CTkLabel(status_f, text=str(wfh_count), font=("Arial", 13, "bold"), text_color="#3498DB").pack(side="left", padx=5)

    def setup_bottom_sidebar(self):
        """Sidebar အောက်ခြေရှိ Control များ (Manual Status Change ပါဝင်ပါသည်)"""
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", padx=15, pady=20)

        # Attendance Button
        ctk.CTkLabel(bottom_frame, text="Attendance", font=("Arial", 11, "bold"), text_color=("#666666", "#AAAAAA")).pack(anchor="w", padx=5)
        self.attendance_btn = ctk.CTkButton(
            bottom_frame, text="📍 Check-in Now", 
            fg_color=("#2ECC71", "#27AE60"), text_color=("#121212", "#E0E0E0"),
            height=35, font=("Arial", 12, "bold"), command=self.toggle_attendance
        )
        self.attendance_btn.pack(fill="x", pady=(5, 15))

        # Status Switch (Admin/Leader အတွက်သာ)
        ctk.CTkLabel(bottom_frame, text="Assigned Schedule", font=("Arial", 11, "bold"), text_color=("#666666", "#AAAAAA")).pack(anchor="w", padx=5)
        
        is_member = self.user['role'].lower() == 'member'
        self.status_switch = ctk.CTkSegmentedButton(
            bottom_frame, values=["🏢 Office", "🏠 WFH"],
            font=("Arial", 12, "bold"),
            unselected_color=("#E0E0E0", "#121212"),
            text_color=("#1A1A1A", "#FFFFFF"),
            state="normal" if not is_member else "disabled",
            command=self.manual_status_change if not is_member else None
        )
        self.status_switch.pack(fill="x", pady=(5, 15))

        # Utilities
        self.theme_switch = ctk.CTkSwitch(
            bottom_frame, text="Dark Mode", command=self.change_appearance_mode,
            progress_color="#3498DB", text_color=("#1A1A1A", "#FFFFFF")
        )
        self.theme_switch.select()
        self.theme_switch.pack(pady=(5, 10), padx=5, anchor="w")

        self.logout_btn = ctk.CTkButton(
            bottom_frame, text="🚪 Logout", fg_color="transparent", 
            text_color=("#E74C3C", "#FF6B6B"), hover_color=("#FADBD8", "#2B2B2B"), 
            anchor="w", command=self.logout_event
        )
        self.logout_btn.pack(fill="x")

    def manual_status_change(self, selected_value):
        """Admin/Leader များ Status ပြောင်းလိုက်လျှင် Database တွင် သိမ်းဆည်းပြီး UI Update လုပ်ခြင်း"""
        # 1. ရွေးချယ်လိုက်တဲ့ Value ပေါ်မူတည်ပြီး Status string ကို သတ်မှတ်ခြင်း
        new_status = "Office" if "Office" in selected_value else "WFH"
        
        # 2. Button အရောင်ကို Office ဆိုလျှင် အစိမ်း၊ WFH ဆိုလျှင် အပြာ ပြောင်းလဲခြင်း
        color = ("#2ECC71", "#2ECC71") if new_status == "Office" else ("#3498DB", "#1FAEE9")
        self.status_switch.configure(selected_color=color)

        try:
            # 3. Database ရှိ users table တွင် current_status ကို UPDATE လုပ်ခြင်း
            # SQL: UPDATE users SET current_status = 'Office' WHERE id = 123
            query = "UPDATE users SET current_status = %s WHERE id = %s"
            self.db.cursor.execute(query, (new_status, self.user['id']))
            self.db.conn.commit()

            # 4. Header ရှိ Office/WFH counter များကို တစ်ခါတည်း Refresh လုပ်ပေးခြင်း
            self.setup_header()
            
            print(f"Success: Status updated to {new_status} in database.")
            
        except Exception as e:
            # Error တက်ခဲ့လျှင် (ဥပမာ- Database Connection ကျသွားလျှင်) rollback လုပ်ရန်
            self.db.conn.rollback()
            print(f"Database Error: {e}")
            messagebox.showerror("Update Error", "Failed to save status change to database.")

    def sync_leader_schedule(self):
        """Database မှ လက်ရှိ status အား UI တွင် ထင်ဟပ်စေခြင်း"""
        today = datetime.date.today().strftime('%Y-%m-%d')
        role = self.user['role'].lower()
        try:
            if role == 'member':
                self.db.cursor.execute("SELECT status FROM wfh_schedules WHERE user_id = %s AND schedule_date = %s", (self.user['id'], today))
                res = self.db.cursor.fetchone()
                status = res['status'] if res else "Office"
            else:
                self.db.cursor.execute("SELECT current_status FROM users WHERE id = %s", (self.user['id'],))
                res = self.db.cursor.fetchone()
                status = res['current_status'] if res and res['current_status'] else "Office"

            self.status_switch.configure(state="normal")
            self.status_switch.set("🏢 Office" if status == "Office" else "🏠 WFH")
            color = ("#2ECC71", "#2ECC71") if status == "Office" else ("#3498DB", "#1FAEE9")
            self.status_switch.configure(selected_color=color)
            if role == 'member': self.status_switch.configure(state="disabled", text_color_disabled=("#1A1A1A", "#FFFFFF"))
        except:
            self.status_switch.set("🏢 Office")

    def toggle_attendance(self):
        location = "Office" if "Office" in self.status_switch.get() else "WFH"
        self.att_manager.handle_toggle(location, self.update_attendance_ui)

    def update_attendance_ui(self, is_checked_in):
        if is_checked_in:
            self.attendance_btn.configure(text="🚩 Check-out", fg_color="#E74C3C")
        else:
            self.attendance_btn.configure(text="📍 Check-in Now", fg_color=("#2ECC71", "#27AE60"))

    def change_appearance_mode(self):
        mode = "dark" if self.theme_switch.get() == 1 else "light"
        ctk.set_appearance_mode(mode)
        self.theme_switch.configure(text=f"{mode.capitalize()} Mode")

    def load_role_content(self, user):
        role = user['role'].lower()
        if role == 'admin': self.menu_logic = AdminMenu(self.sidebar, self.main_view, user)
        elif role == 'leader': self.menu_logic = LeaderMenu(self.sidebar, self.main_view, user)
        else: self.menu_logic = MemberMenu(self.sidebar, self.main_view, user)

    def logout_event(self):
        if messagebox.askyesno("Logout", "Are you sure?"):
            self.destroy()
            from main import LoginApp
            LoginApp().mainloop()