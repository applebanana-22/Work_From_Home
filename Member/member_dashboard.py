import customtkinter as ctk
from tkinter import ttk

class MemberDashboard(ctk.CTkFrame):
    def __init__(self, master, user, db):
        super().__init__(master, fg_color=("#F2F2F2", "#121212"))
        self.user = user
        self.db = db
        self._is_destroyed = False
        self._after_id = None # Track the timer to prevent "invalid command" errors

        self.setup_ui()
        
        # Theme Change Listener
        self.bind("<Expose>", lambda e: self.apply_treeview_style())
        
        self.auto_refresh()

    def setup_ui(self):
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
        
        ctk.CTkLabel(self.welcome_f, text="Real-time Team Activity & Performance Tracker", 
                     font=("Arial", 15), text_color=("#666666", "#888888")).pack(anchor="w", pady=(2, 10))

        # --- 2. Stats Container ---
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=40, pady=10)

        # --- 3. Team Status Table Section ---
        header_f = ctk.CTkFrame(self, fg_color="transparent")
        header_f.pack(fill="x", padx=40, pady=(25, 10))
        
        ctk.CTkLabel(header_f, text="👥 Team Collaboration Status", 
                     font=("Arial", 18, "bold"), text_color=("#3498DB", "#5DADE2")).pack(side="left")

        self.table_bg = ctk.CTkFrame(
            self, fg_color=("#FFFFFF", "#1E1E1E"), 
            corner_radius=15, border_width=1, border_color=("#E0E0E0", "#2B2B2B")
        )
        self.table_bg.pack(fill="both", expand=True, padx=40, pady=(0, 30))

        # Container for the tables and scrollbar
        tree_container = ctk.CTkFrame(self.table_bg, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=15, pady=15)

        # --- DUAL TREEVIEW SETUP ---
        info_cols = ("id", "name", "location")
        self.info_tree = ttk.Treeview(tree_container, columns=info_cols, show="headings", height=10)
        self.status_tree = ttk.Treeview(tree_container, columns=("activity",), show="headings", height=10)

        for col in info_cols:
            self.info_tree.heading(col, text=col.replace("_", " ").upper())
            self.info_tree.column(col, anchor="center")
        
        self.info_tree.column("name", width=250, anchor="w")
        self.status_tree.heading("activity", text="ACTIVITY")
        self.status_tree.column("activity", anchor="center", width=150)

        # Pack tables and Scrollbar
        self.info_tree.pack(side="left", fill="both", expand=True)
        self.status_tree.pack(side="left", fill="y") # Changed to side="left" to sit next to info_tree

        self.apply_treeview_style()
        self.sync_scroll(tree_container)

    def apply_treeview_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_col = "#1E1E1E" if is_dark else "#FFFFFF"
        fg_col = "#FFFFFF" if is_dark else "#000000"
        head_bg = "#2B2B2B" if is_dark else "#F0F2F5"
        odd_row_bg = "#252525" if is_dark else "#F9F9F9"

        for tree_name in ["Treeview", "Treeview.Heading"]:
            style.configure(tree_name, background=bg_col if "Heading" not in tree_name else head_bg, 
                            foreground=fg_col, fieldbackground=bg_col, rowheight=45, 
                            font=("Arial", 11, "bold" if "Heading" in tree_name else "normal"), borderwidth=0)

        style.map("Treeview", background=[('selected', '#3498DB')])

        self.status_tree.tag_configure("ACTIVE", foreground="#2ECC71", font=("Arial", 11, "bold")) 
        self.status_tree.tag_configure("AWAY", foreground="#F1C40F", font=("Arial", 11, "bold"))    
        self.status_tree.tag_configure("OFFLINE", foreground="#E74C3C", font=("Arial", 11, "bold"))
        
        for t in [self.info_tree, self.status_tree]:
            t.tag_configure('odd', background=odd_row_bg)

    def load_team_data(self):
        try:
            query = """
                SELECT employee_id, full_name, current_status, status 
                FROM users WHERE team_id = %s AND role != 'leader'
                ORDER BY full_name ASC
            """
            self.db.cursor.execute(query, (self.user['team_id'],))
            members = self.db.cursor.fetchall()

            for t in [self.info_tree, self.status_tree]: t.delete(*t.get_children())

            for i, m in enumerate(members):
                name_val = f" 👤 {m['full_name']}"
                loc = m['current_status'] or "Office"
                loc_val = f"🏢 {loc}" if loc == "Office" else f"🏠 {loc}"
                raw_status = (m['status'] or "offline").upper()
                act_val = f"● {raw_status}"

                row_tag = ('odd',) if i % 2 != 0 else ()
                self.info_tree.insert("", "end", values=(m['employee_id'], name_val, loc_val), tags=row_tag)
                self.status_tree.insert("", "end", values=(act_val,), tags=(raw_status,) + row_tag)

        except Exception as e:
            print(f"Table Error: {e}")

    def sync_scroll(self, container):
        """Creates a linked scrollbar and mousewheel sync"""
        # 1. Create the Scrollbar
        self.scrollbar = ttk.Scrollbar(container, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        # 2. Command: When scrollbar moves -> Move both trees
        def on_scrollbar_move(*args):
            self.info_tree.yview(*args)
            self.status_tree.yview(*args)
        
        self.scrollbar.config(command=on_scrollbar_move)

        # 3. Update Scrollbar: When either tree moves -> Update scrollbar position
        def on_tree_scroll(*args):
            self.scrollbar.set(*args)
            on_scrollbar_move("moveto", args[0]) # Force other tree to match

        self.info_tree.configure(yscrollcommand=on_tree_scroll)
        self.status_tree.configure(yscrollcommand=on_tree_scroll)

        # 4. Mousewheel binding (Optional but recommended for Windows/Linux)
        def on_mousewheel(event):
            # Move both based on delta
            self.info_tree.yview_scroll(int(-1*(event.delta/120)), "units")
            self.status_tree.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break" # Prevent double scroll

        self.info_tree.bind("<MouseWheel>", on_mousewheel)
        self.status_tree.bind("<MouseWheel>", on_mousewheel)

    def create_card(self, master, title, value, color):
        card = ctk.CTkFrame(master, height=120, corner_radius=15, 
                            border_width=1, border_color=("#E0E0E0", "#2B2B2B"), fg_color=("#FFFFFF", "#1E1E1E"))
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=("Arial", 13), text_color=("#888888", "#AAAAAA")).pack(pady=(20, 0))
        ctk.CTkLabel(card, text=value, font=("Arial", 32, "bold"), text_color=color).pack(pady=5)
        ctk.CTkFrame(card, height=5, fg_color=color).pack(fill="x", side="bottom")
        return card

    def auto_refresh(self):
        if self._is_destroyed: return
        self.refresh_stats()
        self.load_team_data()
        # Save ID to cancel on destroy
        self._after_id = self.after(15000, self.auto_refresh)

    # def refresh_stats(self):
    #     try:
    #         self.db.cursor.execute(
    #             "SELECT COUNT(*) as total, SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active "
    #             "FROM users WHERE team_id = %s AND role != 'leader'", (self.user['team_id'],)
    #         )
    #         stats_res = self.db.cursor.fetchone()
    #         team_size, active_count = stats_res['total'] or 0, stats_res['active'] or 0

    #         for w in self.stats_container.winfo_children(): w.destroy()
            
    #         card_data = [
    #             {"title": "Team Size", "value": str(team_size), "color": "#3498DB"},
    #             {"title": "Active Tasks", "value": "0", "color": "#10B981"},
    #             {"title": "Urgent OT", "value": "0", "color": "#E74C3C"},
    #             {"title": "On Duty", "value": f"{active_count}/{team_size}", "color": "#F39C12"}
    #         ]
    #         for item in card_data:
    #             card = self.create_card(self.stats_container, item['title'], item['value'], item['color'])
    #             card.pack(side="left", padx=(0, 20), expand=True, fill="both")
    #     except Exception as e: print(f"Stats Refresh Error: {e}")
    
    def refresh_stats(self):
        try:
            self.db.cursor.execute(
                "SELECT COUNT(*) as total, SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active "
                "FROM users WHERE team_id = %s AND role != 'leader'", (self.user['team_id'],)
            )
            stats_res = self.db.cursor.fetchone()
            team_size, active_count = stats_res['total'] or 0, stats_res['active'] or 0
 
            # Fetch Active Tasks count
            self.db.cursor.execute(
                    "SELECT COUNT(*) FROM tasks WHERE assigned_to = %s AND status != 'Completed'",
                    (self.user['full_name'],)
                )
            active_tasks_count = self.db.cursor.fetchone()['COUNT(*)'] or 0
 
            # Fetch Urgent OT (Pending Overtime Requests) count
            self.db.cursor.execute(
                "SELECT COUNT(*) FROM overtime_requests WHERE member_id = %s AND status = 'Pending'",
                (self.user['id'],)
            )
            urgent_ot_count = self.db.cursor.fetchone()['COUNT(*)'] or 0
 
            for w in self.stats_container.winfo_children(): w.destroy()
           
            card_data = [
                {"title": "Team Size", "value": str(team_size), "color": "#3498DB"},
                {"title": "Active Tasks", "value": str(active_tasks_count), "color": "#10B981"},
                {"title": "Urgent OT", "value": str(urgent_ot_count), "color": "#E74C3C"},
                {"title": "On Duty", "value": f"{active_count}/{team_size}", "color": "#F39C12"}
            ]
            for item in card_data:
                card = self.create_card(self.stats_container, item['title'], item['value'], item['color'])
                card.pack(side="left", padx=(0, 20), expand=True, fill="both")
        except Exception as e: print(f"Stats Refresh Error: {e}")
        
    def destroy(self):
        self._is_destroyed = True
        if self._after_id:
            self.after_cancel(self._after_id)
        super().destroy()