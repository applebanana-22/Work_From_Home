import customtkinter as ctk
from database import Database
# Import the dashboard we just created
from Member.member_dashboard import MemberDashboard 
from Member.member_activity import MemberActivity
from Member.member_project import MemberProject
from Member.member_report import MemberReportFrame

class MemberMenu:
    def __init__(self, sidebar, content, user):
        self.sidebar = sidebar
        self.content = content
        self.user = user
        self.db = Database() # Central database instance
        self.nav_buttons = []

        # Create Navigation Buttons
        self.setup_menu()

        # Load Dashboard by default
        self.show_dashboard()

    def add_nav_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, 
                            fg_color="transparent", text_color="gray90",
                            hover_color="#2b2b2b", anchor="w", height=40,
                            font=("Arial", 13),
                            command=lambda: self.navigate(btn, command))
        btn.pack(fill="x", padx=10, pady=2)
        self.nav_buttons.append(btn)

    def navigate(self, active_btn, command):
        """Highlights active button and runs the show_ function"""
        for btn in self.nav_buttons:
            btn.configure(fg_color="transparent")
        active_btn.configure(fg_color="#3498DB")
        command()

    def clear(self):
        for w in self.content.winfo_children(): 
            w.destroy()

    def setup_menu(self):
        self.add_nav_btn("📊 Dashboard", self.show_dashboard)
        self.add_nav_btn("📰 Activity", self.show_activity)
        self.add_nav_btn("✅ Tasks", self.show_project)
        self.add_nav_btn("📝 Daily Report", self.show_report)
        self.add_nav_btn("⏰ Overtime", self.show_overtime)

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
        from Member.member_overtime import MemberOvertime
        view = MemberOvertime(self.content, self.user)
        view.pack(fill="both", expand=True)