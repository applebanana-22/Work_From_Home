from turtle import right
from tkinter import messagebox
import customtkinter as ctk
from database import Database
from datetime import datetime
import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk

class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None):
        super().__init__(master, fg_color="transparent")
        self._date = initial_date or datetime.today().date()
        self._open = False
        
        # Calendar style setup
        self.update_calendar_style()
        
        self.btn = ctk.CTkButton(
            self,
            text=self._fmt(),
            width=140,
            height=36,
            corner_radius=8,
            hover_color=("#EBEBEB", "#2A2A2A"),
            border_width=1,
            fg_color=("#F9F9F9", "#1E1E1E"),
            border_color=("#DBDBDB", "#2C2C2C"),
            text_color=("black", "white"),
            anchor="w",
            command=self.toggle
        )
        self.btn.pack()
        
        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color=("#FFFFFF", "#141E2B"),
            corner_radius=12,
            border_width=1,
            border_color=("#DBDBDB", "#2A3A4A")
        )
        
        self.cal = Calendar(
            self.panel,
            style="Custom.Calendar",
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            year=self._date.year,
            month=self._date.month,
            day=self._date.day,
            showweeknumbers=False,
            firstweekday="monday",
            font=("Arial", 11),
            cursor="hand2"
        )
        self.cal.pack(padx=8, pady=8)
        self.cal.bind("<<CalendarSelected>>", self._select)

    def update_calendar_style(self):
        # TTK styles are global and don't support tuples, 
        # so we refresh this specifically when the picker is toggled.
        is_dark = ctk.get_appearance_mode() == "Dark"
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Calendar",
            background="#1A1A2E" if is_dark else "#FFFFFF",
            foreground="white" if is_dark else "black",
            headersbackground="#16213E" if is_dark else "#F0F0F0",
            headersforeground="#4FC3F7" if is_dark else "#1f538d",
            selectbackground="#3498DB",
            selectforeground="white",
            normalbackground="#1A1A2E" if is_dark else "#FFFFFF",
            normalforeground="#CCCCCC" if is_dark else "#333333",
            weekendbackground="#1A1A2E" if is_dark else "#F9F9F9",
            weekendforeground="#F39C12",
            othermonthforeground="#555555" if is_dark else "#AAAAAA",
            bordercolor="#2A2A4A" if is_dark else "#DBDBDB",
            relief="flat"
        )

    def toggle(self):
        if self._open:
            self.panel.place_forget()
        else:
            self.update_calendar_style()
            self.panel.lift()
            self.panel.place(in_=self, x=0, y=self.btn.winfo_height() + 2)
        self._open = not self._open

    def _select(self, event):
        selected = self.cal.get_date()
        self._date = datetime.strptime(selected, "%Y-%m-%d").date()
        self.btn.configure(text=self._fmt())
        self.toggle()

    def get_date(self): return self._date

    def set_date(self, d):
        self._date = d
        self.cal.selection_set(d)
        self.btn.configure(text=self._fmt())

    def _fmt(self): return f"  📅  {self._date.strftime('%Y-%m-%d')}"

