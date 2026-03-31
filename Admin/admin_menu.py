import customtkinter as ctk
from Admin.admin_users import AdminUsers
from Admin.admin_activity import AdminAnnouncements # Activity အတွက် Import လုပ်ခြင်း

class AdminMenu:
    def __init__(self, sidebar, content, user):
        self.sidebar = sidebar
        self.content = content
        self.user = user

        # Navigation Buttons (Image 4 ထဲက Design အတိုင်း)
        self.add_nav_btn("📰  Activity", self.show_activity)
        self.add_nav_btn("👥  User Management", self.show_users)
        self.add_nav_btn("📅  Attendance", self.show_logs)

        # ပရိုဂရမ်စဖွင့်တာနဲ့ Dashboard ကို အရင်ပြထားပါမယ်
        self.show_activity()

    def add_nav_btn(self, text, command):
        """Sidebar ခလုတ်များ၏ Style ကို သတ်မှတ်ခြင်း"""
        btn = ctk.CTkButton(
            self.sidebar, 
            text=text, 
            command=command, 
            fg_color="transparent", 
            text_color="#D1D1D1", 
            hover_color="#2b2b2b", 
            anchor="w", 
            height=42,
            font=("Arial", 13),
            corner_radius=8
        )
        btn.pack(fill="x", padx=12, pady=2)

    def clear_content(self):
        """Content area ထဲက widget ဟောင်းများကို ဖျက်ထုတ်ခြင်း"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_activity(self):
        """📰 Admin Announcements View (သင်ပေးထားတဲ့ Code ကို ချိတ်ဆက်ခြင်း)"""
        self.clear_content()
        # AdminAnnouncements class ကို master အနေနဲ့ self.content ပေးပြီး ခေါ်ယူခြင်း
        try:
            activity_view = AdminAnnouncements(self.content, self.user)
            activity_view.pack(fill="both", expand=True)
        except Exception as e:
            error_lbl = ctk.CTkLabel(self.content, text=f"Error loading Activity: {e}")
            error_lbl.pack(pady=20)

    def show_users(self):
        """👥 User Management (CRUD) View"""
        self.clear_content()
        try:
            users_view = AdminUsers(self.content, self.user)
            users_view.pack(fill="both", expand=True)
        except Exception as e:
            error_lbl = ctk.CTkLabel(self.content, text=f"Error loading User Management: {e}")
            error_lbl.pack(pady=20)

    def show_logs(self):
        """📅 System Access Logs View"""
        self.clear_content()
        ctk.CTkLabel(
            self.content, 
            text="System Logs - Access History", 
            font=("Arial", 22)
        ).pack(pady=20)