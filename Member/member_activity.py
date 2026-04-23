import customtkinter as ctk
from database import Database


class MemberActivity(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")

        self.db = Database()
        self.user = user_data

        # layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ================= STATE =================
        self.current_view = "team"   # default

        # ================= HEADER (TABS) =================
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=100, pady=(10, 5))

        self.team_btn = ctk.CTkButton(
            header,
            text="👥 Team Updates",
            fg_color="gray30",
            corner_radius=20,
            command=lambda: self.switch_view("team")
        )
        self.team_btn.pack(side="left", padx=5)

        self.admin_btn = ctk.CTkButton(
            header,
            text="📢 Company Announcements",
            fg_color="gray30",
            corner_radius=20,
            command=lambda: self.switch_view("admin")
        )
        self.admin_btn.pack(side="left", padx=5)

        # ================= CONTAINERS =================
        # (Same position → switch with show/hide)
        self.team_container = ctk.CTkFrame(self, fg_color="transparent")
        self.team_container.pack(fill="both", expand=True, padx=100, pady=5)

        self.admin_container = ctk.CTkFrame(self, fg_color="transparent")
        self.admin_container.pack(fill="both", expand=True, padx=100, pady=5)

        # ================= TEAM VIEW =================
        self.team_view = ctk.CTkScrollableFrame(
            self.team_container,
            fg_color=("#F5F5F5", "#121212"),
            corner_radius=12,
            border_width=1,
            border_color="#2E86C1"
        )
        self.team_view.pack(fill="both", expand=True, padx=20, pady=5)

        # ================= ADMIN VIEW =================
        self.admin_view = ctk.CTkScrollableFrame(
            self.admin_container,
            fg_color=("#F5F5F5", "#121212"),
            corner_radius=12,
            border_width=1,
            border_color="#2E86C1"
        )
        self.admin_view.pack(fill="both", expand=True, padx=20, pady=5)

        # initial load
        self.refresh_feeds()

    # ================= SWITCH TAB =================
    def switch_view(self, view):
        self.current_view = view

        if view == "team":
            self.team_btn.configure(fg_color="#2E86C1")
            self.admin_btn.configure(fg_color="gray30")
        else:
            self.team_btn.configure(fg_color="gray30")
            self.admin_btn.configure(fg_color="#2E86C1")

        self.refresh_feeds()

    # ================= LOAD DATA =================
    def refresh_feeds(self):
        # clear
        for w in self.team_view.winfo_children():
            w.destroy()
        for w in self.admin_view.winfo_children():
            w.destroy()

        if self.current_view == "team":
            self.team_container.pack(fill="both", expand=True, padx=100, pady=5)
            self.admin_container.pack_forget()

            self.db.cursor.execute("""
                SELECT id, title, message, created_at, created_by
                FROM announcements
                WHERE sender_role='leader'
                ORDER BY created_at DESC
            """)

            for row in self.db.cursor.fetchall():
                self.create_card(self.team_view, row, "#2E86C1")

        else:
            self.admin_container.pack(fill="both", expand=True, padx=100, pady=5)
            self.team_container.pack_forget()

            self.db.cursor.execute("""
                SELECT id, title, message, created_at, created_by
                FROM announcements
                WHERE sender_role='admin'
                ORDER BY created_at DESC
            """)

            for row in self.db.cursor.fetchall():
                self.create_card(self.admin_view, row, "#2E86C1")

    # ================= CARD =================
    def create_card(self, parent, data, theme_color):
        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color=("#FFFFFF", "#1E1E1E"),
            border_width=1,
            border_color="#2A2A2A"
        )
        card.pack(fill="x", pady=10, padx=15)

        main = ctk.CTkFrame(card, fg_color="transparent")
        main.pack(fill="x", padx=12, pady=12)

        # avatar
        name = data['created_by']
        initials = "".join([n[0] for n in name.split()[:2]]).upper()

        avatar = ctk.CTkFrame(
            main,
            width=40,
            height=40,
            corner_radius=20,
            fg_color=theme_color
        )
        avatar.pack(side="left",padx=(0, 10), anchor="n")
        avatar.pack_propagate(False)

        ctk.CTkLabel(avatar, text=initials,
                             font=("Arial", 14, "bold"),
                             text_color=("black", "white")).pack(expand=True)

        # right content
        right = ctk.CTkFrame(main, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        # name + time
        top = ctk.CTkFrame(right, fg_color="transparent")
        top.pack(fill="x")

        time_str = data['created_at'].strftime("%Y-%m-%d | %I:%M %p")

        ctk.CTkLabel(top, text=name,
                     font=("Arial", 13, "bold"),
                     text_color=("black", "white")).pack(side="left")

        ctk.CTkLabel(top, text=time_str,
                     font=("Arial", 10),
                     text_color="#888").pack(side="left", padx=10)

        # title
        ctk.CTkLabel(
            right,
            text=data['title'],
            font=("Arial", 14, "bold"),
            text_color=("black", "white")
        ).pack(anchor="w", pady=(5, 2))

        # message
        self.create_expandable_message(right, data['message'])
        
        # ================= SHOW REPLIES =================
        self.db.cursor.execute(
            "SELECT * FROM announcement_replies WHERE announcement_id=%s ORDER BY created_at ASC",
            (data['id'],)
        )

        replies = self.db.cursor.fetchall()

        MAX_VISIBLE_REPLIES = 3

        if replies:
            replies_container = ctk.CTkFrame(right, fg_color="transparent")
            replies_container.pack(fill="x", padx=5, pady=(5, 0))

            def render_replies(show_all=False, replies_list=replies, container=replies_container):
                # clear old
                for w in container.winfo_children():
                    w.destroy()

                visible = replies_list if show_all else replies_list[:MAX_VISIBLE_REPLIES]

                for reply in visible:
                    reply_box = ctk.CTkFrame(
                        container,
                        fg_color=("#F5F5F5", "#2A2A2A"),
                        corner_radius=8
                    )
                    reply_box.pack(fill="x", padx=10, pady=3)

                    r_name = reply.get("created_by", "User")
                    r_msg = reply.get("message", "")
                    r_time = reply['created_at'].strftime("%Y-%m-%d | %I:%M %p")

                    ctk.CTkLabel(
                        reply_box,
                        text=f"{r_name} ({r_time})",
                        font=("Arial", 11, "bold"),
                        text_color=("gray40", "#AAAAAA")
                    ).pack(anchor="w", padx=8, pady=(3, 0))

                    ctk.CTkLabel(
                        reply_box,
                        text=r_msg,
                        font=("Arial", 12),
                        text_color=("black", "#DDDDDD"),
                        wraplength=600,
                        justify="left"
                    ).pack(anchor="w", padx=8, pady=(0, 5))

                # toggle button
                if len(replies_list) > MAX_VISIBLE_REPLIES:
                    toggle = ctk.CTkLabel(
                        container,
                        text=f"Show all replies ({len(replies_list)})" if not show_all else "Show less",
                        text_color="#4DA6FF",
                        font=("Arial", 11, "underline"),
                        cursor="hand2"
                    )
                    toggle.pack(anchor="w", padx=12, pady=(2, 5))

                    toggle.bind(
                        "<Button-1>",
                        lambda e, state=show_all, rl=replies_list, c=container:
                        render_replies(not state, rl, c)
                    )

            render_replies(False)
        else:
            ctk.CTkLabel(
                right,
                text="No replies yet.",
                text_color=("gray40", "#777777"),
                font=("Arial", 11)
            ).pack(anchor="w", padx=10, pady=(5, 0))
            
        # ================= REPLY INPUT =================
        reply_frame = ctk.CTkFrame(right, fg_color="transparent")
        reply_frame.pack(fill="x", padx=10, pady=(5, 5))

        reply_entry = ctk.CTkTextbox(
                reply_frame,
                height=35,
               fg_color=("#EEEEEE", "#2A2A2A"),
                corner_radius=8,
                wrap="word"
            )
        reply_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

            # Placeholder text
        placeholder_text = "Write a reply..."
        reply_entry.insert("1.0", placeholder_text)
        reply_entry.configure(text_color=("black", "white"))

        def clear_placeholder(event, box=reply_entry):
                if box.get("1.0", "end-1c") == placeholder_text:
                    box.delete("1.0", "end")
                    box.configure(text_color=("black", "white"))

        def restore_placeholder(event, box=reply_entry):
                if not box.get("1.0", "end-1c").strip():
                    box.insert("1.0", placeholder_text)
                    box.configure(text_color=("black", "white"))

        reply_entry.bind("<FocusIn>", clear_placeholder)
        reply_entry.bind("<FocusOut>", restore_placeholder)

        announcement_id = data['id']

            # Send button
        ctk.CTkButton(
                reply_frame,
                text="➤",
                width=35,
                height=35,
                fg_color="#0A93F5",
                hover_color="#0873C4",
                command=lambda a_id=announcement_id, e=reply_entry:
                    self.add_reply(a_id, e)
            ).pack(side="right")

            # Ctrl + Enter to send reply
        reply_entry.bind(
                "<Control-Return>",
                lambda event, a_id=announcement_id, e=reply_entry:
                    self.send_with_ctrl_enter(event, a_id, e)
            )
    def add_reply(self, announcement_id, textbox):
        try:
            reply_text = textbox.get("1.0", "end-1c").strip()

            if not reply_text or reply_text == "Write a reply...":
                return

            self.db.insert_reply(announcement_id, self.user, reply_text)

            textbox.delete("1.0", "end")
            textbox.insert("1.0", "Write a reply...")
            textbox.configure(text_color="gray")

            self.refresh_feeds()

        except Exception as e:
            print("Reply Error:", e)
    
    def send_with_ctrl_enter(self, event, announcement_id, textbox):
        self.add_reply(announcement_id, textbox)
        return "break"
    
    def create_expandable_message(self, parent, full_text):
        preview_length = 80

        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", pady=(2, 0))

        is_expanded = False

        def toggle():
            nonlocal is_expanded
            is_expanded = not is_expanded

            if is_expanded:
                msg_label.configure(text=full_text)
                toggle_btn.configure(text="see less")
            else:
                msg_label.configure(text=full_text[:preview_length] + "...")
                toggle_btn.configure(text="see more...")

        short_text = full_text[:preview_length] + ("..." if len(full_text) > preview_length else "")

        msg_label = ctk.CTkLabel(
            container,
            text=short_text,
            wraplength=700,
            justify="left",
            text_color=("black", "#CCCCCC")
        )
        msg_label.pack(anchor="w")

        if len(full_text) > preview_length:
            toggle_btn = ctk.CTkButton(
                container,
                text="see more...",
                fg_color="transparent",
                hover=False,
                text_color="#4DA6FF",
                font=("Arial", 11),
                command=toggle
            )
            toggle_btn.pack(anchor="w")