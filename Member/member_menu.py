import customtkinter as ctk
from Member.member_activity import MemberActivity
from Member.member_project import MemberProject
from Member.member_report import MemberReportFrame

class MemberMenu:
    def __init__(self, sidebar, content, user):
        self.sidebar = sidebar
        self.content = content
        self.user = user

        # Menu Items
        self.add_nav_btn("📊 Dashboard", self.show_dashboard)
        self.add_nav_btn("📰 Activity", self.show_activity)
        self.add_nav_btn("✅ Tasks", self.show_project)
        self.add_nav_btn("📝 Daily Report", self.show_report)
        self.add_nav_btn("📤 Leave Request", self.show_leave)

        self.show_dashboard()

    def add_nav_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command, 
                            fg_color="transparent", text_color="gray90",
                            hover_color="#2b2b2b", anchor="w", height=40,
                            font=("Arial", 13))
        btn.pack(fill="x", padx=10, pady=2)

    def clear(self):
        """Content area ကို ရှင်းလင်းခြင်း"""
        for w in self.content.winfo_children(): 
            w.destroy()

    def show_dashboard(self):
        self.clear()
        ctk.CTkLabel(self.content, text="Dashboard – Coming Soon", 
                     font=("Arial", 24, "bold"), text_color="gray80").pack(expand=True)

    def show_activity(self):
        self.clear()
        view = MemberActivity(self.content, self.user)
        view.pack(fill="both", expand=True)

    def show_project(self):
        """📁 Member Task View Integration"""
        self.clear() # clear_content() အစား self.clear() ကို သုံးရန် ပြင်ထားပါသည်
        try:
            project_view = MemberProject(self.content, self.user)
            project_view.pack(fill="both", expand=True)
        except Exception as e:
            ctk.CTkLabel(self.content, text=f"Error loading tasks: {e}").pack(pady=20)

    def show_report(self):
        self.clear()
        try:
            # Pass self.user (the dictionary containing 'id', 'role', etc.)
            report_view = MemberReportFrame(self.content, user=self.user)
            report_view.pack(fill="both", expand=True)
        except Exception as e:
            ctk.CTkLabel(self.content, text=f"Error loading report: {e}").pack(pady=20)

    def show_leave(self):
        self.clear()
        ctk.CTkLabel(self.content, text="Apply for Leave", font=("Arial", 22)).pack(pady=20)