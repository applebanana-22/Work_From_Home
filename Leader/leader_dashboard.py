import customtkinter as ctk

class LeaderDashboard(ctk.CTkFrame):
    def __init__(self, master, user, db):
        super().__init__(master, fg_color="transparent")
        self.user = user
        self.db = db

        # --- Welcome Section ---
        self.welcome_f = ctk.CTkFrame(self, fg_color="transparent")
        self.welcome_f.pack(fill="x", padx=40, pady=(40, 20))

        ctk.CTkLabel(self.welcome_f, 
                     text=f"Welcome back, {self.user['full_name']}! 👋", 
                     font=("Arial", 28, "bold"), 
                     text_color=("#1A1A1A", "#FFFFFF")).pack(anchor="w")
        
        ctk.CTkLabel(self.welcome_f, 
                     text="Here is your team's performance overview for today.", 
                     font=("Arial", 14), 
                     text_color="gray").pack(anchor="w", pady=5)

        # --- Stats Container ---
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=40, pady=20)

        self.refresh_stats()

    def refresh_stats(self):
        for w in self.stats_container.winfo_children(): w.destroy()

        # Team specs: 11 members logic
        stats = [
            {"title": "Total Members", "value": "11", "color": "#3498DB"},
            {"title": "Active Projects", "value": "3", "color": "#10B981"},
            {"title": "Pending OT", "value": "2", "color": "#F39C12"},
            {"title": "Today's Attendance", "value": "9/11", "color": "#9B59B6"}
        ]

        for item in stats:
            card = self.create_card(self.stats_container, item['title'], item['value'], item['color'])
            card.pack(side="left", padx=(0, 20))

    def create_card(self, master, title, value, color):
        card = ctk.CTkFrame(master, width=180, height=110, corner_radius=12, 
                            border_width=1, border_color=("#E0E0E0", "#333333"))
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=("Arial", 12), text_color="gray").pack(pady=(15, 0))
        ctk.CTkLabel(card, text=value, font=("Arial", 28, "bold"), text_color=color).pack(pady=5)
        line = ctk.CTkFrame(card, height=4, fg_color=color, corner_radius=2)
        line.pack(fill="x", side="bottom", padx=15, pady=(0, 10))
        return card