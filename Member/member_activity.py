import customtkinter as ctk
from database import Database
from datetime import datetime

class MemberActivity(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user_data

        # 50/50 split ဖြစ်အောင် grid row weight သတ်မှတ်ခြင်း
        self.grid_rowconfigure(0, weight=1) # Team Section (Top 50%)
        self.grid_rowconfigure(1, weight=1) # Admin Section (Bottom 50%)
        self.grid_columnconfigure(0, weight=1)

        # --- 1. UPPER HALF: TEAM ANNOUNCEMENTS (From Leader) ---
        self.team_container = ctk.CTkFrame(self, fg_color="transparent")
        self.team_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        self.team_header = ctk.CTkFrame(self.team_container, fg_color="transparent")
        self.team_header.pack(fill="x", padx=20, pady=(10, 5))
        
        ctk.CTkLabel(self.team_header, text="👥 Team Updates", 
                     font=("Arial", 20, "bold"), text_color="#D68910").pack(side="left")

        # Leader ဆီကလာတဲ့ စာတွက် Scroll area
        self.team_view = ctk.CTkScrollableFrame(self.team_container, 
                                                label_text="From Your Leader", 
                                                label_font=("Arial", 13, "bold"),
                                                border_width=1, border_color="#D68910")
        self.team_view.pack(fill="both", expand=True, padx=20, pady=5)

        # --- SEPARATOR LINE (အလယ်က မျဉ်းတား) ---
        self.sep = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.sep.grid(row=0, column=0, sticky="s", padx=40)

        # --- 2. LOWER HALF: COMPANY NEWS (From Admin) ---
        self.admin_container = ctk.CTkFrame(self, fg_color="transparent")
        self.admin_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        self.admin_header = ctk.CTkFrame(self.admin_container, fg_color="transparent")
        self.admin_header.pack(fill="x", padx=20, pady=(15, 5))
        
        ctk.CTkLabel(self.admin_header, text="📢 Company News", 
                     font=("Arial", 20, "bold"), text_color="#2E86C1").pack(side="left")

        # Admin ဆီကလာတဲ့ စာတွက် Scroll area
        self.admin_view = ctk.CTkScrollableFrame(self.admin_container, 
                                                 label_text="Global Announcements", 
                                                 label_font=("Arial", 13, "bold"),
                                                 border_width=1, border_color="#2E86C1")
        self.admin_view.pack(fill="both", expand=True, padx=20, pady=5)

        self.refresh_feeds()

    def refresh_feeds(self):
        """Database ထဲက data တွေကို ဆွဲထုတ်ပြီး UI မှာ ပြပေးခြင်း"""
        # Clear existing content before reloading
        for w in self.team_view.winfo_children(): w.destroy()
        for w in self.admin_view.winfo_children(): w.destroy()

        try:
            # 1. Fetch Leader Posts (Team News)
            self.db.cursor.execute("""
                SELECT title, message, created_at, created_by 
                FROM announcements 
                WHERE sender_role='leader' 
                ORDER BY created_at DESC
            """)
            team_rows = self.db.cursor.fetchall()
            for row in team_rows:
                self.create_announcement_card(self.team_view, row, "#D68910")

            # 2. Fetch Admin Posts (Company News)
            self.db.cursor.execute("""
                SELECT title, message, created_at, created_by 
                FROM announcements 
                WHERE sender_role='admin' 
                ORDER BY created_at DESC
            """)
            admin_rows = self.db.cursor.fetchall()
            for row in admin_rows:
                self.create_announcement_card(self.admin_view, row, "#2E86C1")

        except Exception as e:
            print(f"Error loading feeds: {e}")

    def create_announcement_card(self, parent, data, theme_color):
        """Card တစ်ခုချင်းစီကို visual ကောင်းအောင် ပုံဖော်ခြင်း"""
        card = ctk.CTkFrame(parent, corner_radius=10, border_width=1, border_color="gray30")
        card.pack(fill="x", pady=8, padx=10)

        # Top Row: Title & Date
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(10, 5))

        ctk.CTkLabel(header, text=data['title'], font=("Arial", 15, "bold")).pack(side="left")
        
        # Date Format: 2026-03-30 | 11:30 AM
        time_str = data['created_at'].strftime("%Y-%m-%d | %I:%M %p")
        ctk.CTkLabel(header, text=time_str, font=("Arial", 10), text_color="gray60").pack(side="right")

        # Message Content
        msg_body = ctk.CTkLabel(card, text=data['message'], font=("Arial", 13), 
                                wraplength=500, justify="left", anchor="w", text_color="gray85")
        msg_body.pack(fill="x", padx=15, pady=(0, 10))

        # Bottom Row: Posted by user name
        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.pack(fill="x", padx=15, pady=(0, 5))
        
        ctk.CTkLabel(footer, text=f"By: {data['created_by']}", 
                     font=("Arial", 9, "italic"), text_color=theme_color).pack(side="right")