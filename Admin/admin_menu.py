import customtkinter as ctk
from Admin.admin_users import AdminUsers
from Admin.admin_activity import AdminAnnouncements 
from Admin.admin_teams import AdminTeams
from Admin.admin_attendance import AdminAttendance

class AdminMenu:
    def __init__(self, sidebar, content, user):
        self.sidebar = sidebar
        self.content = content
        self.user = user
        self.nav_buttons = [] 

        # --- Sidebar Header Section ---
        # Sidebar ရဲ့ ထိပ်ဆုံးမှာ Section Title လေးထည့်ပေးခြင်းဖြင့် ပိုကြည့်ကောင်းစေသည်
        self.menu_label = ctk.CTkLabel(
            self.sidebar, text="ADMIN CONTROLS", 
            font=("Arial", 11, "bold"), text_color="gray"
        )
        self.menu_label.pack(anchor="w", padx=20, pady=(20, 10))

        # --- Navigation Buttons ---
        self.add_nav_btn("📰   Activity", self.show_activity)
        self.add_nav_btn("👥   User Management", self.show_users)
        self.add_nav_btn("🛡️   Team Management", self.show_teams) 
        self.add_nav_btn("📅   Attendance", self.show_attendance)

        # Default စဖွင့်မည့် Page
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
        # Responsive ဖြစ်စေရန် pack ကို စနစ်တကျသုံးထားခြင်း
        btn.pack(fill="x", padx=12, pady=2)
        self.nav_buttons.append(btn)

    def on_btn_click(self, clicked_btn, command):
        """Visual feedback when a button is selected"""
        for btn in self.nav_buttons:
            # Reset unselected buttons
            btn.configure(fg_color="transparent", text_color=("#333333", "#D1D1D1"))
        
        # Highlight selected button
        # Selected color ကို Theme နဲ့ လိုက်ဖက်အောင် Blue ပေးထားသည်
        clicked_btn.configure(fg_color=("#3498DB", "#1F538D"), text_color="white")
        command()

    def clear_content(self):
        """Main view ကို ရှင်းလင်းခြင်း"""
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

    def show_teams(self):
        self.clear_content()
        try:
            teams_view = AdminTeams(self.content, self.user)
            teams_view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Team Management", e)

    def show_attendance(self):
        self.clear_content()
        try:
            attendance_view = AdminAttendance(self.content, self.user)
            attendance_view.pack(fill="both", expand=True)
        except Exception as e:
            self.show_error("Attendance", e)

    def show_error(self, view_name, error):
        """Error ဖြစ်ခဲ့လျှင် ပြသရန်"""
        error_lbl = ctk.CTkLabel(
            self.content, 
            text=f"⚠️ Error loading {view_name}: {str(error)}",
            font=("Arial", 14),
            text_color="#E74C3C"
        )
        error_lbl.pack(pady=40)

    # Note: show_logs logic ကို လောလောဆယ် ခလုတ်မထည့်ထားသေးပါ (လိုအပ်လျှင် add_nav_btn တွင် ထပ်ပေါင်းနိုင်သည်)