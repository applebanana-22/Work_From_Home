import customtkinter as ctk
from tkinter import ttk

class MemberDashboard(ctk.CTkFrame):
    def __init__(self, master, user, db):
        super().__init__(master, fg_color="transparent")
        self.user = user
        self.db = db
        self._is_destroyed = False

        # --- 1. Welcome Section ---
        self.welcome_f = ctk.CTkFrame(self, fg_color="transparent")
        self.welcome_f.pack(fill="x", padx=40, pady=(30, 15))

        self.title_label = ctk.CTkLabel(
            self.welcome_f, 
            text=f"Welcome back, {self.user['full_name']}! 👋", 
            font=("Arial", 32, "bold"),
            text_color=("#1A1A1A", "#FFFFFF")
        )
        self.title_label.pack(anchor="w")
        
        ctk.CTkLabel(
            self.welcome_f, 
            text="Real-time Team Activity & Performance Tracker", 
            font=("Arial", 15), 
            text_color="#888888"
        ).pack(anchor="w", pady=(2, 10))

        # --- 2. Stats Container ---
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=40, pady=10)

        # --- 3. Team Status Table Section ---
        self.setup_modern_table()
        
        # Start the real-time refresh loop
        self.auto_refresh()

    def auto_refresh(self):
        """Refreshes all dashboard data every 5 seconds"""
        if self._is_destroyed:
            return
            
        self.refresh_stats()
        self.load_team_data()
        
        # Schedule next refresh (5000ms = 5 seconds)
        self.after(5000, self.auto_refresh)

    def destroy(self):
        self._is_destroyed = True
        super().destroy()

    def refresh_stats(self):
        """Fetches real data from the database"""
        try:
            # 1. Team Size & On Duty (Active / Total)
            self.db.cursor.execute(
                "SELECT COUNT(*) as total, SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active "
                "FROM users WHERE team_id = %s", (self.user['team_id'],)
            )
            team_stats = self.db.cursor.fetchone()
            team_size = team_stats['total'] or 0
            on_duty = f"{team_stats['active'] or 0}/{team_size}"

            # 2. Active Tasks (Assigned to current user and not completed)
            self.db.cursor.execute(
                "SELECT COUNT(*) as active_tasks FROM tasks "
                "WHERE assigned_to = %s AND status != 'Completed'", (self.user['full_name'],)
            )
            task_stats = self.db.cursor.fetchone()
            active_tasks = task_stats['active_tasks'] or 0

            # 3. Urgent OT (Pending overtime requests for this user)
            self.db.cursor.execute(
                "SELECT COUNT(*) as pending_ot FROM overtime_requests "
                "WHERE member_id = %s AND status = 'Pending'", (self.user['id'],)
            )
            ot_stats = self.db.cursor.fetchone()
            urgent_ot = ot_stats['pending_ot'] or 0

            # Update UI
            for w in self.stats_container.winfo_children(): w.destroy()
            
            stats = [
                {"title": "Team Size", "value": str(team_size), "color": "#3498DB"},
                {"title": "Active Tasks", "value": str(active_tasks), "color": "#10B981"},
                {"title": "Urgent OT", "value": str(urgent_ot), "color": "#E74C3C"},
                {"title": "On Duty", "value": on_duty, "color": "#F39C12"}
            ]
            
            for item in stats:
                card = self.create_card(self.stats_container, item['title'], item['value'], item['color'])
                card.pack(side="left", padx=(0, 20), expand=True, fill="both")
                
        except Exception as e:
            print(f"Stats Refresh Error: {e}")

    def setup_modern_table(self):
        header_f = ctk.CTkFrame(self, fg_color="transparent")
        header_f.pack(fill="x", padx=40, pady=(25, 10))
        
        ctk.CTkLabel(
            header_f, text="👥 Team Collaboration Status", 
            font=("Arial", 18, "bold"),
            text_color=("#3498DB", "#5DADE2")
        ).pack(side="left")

        self.table_bg = ctk.CTkFrame(
            self, fg_color=("#FFFFFF", "#1E1E1E"), 
            corner_radius=15, border_width=1, 
            border_color=("#E0E0E0", "#2B2B2B")
        )
        self.table_bg.pack(fill="both", expand=True, padx=40, pady=(0, 30))

        # --- Treeview Styling ---
        style = ttk.Style()
        style.theme_use("clam")
        
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_col = "#1E1E1E" if is_dark else "#FFFFFF"
        fg_col = "#FFFFFF" if is_dark else "#000000"
        head_bg = "#2B2B2B" if is_dark else "#F0F2F5"
        odd_row_bg = "#252525" if is_dark else "#F9F9F9"

        style.configure("Treeview", 
                        background=bg_col, foreground=fg_col, 
                        fieldbackground=bg_col, rowheight=45, 
                        font=("Arial", 11), borderwidth=0)
        
        style.configure("Treeview.Heading", 
                        background=head_bg, foreground=fg_col, 
                        font=("Arial", 11, "bold"), borderwidth=0)
        
        style.map("Treeview", background=[('selected', '#3498DB')])

        columns = ("id", "name", "location", "activity")
        self.tree = ttk.Treeview(self.table_bg, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").upper())
            self.tree.column(col, anchor="center")

        self.tree.column("name", width=250, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=15, pady=15)
        self.tree.tag_configure('odd', background=odd_row_bg)

    def load_team_data(self):
        """Loads and updates real-time status of teammates"""
        try:
            query = """
                SELECT employee_id, full_name, role, current_status, status 
                FROM users WHERE team_id = %s 
                ORDER BY CASE WHEN role = 'leader' THEN 1 ELSE 2 END
            """
            self.db.cursor.execute(query, (self.user['team_id'],))
            members = self.db.cursor.fetchall()

            # Store selection to restore after refresh
            selected = self.tree.selection()
            
            # Clear table
            for item in self.tree.get_children(): 
                self.tree.delete(item)

            for i, m in enumerate(members):
                role_icon = "👑 " if m['role'] == 'leader' else "👤 "
                name_val = f" {role_icon}{m['full_name']}"
                
                # Location (Current_status)
                loc = m['current_status'] or "Office"
                loc_val = f"🏢 {loc}" if loc == "Office" else f"🏠 {loc}"
                
                # Activity Status
                raw_status = (m['status'] or "offline").lower()
                act_icon = "🟢" if raw_status == "active" else "🟡" if raw_status == "away" else "🔴"
                act_val = f"{act_icon} {raw_status.upper()}"

                tag = 'odd' if i % 2 != 0 else 'even'
                self.tree.insert("", "end", values=(m['employee_id'], name_val, loc_val, act_val), tags=(tag,))

        except Exception as e:
            print(f"Table Error: {e}")

    def create_card(self, master, title, value, color):
        card = ctk.CTkFrame(master, height=120, corner_radius=15, 
                            border_width=1, border_color=("#E0E0E0", "#2B2B2B"))
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=("Arial", 13), text_color="#888888").pack(pady=(20, 0))
        ctk.CTkLabel(card, text=value, font=("Arial", 32, "bold"), text_color=color).pack(pady=5)
        ctk.CTkFrame(card, height=5, fg_color=color).pack(fill="x", side="bottom")
        return card