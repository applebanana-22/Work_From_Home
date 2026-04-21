import customtkinter as ctk
from Leader.leader_activity import LeaderActivity 
from Leader.leader_project import LeaderProject
from Leader.leader_report_view import LeaderReportView
from Leader.leader_overtime import LeaderOvertime
from Leader.leader_dashboard import LeaderDashboard 

class LeaderMenu:
    def __init__(self, sidebar, content, user, db=None):
        self.sidebar = sidebar
        self.content = content
        self.user = user
        self.db = db
        
        # Navigation buttons များကို track ရန် list
        self.nav_buttons = []

        # --- Sidebar Header Section ---
        self.menu_label = ctk.CTkLabel(
            self.sidebar, text="TEAM LEADER MENU", 
            font=("Arial", 11, "bold"), text_color="gray"
        )
        self.menu_label.pack(anchor="w", padx=20, pady=(20, 10))

        # Menu များအားလုံးကို Setup ပြုလုပ်မည်
        self.setup_menu()
        
        # အစဦးတွင် Dashboard ကို Highlight ပြထားမည်
        if self.nav_buttons:
            self.on_btn_click(self.nav_buttons[0], self.show_dashboard)

    def setup_menu(self):
        # လက်ရှိရှိနေသော ခလုတ်များကို ရှင်းလင်းမည်
        for btn in self.nav_buttons:
            btn.destroy()
        self.nav_buttons.clear()

        # Leader အတွက် လိုအပ်သော Menu List
        menus = [
            ("📊   Dashboard", self.show_dashboard),
            ("📰   Activity", self.show_activity),
            ("📝   Daily Report", self.show_reports_list),
            ("📁   Project", self.show_project),
            ("🏠   WFH Schedule", self.show_schedule),
            ("📅   Attendance", self.show_attendance),
            ("⏰   Overtime Requests", self.show_overtime),
            ("📅   Leave Requests", self.show_leave_request)
        ]
        
        for text, cmd in menus:
            self.add_nav_btn(text, cmd)

    def add_nav_btn(self, text, command):
        """Sidebar buttons with adaptive light/dark styling"""
        btn = ctk.CTkButton(
            self.sidebar, 
            text=text, 
            command=lambda: self.on_btn_click(btn, command), 
            fg_color="transparent", 
            text_color=("#333333", "#D1D1D1"), 
            hover_color=("#E0E0E0", "#2B2B2B"), 
            anchor="w", 
            height=42,
            font=("Arial", 13, "bold"),
            corner_radius=8
        )
        # Responsive ဖြစ်စေရန် fill="x" ကို အသုံးပြုထားပါသည်
        btn.pack(fill="x", padx=12, pady=2)
        self.nav_buttons.append(btn)

    def on_btn_click(self, clicked_btn, command):
        """Visual feedback when a button is selected"""
        for btn in self.nav_buttons:
            # Unselected buttons များကို reset လုပ်မည်
            btn.configure(fg_color="transparent", text_color=("#333333", "#D1D1D1"))
        
        # Highlight selected button (Leader အတွက် Blue color သုံးထားပါသည်)
        clicked_btn.configure(fg_color=("#3498DB", "#1F538D"), text_color="white")
        command()
        
    def clear_content(self):
        """Main view (right side) ကို ရှင်းလင်းရန်"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_error(self, view_name, error):
        """Error ဖြစ်ခဲ့လျှင် UI ပေါ်တွင် ပြသရန်"""
        self.clear_content()
        ctk.CTkLabel(
            self.content, 
            text=f"⚠️ Error loading {view_name}: {str(error)}",
            font=("Arial", 14),
            text_color="#E74C3C"
        ).pack(pady=40)

    # --- View Switching Logic ---

    def show_dashboard(self):
        self.clear_content()
        try:
            dash = LeaderDashboard(self.content, self.user, self.db)
            dash.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Dashboard", e)

    def show_leave_request(self):
        self.clear_content()
        try:
            from Leader.leader_leave_manage import LeaderLeaveManage
            view = LeaderLeaveManage(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Leave Requests", e)

    def show_activity(self):
        self.clear_content()
        try:
            LeaderActivity(self.content, self.user).pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Activity", e)

    def show_project(self):
        self.clear_content()
        try:
            LeaderProject(self.content, self.user).pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Project", e)

    def show_overtime(self):
        self.clear_content()
        try:
            LeaderOvertime(self.content, self.user).pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Overtime", e)

    def show_reports_list(self):
        self.clear_content()
        try:
            LeaderReportView(self.content).pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Daily Report", e)

    def show_schedule(self):
        self.clear_content()
        try:
            from Leader.leader_schedule import LeaderSchedule
            view = LeaderSchedule(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("WFH Schedule", e)

    def show_attendance(self):
        self.clear_content()
        try:
            from Leader.leader_attendance import LeaderAttendance
            view = LeaderAttendance(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Attendance", e)