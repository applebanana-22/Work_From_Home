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
        self.team_container.grid(row=0, column=0, sticky="nsew", padx=100, pady=5)
 
        self.team_header = ctk.CTkFrame(self.team_container, fg_color="transparent")
        self.team_header.pack(fill="x", padx=20, pady=(10, 5))
       
        ctk.CTkLabel(self.team_header, text="👥 Team Updates",
                     font=("Arial", 20, "bold"), text_color="#D68910").pack(side="left")
 
        self.team_view = ctk.CTkScrollableFrame(
                            self.team_container,
                            fg_color="#121212",
                            corner_radius=12,
                            border_width=1,
                            border_color="#D68910"
                            )
        self.team_view.pack(fill="both", expand=True, padx=20, pady=5)
 
        # --- SEPARATOR LINE (အလယ်က မျဉ်းတား) ---
        self.sep = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.sep.grid(row=0, column=0, sticky="s", padx=40)
 
        # --- 2. LOWER HALF: COMPANY NEWS (From Admin) ---
        self.admin_container = ctk.CTkFrame(self, fg_color="transparent")
        self.admin_container.grid(row=1, column=0, sticky="nsew", padx=100, pady=5)
 
        self.admin_header = ctk.CTkFrame(self.admin_container, fg_color="transparent")
        self.admin_header.pack(fill="x", padx=20, pady=(15, 5))
       
        ctk.CTkLabel(self.admin_header, text="📢 Company Announcements",
                     font=("Arial", 20, "bold"), text_color="#2E86C1").pack(side="left")
 
        # Admin ဆီကလာတဲ့ စာတွက် Scroll area
        self.admin_view = ctk.CTkScrollableFrame(self.admin_container,
                                               fg_color="#121212",  
                                               corner_radius=12,
                                               border_width=1,
                                               border_color="#2E86C1")
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
           
    # start change
    def create_announcement_card(self, parent, data, theme_color):
 
        card = ctk.CTkFrame(
        parent,
        corner_radius=12,
        fg_color="#1E1E1E",
        border_width=1,
        border_color="#2A2A2A")
 
        card.pack(fill="x", pady=10, padx=15)
 
        # --- Main Row ---
        main = ctk.CTkFrame(card, fg_color="transparent")
        main.pack(fill="x", padx=12, pady=12 ,anchor="n")

        # 👤 Avatar (Initials)
        name = data['created_by']
        initials = "".join([n[0] for n in name.split()[:2]]).upper()

        avatar = ctk.CTkFrame(
            main,
            width=40,
            height=40,
            corner_radius=20,
            fg_color=theme_color
        )
        avatar.pack(side="left", padx=(0, 10), anchor="n")
        avatar.pack_propagate(False)

        ctk.CTkLabel(
            avatar,
            text=initials,
            font=("Arial", 14, "bold"),
            text_color="white"
        ).pack(expand=True)

        # RIGHT CONTENT
        right = ctk.CTkFrame(main, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        # --- Name + Time ---
        top = ctk.CTkFrame(right, fg_color="transparent")
        top.pack(fill="x", anchor="n")

        ctk.CTkLabel(
            top,
            text=name,
            font=("Arial", 13, "bold"),
            text_color="white"
        ).pack(side="left")

        time_str = data['created_at'].strftime("%Y-%m-%d | %I:%M %p")

        ctk.CTkLabel(
            top,
            text=time_str,
            font=("Arial", 10),
            text_color="#888"
        ).pack(side="left", padx=10)
 
        # --- Title ---
        ctk.CTkLabel(
            right,
        text=data['title'],
        font=("Arial", 14, "bold"),
        text_color="#DDDDDD"
        ).pack(anchor="w", pady=(5, 2))
        
     # --- Message ---
        message = data['message'] if data['message'] else ""
        preview_length = 30
        max_lines = 3
        msg_label = ctk.CTkLabel(
            right,
            text=message[:preview_length],
            font=("Arial", 13),
            wraplength=700,
            justify="left",
            anchor="w",
            text_color="#CCCCCC"
        )
        msg_label.pack(anchor="w")

        # --- See More (WORKING BUTTON) ---
        if len(message) > preview_length or message.count("\n") > max_lines:
            expanded = False

            def toggle():
                nonlocal expanded
                if not expanded:
                    msg_label.configure(text=message)
                    see_more.configure(text="see less")
                else:
                    msg_label.configure(text=message[:30])
                    see_more.configure(text="see more...")
                expanded = not expanded

            see_more = ctk.CTkButton(
                right,
                text="see more...",
                font=("Arial", 11),
                text_color="#2980B9",
                fg_color="transparent",
                hover=False,
                anchor="w",
                command=toggle
            )
            see_more.pack(anchor="w", pady=(2, 0)) 
 