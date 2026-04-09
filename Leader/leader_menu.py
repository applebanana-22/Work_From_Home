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

        self.setup_menu()
        self.show_dashboard()

    def setup_menu(self):
        menus = [
            ("📊  Dashboard", self.show_dashboard),
            ("📰  Activity", self.show_activity),
            ("📝  Daily Report", self.show_reports_list),
            ("📁  Project", self.show_project),
            ("🏠  WFH Schedule", self.show_schedule),
            ("📅  Attendance", self.show_attendance),
            ("⏰  Overtime Requests", self.show_overtime), # Added missing comma
            ("📅  Leave Requests", self.show_leave_request) # New Feature
        ]
        for text, cmd in menus:
            self.add_nav_btn(text, cmd)

    def add_nav_btn(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar, text=text, command=command, 
            fg_color="transparent", text_color="#D1D1D1", 
            hover_color="#2b2b2b", anchor="w", height=42,
            font=("Arial", 13), corner_radius=8
        )
        btn.pack(fill="x", padx=12, pady=2)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # --- View Switching Logic ---

    def show_dashboard(self):
        self.clear_content()
        try:
            dash = LeaderDashboard(self.content, self.user, self.db)
            dash.pack(fill="both", expand=True)
        except Exception as e:
            ctk.CTkLabel(self.content, text=f"Error loading Dashboard: {e}").pack(pady=20)

    def show_leave_request(self):
        """Feature: Manage Team Leave Requests"""
        self.clear_content()
        try:
            from Leader.leader_leave_manage import LeaderLeaveManage
            view = LeaderLeaveManage(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            ctk.CTkLabel(self.content, text=f"Error loading Leave Management: {e}", text_color="red").pack(pady=20)

    # ... (Keep other show_ methods as they were)
    def show_activity(self):
        self.clear_content()
        LeaderActivity(self.content, self.user).pack(fill="both", expand=True)

    def show_project(self):
        self.clear_content()
        LeaderProject(self.content, self.user).pack(fill="both", expand=True)

    def show_overtime(self):
        self.clear_content()
        LeaderOvertime(self.content, self.user).pack(fill="both", expand=True)

    def show_reports_list(self):
        self.clear_content()
        LeaderReportView(self.content).pack(fill="both", expand=True)

    def show_schedule(self):
        """Update this in your LeaderMenu class"""
        self.clear_content()
        try:
            from Leader.leader_schedule import LeaderSchedule
            view = LeaderSchedule(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            ctk.CTkLabel(self.content, text=f"Error: {e}", text_color="red").pack(pady=20)

    def show_attendance(self):
        self.clear_content()
        try:
            from Leader.leader_attendance import LeaderAttendance
            view = LeaderAttendance(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            ctk.CTkLabel(self.content, text=f"Error loading Attendance: {e}", text_color="red").pack(pady=20)