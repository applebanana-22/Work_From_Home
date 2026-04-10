import customtkinter as ctk
from Admin.admin_users import AdminUsers
from Admin.admin_activity import AdminAnnouncements 
# 1. Import your new Team Management class here
from Admin.admin_teams import AdminTeams
from Admin.admin_attendance import AdminAttendance

class AdminMenu:
    def __init__(self, sidebar, content, user):
        self.sidebar = sidebar
        self.content = content
        self.user = user
        self.nav_buttons = [] 

        # Navigation Buttons
        self.add_nav_btn("📰   Activity", self.show_activity)
        self.add_nav_btn("👥   User Management", self.show_users)
        # 2. Add the new Create Team button here
        self.add_nav_btn("🛡️   Team Management", self.show_teams) 
        self.add_nav_btn("📅   Attendance", self.show_attendance)

        self.show_activity()

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
        btn.pack(fill="x", padx=12, pady=2)
        self.nav_buttons.append(btn)

    def on_btn_click(self, clicked_btn, command):
        """Visual feedback when a button is selected"""
        for btn in self.nav_buttons:
            # Reset text color to adaptive gray when unselected
            btn.configure(fg_color="transparent", text_color=("#333333", "#D1D1D1"))
        
        # Highlight selected
        clicked_btn.configure(fg_color=("#3498DB", "#1f538d"), text_color="white")
        command()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_activity(self):
        self.clear_content()
        try:
            activity_view = AdminAnnouncements(self.content, self.user)
            activity_view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Activity", e)

    def show_users(self):
        self.clear_content()
        try:
            users_view = AdminUsers(self.content, self.user)
            users_view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("User Management", e)

    # 3. Add the new View Method
    def show_teams(self):
        self.clear_content()
        try:
            teams_view = AdminTeams(self.content, self.user)
            teams_view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Team Management", e)

    def show_logs(self):
        self.clear_content()
        ctk.CTkLabel(
            self.content, 
            text="System Logs - Access History", 
            font=("Arial", 22, "bold"),
            text_color=("#2C3E50", "#FFFFFF") 
        ).pack(pady=20)

    def show_error(self, view_name, error):
        error_lbl = ctk.CTkLabel(
            self.content, 
            text=f"Error loading {view_name}: {error}",
            text_color="#E74C3C"
        )
        error_lbl.pack(pady=20)
    
    def show_attendance(self):
        self.clear_content()
        try:
            attendance_view = AdminAttendance(self.content, self.user)
            attendance_view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Attendance", e)