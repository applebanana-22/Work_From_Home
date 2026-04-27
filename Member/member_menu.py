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
        self.nav_buttons = {}  # Using dict for easier badge targeting
        self.badge_label = None
        self._is_destroyed = False 

        # --- Sidebar Header Section ---
        self.menu_label = ctk.CTkLabel(
            self.sidebar, text="MEMBER PANEL", 
            font=("Arial", 11, "bold"), text_color="gray"
        )
        self.menu_label.pack(anchor="w", padx=20, pady=(20, 10))

        # Setup all menu buttons
        self.setup_menu()
        
        # Initial View: Dashboard
        self.navigate("dashboard", self.show_dashboard)
        
        # Start background notification polling (every 5 seconds)
        self.auto_refresh_loop()

    def setup_menu(self):
        """Defines and creates sidebar buttons with consistent styling"""
        menus = [
            ("dashboard", "📊   Dashboard", self.show_dashboard),
            ("activity", "📰   Activity", self.show_activity),
            ("tasks", "✅   Tasks", self.show_project),
            ("report", "📝   Daily Report", self.show_report),
            ("overtime", "⏰   Overtime", self.show_overtime),
            ("leave", "📅   Leave Request", self.show_leave_request),
            ("schedule", "🏠   WFH Schedule", self.show_schedule),
            ("attendance", "🚪   Attendance", self.show_attendance)
        ]

        for key, text, cmd in menus:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=text, 
                fg_color="transparent", 
                text_color=("#333333", "#D1D1D1"), 
                hover_color=("#E0E0E0", "#2B2B2B"), 
                anchor="w", 
                height=42,
                font=("Arial", 13, "bold"),
                corner_radius=8,
                command=lambda k=key, c=cmd: self.navigate(k, c)
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[key] = btn

    # --- Notification System Logic ---

    def auto_refresh_loop(self):
        """Background Loop: Checks for new notifications every 5 seconds"""
        if not self._is_destroyed:
            self.refresh_sidebar_badge()
            self.sidebar.after(5000, self.auto_refresh_loop)

    def refresh_sidebar_badge(self):
        """Fetches unread count from DB and updates the red badge on Leave button"""
        try:
            self.db.cursor.execute(
                "SELECT COUNT(*) as count FROM notifications WHERE user_id = %s AND is_read = 0", 
                (self.user['id'],)
            )
            result = self.db.cursor.fetchone()
            count = result['count'] if result else 0
            
            if self.badge_label: 
                self.badge_label.destroy()
                self.badge_label = None
            
            if count > 0:
                leave_btn = self.nav_buttons.get("leave")
                if leave_btn:
                    self.badge_label = ctk.CTkLabel(
                        leave_btn, text=str(count), 
                        font=("Arial", 10, "bold"), 
                        fg_color="#E74C3C", text_color="white", 
                        width=18, height=18, corner_radius=9
                    )
                    self.badge_label.place(relx=0.9, rely=0.5, anchor="center")
        except: 
            pass

    def mark_notifications_as_read(self):
        """Updates DB to set notifications as read and clears the UI badge"""
        try:
            self.db.cursor.execute(
                "UPDATE notifications SET is_read = 1 WHERE user_id = %s AND is_read = 0", 
                (self.user['id'],)
            )
            self.db.conn.commit()
            self.refresh_sidebar_badge()
        except Exception as e:
            print(f"Update Read Error: {e}")

    # --- Navigation Logic ---

    def navigate(self, active_key, command):
        """Handles visual selection (Blue highlight) and view switching"""
        for key in self.nav_buttons:
            self.nav_buttons[key].configure(
                fg_color="transparent", 
                text_color=("#333333", "#D1D1D1")
            )
        
        if active_key in self.nav_buttons:
            self.nav_buttons[active_key].configure(
                fg_color=("#3498DB", "#1F538D"), 
                text_color="white"
            )
        command()

    def clear(self):
        """Safely clear the main content area"""
        for w in self.content.winfo_children(): 
            try: w.destroy()
            except: pass

    def show_error(self, message):
        """UI helper for displaying errors"""
        self.clear()
        ctk.CTkLabel(
            self.content, text=f"⚠️ {message}", 
            text_color="#E74C3C", font=("Arial", 14, "bold")
        ).pack(pady=50)

    # --- View Methods ---

    def show_dashboard(self):
        self.clear()
        try:
            view = MemberDashboard(self.content, self.user, self.db)
            view.pack(fill="both", expand=True)
        except Exception as e: self.show_error(f"Dashboard Error: {e}")

    def show_leave_request(self):
        """Specialized view: Clears notifications upon clicking"""
        self.clear()
        try:
            from Member.member_leave import MemberLeave
            self.mark_notifications_as_read()
            # Passing self as sidebar_ref allows child views to trigger menu updates
            view = MemberLeave(self.content, self.user, sidebar_ref=self) 
            view.pack(fill="both", expand=True)
        except Exception as e: self.show_error(f"Leave View Error: {e}")

    def show_activity(self):
        self.clear()
        try:
            view = MemberActivity(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e: self.show_error(f"Activity Error: {e}")

    def show_project(self):
        self.clear()
        try:
            view = MemberProject(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e: self.show_error(f"Tasks Error: {e}")

    def show_report(self):
        self.clear()
        try:
            view = MemberReportFrame(self.content, user=self.user)
            view.pack(fill="both", expand=True)
        except Exception as e: self.show_error(f"Report Error: {e}")

    def show_overtime(self):
        self.clear()
        try:
            from Member.member_overtime import MemberOvertime
            view = MemberOvertime(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e: self.show_error(f"Overtime Error: {e}")

    def show_schedule(self):
        self.clear()
        try:
            view = MemberSchedule(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e: self.show_error(f"Schedule Error: {e}")

    def show_attendance(self):
        self.clear()
        try:
            from Member.member_attendance import MemberAttendance
            view = MemberAttendance(self.content, self.user)
            view.pack(fill="both", expand=True)
        except Exception as e: self.show_error(f"Attendance Error: {e}")