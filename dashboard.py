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
        
        # --- Window & Theme Configuration ---
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue")
        self.title("WorkSync - Modern Dashboard")
        self.geometry("1100x700")
        
        self.db = Database()
        self.user = user_data
        
        self.att_manager = AttendanceManager(self.db, self.user['id'], self.user['role'])

        # --- Layout Structure ---
        self.header_frame = ctk.CTkFrame(
            self, height=60, corner_radius=0,
            fg_color=("#FFFFFF", "#181818"),
            border_width=1, border_color=("#E0E0E0", "#2B2B2B")
        )
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)

        self.container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.container.pack(side="top", expand=True, fill="both")

        self.sidebar = ctk.CTkFrame(
            self.container, width=220, corner_radius=0, 
            fg_color=("#FFFFFF", "#1F1F1F"), 
            border_width=1, border_color=("#E0E0E0", "#2B2B2B")
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

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
        self.update_attendance_ui(self.att_manager.is_checked_in)

    def setup_header(self):
        """Header with dynamic text colors for Light/Dark mode"""
        for widget in self.header_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.header_frame, text="⚡ WorkSync", 
            font=("Arial", 22, "bold"), 
            text_color=("#000000", "#FFFFFF")
        ).pack(side="left", padx=25)

        # Dynamic color for Profile Label: Black in Light, White in Dark
        profile_text_color = ("#000000", "#FFFFFF")
        role_label = f"👤 {self.user['full_name']} | [{self.user['role'].upper()}]"
        
        ctk.CTkLabel(
            self.header_frame, text=role_label, 
            font=("Arial", 13, "bold"),
            text_color=profile_text_color if self.user['role'].lower() == 'member' else ("#000000", "#FFFFFF")
        ).pack(side="right", padx=25)

        self.create_status_header(self.header_frame)

    def create_status_header(self, parent_frame):
        try: off_count, wfh_count = self.db.get_status_counts()
        except: off_count, wfh_count = 0, 0 

        status_f = ctk.CTkFrame(parent_frame, fg_color="transparent")
        status_f.pack(side="right", padx=30)

        ctk.CTkLabel(status_f, text="🏢 Office:", font=("Arial", 13, "bold"), text_color="#2ECC71").pack(side="left")
        ctk.CTkLabel(status_f, text=str(off_count), font=("Arial", 13, "bold"), text_color=("#000000", "#FFFFFF")).pack(side="left", padx=(5, 15))

        ctk.CTkLabel(status_f, text="🏠 WFH:", font=("Arial", 13, "bold"), text_color="#3498DB").pack(side="left")
        ctk.CTkLabel(status_f, text=str(wfh_count), font=("Arial", 13, "bold"), text_color=("#000000", "#FFFFFF")).pack(side="left", padx=5)

    def setup_bottom_sidebar(self):
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", padx=15, pady=20)

        ctk.CTkLabel(bottom_frame, text="Attendance", font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w", padx=5)
        
        # Initializing button with dynamic text color
        self.attendance_btn = ctk.CTkButton(
            bottom_frame, text="📍 Check-in Now", 
            fg_color=("#2ECC71", "#27AE60"), 
            text_color=("#000000", "#FFFFFF"),
            height=38, font=("Arial", 12, "bold"), command=self.toggle_attendance
        )
        self.attendance_btn.pack(fill="x", pady=(5, 15))

        ctk.CTkLabel(bottom_frame, text="Current Work Mode", font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w", padx=5)
        
        is_member = self.user['role'].lower() == 'member'
        self.status_switch = ctk.CTkSegmentedButton(
            bottom_frame, values=["🏢 Office", "🏠 WFH"],
            font=("Arial", 12, "bold"),
            text_color=("#000000", "#FFFFFF"),
            state="normal" if not is_member else "disabled",
            command=self.manual_status_change if not is_member else None
        )
        self.status_switch.pack(fill="x", pady=(5, 15))

        self.theme_switch = ctk.CTkSwitch(bottom_frame, text="Dark Mode", command=self.change_appearance_mode)
        self.theme_switch.select()
        self.theme_switch.pack(pady=(5, 10), padx=5, anchor="w")

        self.logout_btn = ctk.CTkButton(
            bottom_frame, text="🚪 Logout", fg_color="transparent", 
            text_color="#E74C3C", anchor="w", command=self.logout_event
        )
        self.logout_btn.pack(fill="x")

    def apply_segmented_style(self, status):
        """Logic for Office (Green) and WFH (Blue) with Mode-Aware Text"""
        if status == "Office":
            bg_color = ("#2ECC71", "#2ECC71")
        else:
            bg_color = ("#3498DB", "#1FAEE9")

        # Fixed: selected text stays white/black based on mode
        self.status_switch.configure(
            selected_color=bg_color,
            text_color=("#000000", "#FFFFFF")
        )

    def update_attendance_ui(self, is_checked_in):
        """Updates Attendance button text color dynamically for Light/Dark mode"""
        if is_checked_in:
            self.attendance_btn.configure(
                text="🚩 Check-out", 
                fg_color="#E74C3C", 
                hover_color="#C0392B", 
                text_color=("#000000", "#FFFFFF") # Always white on red for visibility
            )
        else:
            self.attendance_btn.configure(
                text="📍 Check-in Now", 
                fg_color=("#2ECC71", "#27AE60"), 
                text_color=("#000000", "#FFFFFF") # Dynamic text
            )

    def toggle_attendance(self):
        location = "Office" if "Office" in self.status_switch.get() else "WFH"
        self.att_manager.handle_toggle(location, self.update_attendance_ui)
        self.setup_header()

    def manual_status_change(self, selected_value):
        new_status = "Office" if "Office" in selected_value else "WFH"
        try:
            query = "UPDATE users SET current_status = %s WHERE id = %s"
            self.db.cursor.execute(query, (new_status, self.user['id']))
            self.db.conn.commit()
            self.apply_segmented_style(new_status)
            self.setup_header() 
        except:
            self.db.conn.rollback()

    def sync_leader_schedule(self):
        today = datetime.date.today().strftime('%Y-%m-%d')
        role = self.user['role'].lower()
        
        try:
            if role == 'member':
                self.db.cursor.execute(
                    "SELECT status FROM wfh_schedules WHERE user_id = %s AND schedule_date = %s", 
                    (self.user['id'], today)
                )
                res = self.db.cursor.fetchone()
                status = res['status'] if res else "Office"
                
                self.status_switch.configure(state="normal")
                self.status_switch.set("🏢 Office" if status == "Office" else "🏠 WFH")
                self.apply_segmented_style(status)
                self.status_switch.configure(state="disabled")
            else:
                self.db.cursor.execute("SELECT current_status FROM users WHERE id = %s", (self.user['id'],))
                res = self.db.cursor.fetchone()
                status = res['current_status'] if res and res['current_status'] else "Office"
                
                self.status_switch.set("🏢 Office" if status == "Office" else "🏠 WFH")
                self.apply_segmented_style(status)
        except Exception as e:
            self.status_switch.set("🏢 Office")
            self.apply_segmented_style("Office")

    def change_appearance_mode(self):
        mode = "dark" if self.theme_switch.get() == 1 else "light"
        ctk.set_appearance_mode(mode)
        # Refresh header to apply new dynamic text colors immediately
        self.setup_header()

    # ဖိုင်ရဲ့အပေါ်ဆုံးမှာ import အရင်လုပ်ပါ


    def load_role_content(self, user):
        role = user['role'].lower()
        if role == 'admin': 
            self.menu_logic = AdminMenu(self.sidebar, self.main_view, user)
        elif role == 'leader': 
            self.menu_logic = LeaderMenu(self.sidebar, self.main_view, user)
        else: 
            # --- Member ဖြစ်ခဲ့လျှင် Tracking ကို ဒီမှာ စဖွင့်မည် ---
            print(f"🚀 Initializing tracking for: {user['full_name']}")
            
            # Database ထဲက employee_id (သို့မဟုတ် id) ကို သုံးပြီး tracker စဖွင့်ခြင်း
            # server_url နေရာတွင် သင့် Server Laptop ၏ IP ကို ထည့်ရန် မမေ့ပါနှင့်
            self.tracker = MemberTracking(
                user_id=user['id'], 
                server_url="http://172.19.135.113:5000" # <-- ဒီနေရာမှာ Server IP ပြင်ပါ
            )
            
            self.menu_logic = MemberMenu(self.sidebar, self.main_view, user)

    def logout_event(self):
        if messagebox.askyesno("Logout", "Are you sure?"):
            self.destroy()
            from main import LoginApp
            LoginApp().mainloop()