class MemberActivity(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")

        self.db = Database()
        self.user = user_data
        self.date_filter_active = False
        self.current_search_keyword = ""

        # layout
        self.grid_rowconfigure(0, weight=1)
        
        self.grid_columnconfigure(0, weight=1)

        # ================= STATE =================
        self.current_view = "team"   # default

        # ================= HEADER (TABS) =================
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=80, pady=(10, 5))

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
        
        self.search_var = ctk.StringVar()

        search_container = ctk.CTkFrame(
            header,
            width=220,
            height=42,
            corner_radius=14,
            fg_color=("#F3F2F1", "#2A2A2A"),
            border_width=1,
            border_color="#555555"
        )
        search_container.pack(side="right", padx=(10, 0))
        search_container.pack_propagate(False)

        ctk.CTkLabel(
            search_container,
            text="⌕",
            font=("Segoe UI Symbol", 18),
            text_color="#777777"
        ).pack(side="left", padx=(18, 10))

        self.search_entry = ctk.CTkEntry(
            search_container,
            textvariable=self.search_var,
            placeholder_text="Search announcements...",
            placeholder_text_color="#888888",
            fg_color="transparent",
            border_width=0,
            text_color=("black", "white"),
            font=("Arial", 13)
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 18), pady=6)
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_announcements())

        filter_row = ctk.CTkFrame(header, fg_color="transparent")
        filter_row.pack(side="right", padx=(10, 0))

        ctk.CTkLabel(filter_row, text="From:", text_color=("black", "white")).pack(side="left", padx=(0, 5))
        self.from_date_entry = DatePickerButton(filter_row, initial_date=datetime.today().date())
        self.from_date_entry.pack(side="left", padx=(0, 12))

        ctk.CTkLabel(filter_row, text="To:", text_color=("black", "white")).pack(side="left", padx=(0, 5))
        self.to_date_entry = DatePickerButton(filter_row, initial_date=datetime.today().date())
        self.to_date_entry.pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            filter_row, text="🔍 Filter", width=80, height=36,
            fg_color="#2471A3", hover_color="#1A5276",
            font=("Arial", 12, "bold"),
            command=self.apply_date_filter
        ).pack(side="left", padx=4)

        self.clear_btn = ctk.CTkButton(
            filter_row,
            text="✖ Clear",
            width=90,
            height=36,
            fg_color="#566573",
            hover_color="#424949",
            font=("Arial", 12, "bold"),
            command=self.clear_date_filter
        )
        self.clear_btn.pack(side="left", padx=(6, 0))
        
        # ================= CONTAINERS =================
        # (Same position → switch with show/hide)
        self.team_container = ctk.CTkFrame(self, fg_color="transparent")
        self.team_container.pack(fill="both", expand=True, padx=80, pady=5)

        self.admin_container = ctk.CTkFrame(self, fg_color="transparent")
        self.admin_container.pack(fill="both", expand=True, padx=80, pady=5)

        # ================= TEAM VIEW =================
        self.team_view = ctk.CTkScrollableFrame(
            self.team_container,
            fg_color=("#D1D1D1", "#444444"),
            corner_radius=12,
            border_width=1,
            # border_color="#2E86C1"
        )
        self.team_view.pack(fill="both", expand=True, padx=0, pady=5)

        # ================= ADMIN VIEW =================
        self.admin_view = ctk.CTkScrollableFrame(
            self.admin_container,
            fg_color=("#D1D1D1", "#444444"),
            corner_radius=12,
            border_width=1,
            # border_color="#2E86C1"
        )
        self.admin_view.pack(fill="both", expand=True, padx=0, pady=5)

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
        
        
    def apply_date_filter(self):
            self.date_filter_active = True
            self.refresh_feeds()

    def clear_date_filter(self):
            self.date_filter_active = False
            today = datetime.today().date()
            self.from_date_entry.set_date(today)
            self.to_date_entry.set_date(today)
            self.current_search_keyword = ""
            self.search_var.set("")
            self.refresh_feeds()
    def search_announcements(self):
            self.current_search_keyword = self.search_var.get().strip()
            self.refresh_feeds()
    def refresh_feeds(self):
        for w in self.team_view.winfo_children():
            w.destroy()
        for w in self.admin_view.winfo_children():
            w.destroy()
        if self.current_view == "team":
            self.team_container.pack(fill="both", expand=True, padx=80, pady=5)
            self.admin_container.pack_forget()
            parent = self.team_view
            sender_role = "leader"
        else:
            self.admin_container.pack(fill="both", expand=True, padx=80, pady=5)
            self.team_container.pack_forget()
            parent = self.admin_view
            sender_role = "admin"
        query = """
            SELECT id, title, message, created_at, created_by,user_id
            FROM announcements
            WHERE sender_role=%s
        """
        params = [sender_role]
        if self.date_filter_active:
            query += " AND DATE(created_at) >= %s AND DATE(created_at) <= %s"
            params.extend([
                str(self.from_date_entry.get_date()),
                str(self.to_date_entry.get_date())
            ])

        if self.current_search_keyword:
            keyword = f"%{self.current_search_keyword}%"
            query += """
                AND (
                    title LIKE %s
                    OR message LIKE %s
                    OR id IN (
                        SELECT announcement_id
                        FROM announcement_replies
                        WHERE message LIKE %s
                    )
                )
            """
            params.extend([keyword, keyword, keyword])

        query += " ORDER BY created_at DESC"

        self.db.cursor.execute(query, tuple(params))
        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(
                parent,
                text="No announcements found for selected date.",
                font=("Arial", 13),
                text_color=("black", "white")
            ).pack(pady=30)
            return

        for row in rows:
            self.create_card(parent, row, "#2E86C1")
            
    def show_post_menu(self, button, row):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()
            return

        self.active_menu = ctk.CTkToplevel(self)
        self.active_menu.overrideredirect(True)
        self.active_menu.attributes("-topmost", True)
        self.active_menu.configure(fg_color=("#FFFFFF", "#2B2B2B"))

        x = button.winfo_rootx() - 115
        y = button.winfo_rooty() + button.winfo_height() + 5
        self.active_menu.geometry(f"150x95+{x}+{y}")

        menu_frame = ctk.CTkFrame(self.active_menu, corner_radius=8, border_width=1, border_color="#555555")
        menu_frame.pack(fill="both", expand=True)

        edit_btn = ctk.CTkButton(
            menu_frame,
            text="🖉  Edit",
            height=38,
            fg_color="transparent",
            hover_color=("#EEEEEE", "#3A3A3A"),
            text_color=("black", "white"),
            anchor="w"
        )
        edit_btn.pack(fill="x", padx=6, pady=(6, 0))

        edit_btn.configure(
            command=lambda r=row: self.menu_edit(r)
        )

        ctk.CTkButton(
            menu_frame, text="✖ Delete", height=38,
            fg_color="transparent", anchor="w",
            command=lambda i=row["id"]: self.menu_delete(i)
        ).pack(fill="x", padx=6, pady=(0, 6))
        
    
    def menu_edit(self, row):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        self.winfo_toplevel().unbind("<Button-1>")
        self.edit_post(row)


    def edit_post(self, row):
        self.pack_forget()

        self.master.member_edit_page = MemberEditPostPage(
            self.master,
            self.user,
            edit_data=row,
            back_callback=self.back_from_edit_post
        )
        self.master.member_edit_page.pack(fill="both", expand=True)
    def show_reply_menu(self, button, reply):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()
            return

        self.active_menu = ctk.CTkToplevel(self)
        self.active_menu.overrideredirect(True)
        self.active_menu.attributes("-topmost", True)
        self.active_menu.configure(fg_color=("#FFFFFF", "#2B2B2B"))

        menu_width = 150
        menu_height = 95

        x = button.winfo_rootx() - menu_width + button.winfo_width()
        y = button.winfo_rooty() + button.winfo_height() + 5

        self.active_menu.geometry(f"{menu_width}x{menu_height}+{x}+{y}")

        menu_frame = ctk.CTkFrame(
            self.active_menu,
            fg_color=("#FFFFFF", "#2B2B2B"),
            corner_radius=8,
            border_width=1,
            border_color="#555555"
        )
        menu_frame.pack(fill="both", expand=True)

        ctk.CTkButton(
            menu_frame,
            text="🖉  Edit",
            height=38,
            fg_color="transparent",
            hover_color=("#EEEEEE", "#3A3A3A"),
            text_color=("black", "white"),
            anchor="w",
            command=lambda r=reply: self.edit_reply(r)
        ).pack(fill="x", padx=6, pady=(6, 0))

        ctk.CTkButton(
            menu_frame,
            text="✖ Delete",
            height=38,
            fg_color="transparent",
            hover_color=("#FFE5E5", "#4A2A2A"),
            text_color=("black", "white"),
            anchor="w",
            command=lambda r=reply: self.delete_reply(r)
        ).pack(fill="x", padx=6, pady=(0, 6))


    def edit_reply(self, reply):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        print("Edit reply:", reply)
        
    def delete_reply(self, reply):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        try:
            self.db.cursor.execute(
                "DELETE FROM announcement_replies WHERE id=%s AND user_id=%s",
                (reply["id"], self.user["id"])
            )
            self.db.conn.commit()
            self.refresh_feeds()

        except Exception as e:
            print("Delete reply error:", e)
    def delete_post(self, ann_id):
       

        if messagebox.askyesno("Confirm Delete", "Delete this post?"):
            self.db.cursor.execute(
                "DELETE FROM announcements WHERE id=%s AND user_id=%s",
                (ann_id, self.user["id"])
            )
            self.db.conn.commit()
            self.refresh_feeds()


    def edit_post(self, row):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        self.pack_forget()

        self.master.member_edit_page = MemberEditPostPage(
            self.master,
            self.user,
            edit_data=row,
            back_callback=self.back_from_edit_post
        )
        self.master.member_edit_page.pack(fill="both", expand=True)
    def back_from_edit_post(self):
        if hasattr(self.master, "member_edit_page") and self.master.member_edit_page.winfo_exists():
            self.master.member_edit_page.destroy()

        self.db = Database()
        self.pack(fill="both", expand=True)
        self.refresh_feeds()
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

        right = ctk.CTkFrame(main, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        CONTENT_PADX = 12

        # name + time FIRST
        top = ctk.CTkFrame(right, fg_color="transparent")
        top.pack(fill="x", padx=CONTENT_PADX)

        # title/message/replies/input
        content_frame = ctk.CTkFrame(right, fg_color="transparent")
        content_frame.pack(fill="x", padx=CONTENT_PADX)

        time_str = data['created_at'].strftime("%Y-%m-%d | %I:%M %p")

        ctk.CTkLabel(top, text=name,
                     font=("Arial", 13, "bold"),
                     text_color=("black", "white")).pack(side="left")

        ctk.CTkLabel(top, text=time_str,
                     font=("Arial", 10),
                     text_color="#888").pack(side="left", padx=10)

        if str(data.get("user_id")) == str(self.user.get("id")):
            menu_btn = ctk.CTkButton(
                top,
                text="⋯",
                width=35,
                height=28,
                fg_color="transparent",
                hover_color=("#E5E5E5", "#333333"),
                text_color=("black", "white"),
                font=("Arial", 18, "bold")
            )
            menu_btn.pack(side="right", padx=5)

            menu_btn.configure(
                command=lambda b=menu_btn, r=data: self.show_post_menu(b, r)
            )
        # title
        self.highlight_text(
            content_frame,
            data['title'],
            font=("Arial", 14, "bold"),
            height=1,
            pady=(5, 2)
        )

        # message
        self.create_expandable_message(
            content_frame,
            data['message'],
            padx=12,
            keyword=self.current_search_keyword
        )
                
        # ================= SHOW REPLIES =================
        self.db.cursor.execute(
            "SELECT * FROM announcement_replies WHERE announcement_id=%s ORDER BY created_at ASC",
            (data['id'],)
        )

        replies = self.db.cursor.fetchall()

        MAX_VISIBLE_REPLIES = 2

        if replies:
            replies_container = ctk.CTkFrame(content_frame, fg_color="transparent")
            replies_container.pack(fill="x", padx=0, pady=(5, 0))

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
                    reply_box.pack(fill="x", padx=12, pady=3)

                    r_name = reply.get("created_by", "User")
                    r_msg = reply.get("message", "")
                    r_time = reply['created_at'].strftime("%Y-%m-%d | %I:%M %p")

                    reply_top = ctk.CTkFrame(reply_box, fg_color="transparent")
                    reply_top.pack(fill="x", padx=8, pady=(3, 0))

                    ctk.CTkLabel(
                        reply_top,
                        text=f"{r_name} ({r_time})",
                        font=("Arial", 11, "bold"),
                        text_color=("gray40", "#AAAAAA")
                    ).pack(side="left")

                    if str(reply.get("user_id")) == str(self.user.get("id")):
                        reply_menu_btn = ctk.CTkButton(
                            reply_top,
                            text="⋯",
                            width=30,
                            height=24,
                            fg_color="transparent",
                            hover_color=("#E5E5E5", "#333333"),
                            text_color=("black", "white"),
                            font=("Arial", 16, "bold")
                        )
                        reply_menu_btn.pack(side="right")

                        reply_menu_btn.configure(
                            command=lambda b=reply_menu_btn, rp=reply: self.show_reply_menu(b, rp)
                        )

                    self.highlight_text(
                        reply_box,
                        r_msg,
                        font=("Arial", 12),
                        height=2,
                        padx=8,
                        pady=(0, 5),
                        bg_parent=True
                    )

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
                content_frame,
                text="No replies yet.",
                text_color=("gray40", "#777777"),
                font=("Arial", 11)
            ).pack(anchor="w", padx=12, pady=(5, 5))
            
        # ================= REPLY INPUT =================
        reply_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        reply_frame.pack(fill="x", padx=12, pady=(5, 8))

        reply_frame.grid_columnconfigure(0, weight=1)
        reply_frame.grid_columnconfigure(1, weight=0)

        placeholder_text = "Write a reply..."

        reply_entry = ctk.CTkTextbox(
            reply_frame,
            height=35,
            fg_color=("#EEEEEE", "#2A2A2A"),
            text_color="#888888",
            corner_radius=8,
            border_width=0,
            wrap="word",
            font=("Arial", 13)
        )
        reply_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        reply_entry.insert("1.0", placeholder_text)

        send_btn = ctk.CTkButton(
            reply_frame,
            text="➤",
            width=45,
            height=35,
            fg_color="#0A93F5",
            hover_color="#087ACC",
            border_width=0,
            font=("Arial", 18),
            command=lambda a_id=data['id'], e=reply_entry: self.add_reply(a_id, e)
        )
        send_btn.grid(row=0, column=1, sticky="se")


        def resize_reply_box(box=reply_entry, btn=send_btn):
            text = box.get("1.0", "end-1c")

            if text == placeholder_text or not text.strip():
                new_height = 35
            else:
                lines = int(box.index("end-1c").split(".")[0])
                new_height = 35 + ((lines - 1) * 22)

                if new_height > 220:
                    new_height = 220

            box.configure(height=new_height)
            btn.grid_configure(sticky="se", pady=(new_height - 35, 0))


        def clear_placeholder(event, box=reply_entry):
            if box.get("1.0", "end-1c") == placeholder_text:
                box.delete("1.0", "end")
                box.configure(text_color=("black", "white"))
                resize_reply_box(box)


        def restore_placeholder(event, box=reply_entry):
            if not box.get("1.0", "end-1c").strip():
                box.delete("1.0", "end")
                box.insert("1.0", placeholder_text)
                box.configure(text_color="#888888")
                resize_reply_box(box)


        def on_key_release(event, box=reply_entry):
            resize_reply_box(box)


        def handle_enter(event, a_id=data['id'], box=reply_entry):
            if event.state & 0x0001:   # Shift + Enter = new line
                box.insert("insert", "\n")
                box.after(10, lambda: resize_reply_box(box))
                return "break"

            self.add_reply(a_id, box)   # Enter = send
            return "break"


        reply_entry.bind("<FocusIn>", clear_placeholder)
        reply_entry.bind("<FocusOut>", restore_placeholder)
        reply_entry.bind("<KeyRelease>", on_key_release)
        reply_entry.bind("<Return>", handle_enter)
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
            
    def highlight_text(self, parent, text, font=("Arial", 12), height=1, padx=0, pady=0, bg_parent=False):
        is_dark = ctk.get_appearance_mode() == "Dark"

        txt = tk.Text(
            parent,
            height=height,
            wrap="word",
            bg="#2A2A2A" if bg_parent and is_dark else ("#1E1E1E" if is_dark else "#FFFFFF"),
            fg="white" if is_dark else "black",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=font,
            cursor="arrow",
            takefocus=0
        )
        txt.pack(anchor="w", fill="x", padx=padx, pady=pady)

        txt.insert("1.0", text)

        keyword = self.current_search_keyword
        if keyword:
            lower_text = text.lower()
            lower_keyword = keyword.lower()
            start_index = lower_text.find(lower_keyword)

            while start_index != -1:
                end_index = start_index + len(keyword)
                txt.tag_add("highlight", f"1.{start_index}", f"1.{end_index}")
                start_index = lower_text.find(lower_keyword, end_index)

            txt.tag_config("highlight", background="#FFD54F", foreground="black")

        txt.configure(state="disabled")
    
    def send_with_ctrl_enter(self, event, announcement_id, textbox):
        self.add_reply(announcement_id, textbox)
        return "break"
    
    def create_expandable_message(self, parent, full_text, padx=20, keyword=""):
        is_dark = ctk.get_appearance_mode() == "Dark"
        preview_length = 80

        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=padx, pady=(2,5))

        is_expanded = False

        msg_text = tk.Text(
            container,
            wrap="word",
            height=2,
            bg="#1E1E1E" if is_dark else "#FFFFFF",
            fg="white" if is_dark else "black",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=("Arial", 12),
            cursor="arrow",
            takefocus=0
        )
        msg_text.pack(fill="x", anchor="w")

        def apply_text(text_to_show):
            msg_text.configure(state="normal")
            msg_text.delete("1.0", "end")
            msg_text.insert("1.0", text_to_show)

            if keyword:
                lower_text = text_to_show.lower()
                lower_keyword = keyword.lower()
                start_index = lower_text.find(lower_keyword)

                while start_index != -1:
                    end_index = start_index + len(keyword)
                    msg_text.tag_add("highlight", f"1.{start_index}", f"1.{end_index}")
                    start_index = lower_text.find(lower_keyword, end_index)

                msg_text.tag_config(
                    "highlight",
                    background="#FFD54F",
                    foreground="black",
                    font=("Arial", 12, "bold")
                )

            msg_text.configure(state="disabled")

        def toggle():
            nonlocal is_expanded
            is_expanded = not is_expanded

            if is_expanded:
                apply_text(full_text)
                toggle_btn.configure(text="see less")
            else:
                apply_text(full_text[:preview_length] + "...")
                toggle_btn.configure(text="see more...")

        display_text = full_text[:preview_length] + ("..." if len(full_text) > preview_length else "")
        apply_text(display_text)

        if len(full_text) > preview_length:
            toggle_btn = ctk.CTkLabel(
                container,
                text="see more...",
                text_color="#4DA6FF",
                font=("Arial", 11),
                cursor="hand2"
            )
            toggle_btn.pack(anchor="w", padx=0, pady=(0, 2))
            toggle_btn.bind("<Button-1>", lambda e: toggle())

