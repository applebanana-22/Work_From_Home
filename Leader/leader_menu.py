import customtkinter as ctk
from database import Database
from Leader.leader_dashboard import LeaderDashboard 
from Leader.leader_activity import LeaderActivity 
from Leader.leader_project import LeaderProject
from Leader.leader_report_view import LeaderReportView
from Leader.leader_overtime import LeaderOvertime

class LeaderMenu:
    def __init__(self, sidebar, content, user, db=None):
        self.sidebar = sidebar
        self.content = content
        self.user = user
        # Initialize Database connection if not provided
        self.db = db if db else Database()
        
        # Dictionary format to track buttons for badge placement and highlighting
        self.nav_buttons = {} 
        self.badge_label = None
        self._is_destroyed = False

        # --- Sidebar Header Section ---
        self.menu_label = ctk.CTkLabel(
            self.sidebar, text="TEAM LEADER MENU", 
            font=("Arial", 11, "bold"), text_color="gray"
        )
        self.menu_label.pack(anchor="w", padx=20, pady=(20, 10))

        # Setup the UI buttons
        self.setup_menu()
        
        # Default starting view: Dashboard
        self.navigate("dashboard", self.show_dashboard)
        
        # Start the background loop to check for notifications every 5 seconds
        self.auto_refresh_badge()

    def setup_menu(self):
        """Initializes and packs sidebar navigation buttons"""
        # Menu configuration (Key, Label, Method)
        menus = [
            ("dashboard", "📊 Dashboard", self.show_dashboard),
            ("activity", "📰 Activity", self.show_activity),
            ("reports", "📝 Daily Report", self.show_reports_list),
            ("project", "📁 Project", self.show_project),
            ("schedule", "🏠 WFH Schedule", self.show_schedule),
            ("attendance", "📅 Attendance", self.show_attendance),
            ("overtime", "⏰ Overtime Requests", self.show_overtime),
            ("leave", "📅 Leave Requests", self.show_leave_request)
        ]

        for key, text, cmd in menus:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=text, 
                command=lambda k=key, c=cmd: self.navigate(k, c), 
                fg_color="transparent", 
                text_color=("#333333", "#D1D1D1"), 
                hover_color=("#E0E0E0", "#2B2B2B"), 
                anchor="w", 
                height=42,
                font=("Arial", 13, "bold"), 
                corner_radius=8
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[key] = btn

    # --- Navigation Logic ---

    def navigate(self, active_key, command):
        """Handles highlighting and switching views"""
        # Reset all buttons to transparent
        for key in self.nav_buttons:
            self.nav_buttons[key].configure(
                fg_color="transparent", 
                text_color=("#333333", "#D1D1D1")
            )
        
        # Apply highlight to the active button
        if active_key in self.nav_buttons:
            self.nav_buttons[active_key].configure(
                fg_color=("#3498DB", "#1F538D"), 
                text_color="white"
            )
        
        command()

    # --- Notification & Badge System ---

    def auto_refresh_badge(self):
        """Background polling loop for notification updates"""
        if not self._is_destroyed:
            self.refresh_sidebar_badge()
            self.sidebar.after(5000, self.auto_refresh_badge) 

    def refresh_sidebar_badge(self):
        """Updates the red notification count on the Leave button"""
        try:
            self.db.cursor.execute(
                "SELECT COUNT(*) as count FROM notifications WHERE user_id = %s AND is_read = 0", 
                (self.user['id'],)
            )
            result = self.db.cursor.fetchone()
            count = result['count'] if result else 0

            # Remove existing badge if it exists
            if self.badge_label:
                self.badge_label.destroy()
                self.badge_label = None

            # Create new badge if count > 0
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
        except Exception: 
            pass

    def mark_notifications_as_read(self):
        """Clears notification status in Database and updates the UI"""
        try:
            self.db.cursor.execute(
                "UPDATE notifications SET is_read = 1 WHERE user_id = %s AND is_read = 0", 
                (self.user['id'],)
            )
            self.db.conn.commit()
            self.refresh_sidebar_badge()
        except Exception as e:
            print(f"Notification Update Error: {e}")

    # --- UI Utility Methods ---

    def clear_content(self):
        """Wipes the main content frame clean before loading new view"""
        for widget in self.content.winfo_children():
            try: widget.destroy()
            except: pass

    def show_error(self, view_name, error):
        """Displays a standardized error message on the main frame"""
        self.clear_content()
        ctk.CTkLabel(
            self.content, 
            text=f"⚠️ Error loading {view_name}: {str(error)}",
            font=("Arial", 14), 
            text_color="#E74C3C"
        ).pack(pady=40)

    # --- View Switching Methods ---

    def show_dashboard(self):
        self.clear_content()
        try:
            view = LeaderDashboard(self.content, self.user, self.db)
            view.pack(fill="both", expand=True)
        except Exception as e: self.show_error("Dashboard", e)

    def show_leave_request(self):
        """Displays Leave Manager and clears notification badges"""
        self.clear_content()
        try:
            from Leader.leader_leave_manage import LeaderLeaveManage
            self.mark_notifications_as_read()
            # Pass sidebar_ref so child views can trigger sidebar updates
            view = LeaderLeaveManage(self.content, self.user, sidebar_ref=self)
            view.pack(fill="both", expand=True)
        except Exception as e: self.show_error("Leave Requests", e)

    def show_activity(self):
        self.clear_content()
        try: 
            LeaderActivity(self.content, self.user).pack(fill="both", expand=True)
        except Exception as e: self.show_error("Activity", e)

    def show_project(self):
        self.clear_content()
        try: 
            LeaderProject(self.content, self.user).pack(fill="both", expand=True)
        except Exception as e: self.show_error("Project", e)

    def show_reports_list(self):
        self.clear_content()
        try: 
            LeaderReportView(self.content, self.user).pack(fill="both", expand=True)
        except Exception as e: self.show_error("Daily Report", e)

    def show_overtime(self):
        self.clear_content()
        try: 
            LeaderOvertime(self.content, self.user).pack(fill="both", expand=True)
        except Exception as e: self.show_error("Overtime", e)

    def show_schedule(self):
        self.clear_content()
        try:
            from Leader.leader_schedule import LeaderSchedule
            LeaderSchedule(self.content, self.user).pack(fill="both", expand=True)
        except Exception as e: self.show_error("WFH Schedule", e)

    def show_attendance(self):
        self.clear_content()
        try:
            from Leader.leader_attendance import LeaderAttendance
            LeaderAttendance(self.content, self.user).pack(fill="both", expand=True)
        except Exception as e: self.show_error("Attendance", e)