import customtkinter as ctk
from Leader.leader_activity import LeaderActivity # Activity အတွက် Import လုပ်ခြင်း
from Leader.leader_project import LeaderProject
from Leader.leader_report_view import LeaderReportView

class LeaderMenu:
    def __init__(self, sidebar, content, user):
        self.sidebar = sidebar
        self.content = content
        self.user = user

        # Image (5) ပါ Design နှင့် Menu Items များအတိုင်း Fixed လုပ်ထားခြင်း
        self.add_nav_btn("📊  Dashboard", self.show_dashboard)
        self.add_nav_btn("📰  Activity", self.show_activity)
        self.add_nav_btn("📝  Daily Report", self.show_reports_list)
        self.add_nav_btn("📁  Project", self.show_project)
        self.add_nav_btn("🏠  WFH Schedule", self.show_schedule)
        self.add_nav_btn("📅  Attendance", self.show_attendance)

        # Dashboard ကို Default View အဖြစ် သတ်မှတ်ခြင်း
        self.show_dashboard()

    def add_nav_btn(self, text, command):
        """Sidebar ခလုတ်များအတွက် Modern UI Style သတ်မှတ်ခြင်း"""
        btn = ctk.CTkButton(
            self.sidebar, 
            text=text, 
            command=command, 
            fg_color="transparent", 
            text_color="#D1D1D1", # Grayish white text
            hover_color="#2b2b2b", 
            anchor="w", 
            height=42,
            font=("Arial", 13),
            corner_radius=8
        )
        btn.pack(fill="x", padx=12, pady=2)

    def clear_content(self):
        """Content area ရှိ widget ဟောင်းများကို ဖျက်ထုတ်ခြင်း"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        """📊 Team Overview Dashboard"""
        self.clear_content()
        ctk.CTkLabel(
            self.content, 
            text="Leader Dashboard – Team Overview", 
            font=("Arial", 24, "bold"),
            text_color="gray80"
        ).pack(expand=True)

    def show_activity(self):
        """📰 Team & Admin Announcements (Integrated with LeaderActivity)"""
        self.clear_content()
        try:
            # LeaderActivity class ကို ခေါ်ယူအသုံးပြုခြင်း
            activity_view = LeaderActivity(self.content, self.user)
            activity_view.pack(fill="both", expand=True)
        except Exception as e:
            error_lbl = ctk.CTkLabel(self.content, text=f"Error loading Leader Activity: {e}")
            error_lbl.pack(pady=20)

    def show_reports_list(self):
        """View all reports from members"""
        self.clear_content()
        # Now we only import and call one thing. 
        # No callbacks or extra methods needed in this file!
        from Leader.leader_report_view import LeaderReportView
        LeaderReportView(self.content).pack(fill="both", expand=True)

    def show_project(self):
        """📁 Project Management View Integration"""
        self.clear_content()
        try:
            # LeaderProject class ကို ခေါ်ယူအသုံးပြုခြင်း
            project_view = LeaderProject(self.content, self.user)
            project_view.pack(fill="both", expand=True)
        except Exception as e:
            error_lbl = ctk.CTkLabel(self.content, text=f"Error loading Projects: {e}")
            error_lbl.pack(pady=20)

    def show_schedule(self):
        """🏠 WFH Schedule"""
        self.clear_content()
        ctk.CTkLabel(self.content, text="Team WFH/Office Schedule", font=("Arial", 22)).pack(pady=20)

    def show_attendance(self):
        """📅 Attendance Tracking"""
        self.clear_content()
        ctk.CTkLabel(self.content, text="Team Attendance Logs", font=("Arial", 22)).pack(pady=20)