class MemberEditPostPage(ctk.CTkFrame):
    def __init__(self, master, user_data, edit_data, back_callback):
        super().__init__(master, fg_color=("white", "#0E0E0E"))

        self.db = Database()
        self.user = user_data
        self.edit_data = edit_data
        self.back_callback = back_callback

        container = ctk.CTkFrame(
            self,
            fg_color=("#FFFFFF", "#1A1A1A"),
            corner_radius=15
        )
        container.pack(fill="both", expand=True, padx=80, pady=30)

        back_btn = ctk.CTkButton(
            container,
            text="← Back",
            width=80,
            fg_color=("#DBDBDB", "#333333"),
            text_color=("black", "white"),
            hover_color=("#CFCFCF", "#444444"),
            corner_radius=8,
            command=self.back_callback
        )
        back_btn.pack(anchor="w", padx=30, pady=(20, 10))

        self.title_ent = ctk.CTkEntry(
            container,
            placeholder_text="Add a subject",
            height=45,
            corner_radius=10,
            fg_color="#DADADA",
            text_color="#000000",
            border_width=0,
            font=("Arial", 14)
        )
        self.title_ent.pack(fill="x", padx=30, pady=10)
        self.title_ent.insert(0, edit_data["title"])

        self.msg_ent = ctk.CTkTextbox(
            container,
            height=300,
            corner_radius=10,
            fg_color="#DADADA",
            text_color="#000000",
            border_width=0,
            font=("Arial", 14)
        )
        self.msg_ent.pack(fill="both", expand=True, padx=30, pady=10)
        self.msg_ent.insert("1.0", edit_data["message"])

        update_btn = ctk.CTkButton(
            container,
            text="Update Now",
            width=100,
            height=35,
            corner_radius=10,
            fg_color="#F1C40F",
            hover_color="#D4AC0D",
            text_color="black",
            command=self.update_post
        )
        update_btn.pack(pady=20)

    def update_post(self):
        title = self.title_ent.get().strip()
        message = self.msg_ent.get("1.0", "end-1c").strip()

        if not title or not message:
            messagebox.showwarning("Error", "Fill all fields")
            return

        try:
            self.db.cursor.execute(
                """
                UPDATE announcements
                SET title=%s, message=%s
                WHERE id=%s AND user_id=%s
                """,
                (title, message, self.edit_data["id"], self.user["id"])
            )
            self.db.conn.commit()

            messagebox.showinfo("Success", "Updated successfully")
            self.back_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))