import customtkinter as ctk
from database import Database
from Member.member_dashboard import MemberDashboard 
from Member.member_activity import MemberActivity
from Member.member_project import MemberProject
from Member.member_report import MemberReportFrame
from Member.member_schedule import MemberSchedule

class MemberMenu:
    def __init__(self, sidebar, content, user):
        self.sidebar = sidebar
        self.content = content
        self.user = user
        self.db = Database() 
        self.nav_buttons = []

        # --- Sidebar Header Section ---
        self.menu_label = ctk.CTkLabel(
            self.sidebar, text="MEMBER PANEL", 
            font=("Arial", 11, "bold"), text_color="gray"
        )
        self.menu_label.pack(anchor="w", padx=20, pady=(20, 10))

        # Menu များအားလုံးကို Setup ပြုလုပ်မည်
        self.setup_menu()
        
        # အစဦးတွင် Dashboard ကို Highlight ပြထားမည်
        if self.nav_buttons:
            self.navigate(self.nav_buttons[0], self.show_dashboard)
        
    def setup_menu(self):
        # Menu definitions - Sidebar တွင် ပေါ်မည့် အစီအစဉ်
        menus = [
            ("📊   Dashboard", self.show_dashboard),
            ("📰   Activity", self.show_activity),
            ("✅   Tasks", self.show_project),
            ("📝   Daily Report", self.show_report),
            ("⏰   Overtime", self.show_overtime),
            ("📅   Leave Request", self.show_leave_request),
            ("🏠   WFH Schedule", self.show_schedule),
            ("🚪   Attendance", self.show_attendance)
        ]
        
        for text, cmd in menus:
            self.add_nav_btn(text, cmd)

    def add_nav_btn(self, text, command):
        """Adaptive Sidebar buttons: matches Admin/Leader design"""
        btn = ctk.CTkButton(
            self.sidebar, 
            text=text, 
            # command logic ကို navigate function နှင့် ချိတ်ဆက်မည်
            command=lambda b=None: self.navigate(b, command),
            fg_color="transparent", 
            text_color=("#333333", "#D1D1D1"), 
            hover_color=("#E0E0E0", "#2B2B2B"), 
            anchor="w", 
            height=42,
            font=("Arial", 13, "bold"),
            corner_radius=8
        )
        # Button instance ကို lambda ထဲသို့ ပြန်ထည့်ပေးခြင်း
        btn.configure(command=lambda b=btn: self.navigate(b, command))
        
        # Responsive ဖြစ်စေရန် pack fill="x" ကို အသုံးပြုပါသည်
        btn.pack(fill="x", padx=12, pady=2)
        self.nav_buttons.append(btn)

    def navigate(self, active_btn, command):
        """Visual feedback for selection with Blue highlight"""
        for btn in self.nav_buttons:
            # Unselected buttons များကို reset လုပ်မည်
            btn.configure(
                fg_color="transparent", 
                text_color=("#333333", "#D1D1D1")
            )
            
        # Highlight active (Blue background, White text)
        if active_btn:
            active_btn.configure(
                fg_color=("#3498DB", "#1F538D"), 
                text_color="white"
            )
        command()

    def clear(self):
        """Safely clear the content area (main view)"""
        for w in self.content.winfo_children(): 
            w.destroy()

    def show_error(self, message):
        """Error ဖြစ်ခဲ့လျှင် screen ပေါ်တွင် ပြသရန် helper function"""
        self.clear()
        ctk.CTkLabel(
            self.content, 
            text=f"⚠️ {message}", 
            text_color="#E74C3C", 
            font=("Arial", 14, "bold")
        ).pack(pady=50)

    # --- View Switching Logic ---

    def show_dashboard(self):
        self.clear()
        try:
            view = MemberDashboard(self.content, self.user, self.db)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error(f"Dashboard Error: {str(e)}")

    def show_activity(self):
        self.clear()
        try:
            view = MemberActivity(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error(f"Activity Error: {str(e)}")

    def show_project(self):
        self.clear()
        try:
            view = MemberProject(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error(f"Tasks Error: {str(e)}")

    def show_report(self):
        self.clear()
        try:
            view = MemberReportFrame(self.content, user=self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error(f"Report Error: {str(e)}")

    def show_overtime(self):
        self.clear()
        try:
            from Member.member_overtime import MemberOvertime
            view = MemberOvertime(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error(f"Overtime View Error: {str(e)}")

    def show_leave_request(self):
        self.clear()
        try:
            from Member.member_leave import MemberLeave
            view = MemberLeave(self.content, self.user) 
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error(f"Leave View Error: {str(e)}")

    def show_schedule(self):
        self.clear()
        try:
            view = MemberSchedule(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error(f"Schedule View Error: {str(e)}")
    
    def show_attendance(self):
        self.clear()
        try:
            from Member.member_attendance import MemberAttendance
            view = MemberAttendance(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error(f"Attendance View Error: {str(e)}")