import customtkinter as ctk
from Admin.admin_users import AdminUsers
from Admin.admin_activity import AdminAnnouncements 

class AdminMenu:
    def __init__(self, sidebar, content, user):
        self.sidebar = sidebar
        self.content = content
        self.user = user
        self.nav_buttons = [] # Track buttons to manage active states

        # Navigation Buttons
        # Icons stay the same, but colors will adapt
        self.add_nav_btn("📰   Activity", self.show_activity)
        self.add_nav_btn("👥   User Management", self.show_users)
        self.add_nav_btn("📅   Attendance", self.show_logs)

        # Initial View
        self.show_activity()

    def add_nav_btn(self, text, command):
        """Sidebar buttons with adaptive light/dark styling"""
        btn = ctk.CTkButton(
            self.sidebar, 
            text=text, 
            command=lambda: self.on_btn_click(btn, command), 
            fg_color="transparent", 
            # FIX: Light Mode = Dark Gray (#333333), Dark Mode = Light Gray (#D1D1D1)
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
        # Reset all buttons to transparent
        for btn in self.nav_buttons:
            btn.configure(fg_color="transparent")
        
        # Highlight selected button with professional blue
        clicked_btn.configure(fg_color=("#3498DB", "#1f538d"), text_color="white")
        command()

    def clear_content(self):
        """Clear content area for new view"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_activity(self):
        """📰 Admin Announcements View"""
        self.clear_content()
        try:
            # Ensure AdminAnnouncements uses adaptive colors internally too
            activity_view = AdminAnnouncements(self.content, self.user)
            activity_view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Activity", e)

    def show_users(self):
        """👥 User Management (CRUD) View"""
        self.clear_content()
        try:
            users_view = AdminUsers(self.content, self.user)
            users_view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("User Management", e)

    def show_logs(self):
        """📅 System Access Logs View"""
        self.clear_content()
        ctk.CTkLabel(
            self.content, 
            text="System Logs - Access History", 
            font=("Arial", 22, "bold"),
            text_color=("#2C3E50", "#FFFFFF") # Adaptive Heading
        ).pack(pady=20)

    def show_error(self, view_name, error):
        """Standardized error display"""
        error_lbl = ctk.CTkLabel(
            self.content, 
            text=f"Error loading {view_name}: {error}",
            text_color="#E74C3C"
        )
        error_lbl.pack(pady=20)