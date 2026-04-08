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

        self.setup_menu()
        # Start with Dashboard
        self.show_dashboard()
        
    def setup_menu(self):
        # We find the buttons and map them
        self.add_nav_btn("📊 Dashboard", self.show_dashboard)
        self.add_nav_btn("📰 Activity", self.show_activity)
        self.add_nav_btn("✅ Tasks", self.show_project)
        self.add_nav_btn("📝 Daily Report", self.show_report)
        self.add_nav_btn("⏰ Overtime", self.show_overtime)
        self.add_nav_btn("📅 Leave Request", self.show_leave_request)
        self.add_nav_btn("🏠 WFH Schedule", self.show_schedule)


    def add_nav_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, 
                            fg_color="transparent", text_color="gray90",
                            hover_color="#2b2b2b", anchor="w", height=40,
                            font=("Arial", 13),
                            command=lambda: self.navigate(btn, command))
        btn.pack(fill="x", padx=10, pady=2)
        self.nav_buttons.append(btn)

    def navigate(self, active_btn, command):
        for btn in self.nav_buttons:
            btn.configure(fg_color="transparent")
        active_btn.configure(fg_color="#3498DB")
        command()

    def clear(self):
        """Safely clear the content area"""
        for w in self.content.winfo_children(): 
            w.destroy()

    def show_dashboard(self):
        self.clear()
        view = MemberDashboard(self.content, self.user, self.db)
        view.pack(fill="both", expand=True)

    def show_activity(self):
        self.clear()
        view = MemberActivity(self.content, self.user)
        view.pack(fill="both", expand=True)

    def show_project(self):
        self.clear()
        view = MemberProject(self.content, self.user)
        view.pack(fill="both", expand=True)

    def show_report(self):
        self.clear()
        view = MemberReportFrame(self.content, user=self.user)
        view.pack(fill="both", expand=True)

    def show_overtime(self):
        self.clear()
        try:
            from Member.member_overtime import MemberOvertime
            view = MemberOvertime(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error(f"Overtime View Error: {e}")

    def show_leave_request(self):
        self.clear()
        try:
            # Dynamic import to prevent circular dependency
            from Member.member_leave import MemberLeave
            view = MemberLeave(self.content, self.user) 
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error(f"Leave View Error: {e}")

    def show_error(self, message):
        """Helper to show errors on the screen if a module fails to load"""
        ctk.CTkLabel(self.content, text=message, text_color="red").pack(pady=50)
        
    def show_schedule(self):
        self.clear()
        try:
            # Initialize the actual class we built
            view = MemberSchedule(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error(f"Schedule View Error: {e}")


    