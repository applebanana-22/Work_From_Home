import customtkinter as ctk
from Admin.admin_activity import EditReplyPage
from database import Database
from tkinter import messagebox
from datetime import datetime, timedelta
import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk
import calendar


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
class LeaderActivity(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")

        self.db = Database()
        self.user = user_data
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.db.cursor.execute("""
                SELECT MAX(created_at) as last_time 
                FROM announcements
            """)

        result = self.db.cursor.fetchone()

        if result['last_time']:
                self.last_check_time = result['last_time']
        else:
                self.last_check_time = datetime.now()

        # ================= HEADER =================
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=80, pady=(10, 5))

        self.current_view = "company"
        self.date_filter_active = False
        self.current_search_keyword = ""

        # ROW 1: tabs + filter + search
        top_row = ctk.CTkFrame(header, fg_color="transparent")
        top_row.pack(fill="x")

        # LEFT TABS
        left_tabs = ctk.CTkFrame(top_row, fg_color="transparent")
        left_tabs.pack(side="left")

        self.company_btn = ctk.CTkButton(
            left_tabs,
            text="📢 Company",
            fg_color="#2E86C1",
            command=lambda: self.switch_view("company")
        )
        self.company_btn.pack(side="left", padx=5)

        self.badge_count = 0
        self.badge_label = ctk.CTkLabel(
            self.company_btn,
            text="0",
            width=18,
            height=18,
            corner_radius=9,
            fg_color="#E74C3C",
            text_color="white",
            font=("Arial", 10, "bold")
        )

        self.team_btn = ctk.CTkButton(
            left_tabs,
            text="👥 Your Announcements",
            fg_color="gray30",
            command=lambda: self.switch_view("team")
        )
        self.team_btn.pack(side="left", padx=5)

        # CREATE BUTTON ROW - under Company tab
        self.create_row = ctk.CTkFrame(header, fg_color="transparent")

        self.create_btn = ctk.CTkButton(
            self.create_row,
            text="+ Create New",
            width=140,
            height=34,
            fg_color="#27AE60",
            hover_color="#1E8449",
            corner_radius=20,
            command=self.go_to_create_page
        )

        # Company tab အောက်တည့်တည့်
        self.create_btn.pack(anchor="w", padx=5)

        # initially hide
        self.create_row.pack_forget()
        # ================= SEARCH =================
        self.search_var = ctk.StringVar()

        search_container = ctk.CTkFrame(
            top_row,
            width=260,
            height=42,
            corner_radius=14,
            fg_color=("#F3F2F1", "#2A2A2A"),
            border_width=1,
            border_color="#555555"
        )

        search_container.pack(side="right", padx=(10, 0))
        search_container.pack_propagate(False)

        search_icon = ctk.CTkLabel(
            search_container,
            text="⌕",
            font=("Segoe UI Symbol", 18),
            text_color="#777777"
        )
        search_icon.pack(side="left", padx=(18, 10))

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

        self.search_entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 18),
            pady=6
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda e: self.search_announcements()
        )

        # ================= FILTER ROW =================
        filter_row = ctk.CTkFrame(top_row, fg_color="transparent")
        filter_row.pack(side="right", padx=(10, 0))

        ctk.CTkLabel(
            filter_row,
            text="From:",
            font=("Arial", 12),
            text_color=("black", "white")
        ).pack(side="left", padx=(0, 5))

        self.from_date_entry = DatePickerButton(
            filter_row,
            initial_date=datetime.today().date()
        )
        self.from_date_entry.pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            filter_row,
            text="To:",
            font=("Arial", 12),
            text_color=("black", "white")
        ).pack(side="left", padx=(0, 5))

        self.to_date_entry = DatePickerButton(
            filter_row,
            initial_date=datetime.today().date()
        )
        self.to_date_entry.pack(side="left", padx=(0, 12))

        def modern_btn(parent, text, color, hover, cmd):

            return ctk.CTkButton(
                parent,
                text=text,
                width=80,
                height=36,
                corner_radius=9,
                font=("Arial", 12, "bold"),
                fg_color=color,
                hover_color=hover,
                text_color="white",
                command=cmd
            )

        filter_btn = modern_btn(
            filter_row,
            "🔍 Filter",
            "#2471A3",
            "#1A5276",
            self.apply_date_filter
        )
        filter_btn.pack(side="left", padx=4)

        clear_btn = modern_btn(
            filter_row,
            "✖ Clear",
            "#566573",
            "#424949",
            self.clear_date_filter
        )
        clear_btn.pack(side="left", padx=4)

        # ================= SCROLL AREA =================
        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color=("#D1D1D1", "#444444"),
            corner_radius=12
        )
        self.container.pack(fill="both", expand=True, padx=80, pady=10)

        self.refresh_ui()
        self.after(2000, self.check_new_posts)
        
    def check_new_posts(self):
        try:
            self.db = Database()

            self.db.cursor.execute("""
                SELECT COUNT(*) as total FROM announcements
                WHERE sender_role='admin'
                AND created_at > %s
            """, (self.last_check_time,))

            result = self.db.cursor.fetchone()
            count = result['total']

            if count > 0:
                self.badge_count += count
                self.badge_label.configure(text=str(self.badge_count))

                self.badge_label.place(
                    in_=self.company_btn,
                    relx=1, x=-10,
                    rely=0, y=5
                )

                # ✅ update using DB time (IMPORTANT)
                self.db.cursor.execute("""
                    SELECT MAX(created_at) as last_time FROM announcements
                """)
                self.last_check_time = self.db.cursor.fetchone()['last_time']

        except Exception as e:
            print("Notify error:", e)

        self.after(5000, self.check_new_posts)
            
    def open_create_form(self):
        messagebox.showinfo("Create", "Open Create Page Here")
        
    def switch_view(self, view):
        self.current_view = view

        if view == "team":
            self.badge_count = 0
            self.badge_label.place_forget()

        if view == "company":
            self.company_btn.configure(fg_color="#2E86C1")
            self.team_btn.configure(fg_color="gray30")
            self.create_row.pack_forget()

        else:
            self.company_btn.configure(fg_color="gray30")
            self.team_btn.configure(fg_color="#2E86C1")

            self.create_row.pack(fill="x", pady=(6, 0))
            self.create_btn.pack(anchor="w", padx=5)

        self.refresh_ui()
            
    def apply_date_filter(self):
            self.date_filter_active = True

            from_date = str(self.from_date_entry.get_date())
            to_date = str(self.to_date_entry.get_date())

            if not from_date and not to_date:
                self.date_filter_active = False
                self.refresh_ui(
                search_keyword=self.current_search_keyword
            )
                return

            self.refresh_ui()


    def clear_date_filter(self):

        self.date_filter_active = False

        today = datetime.today().date()

        self.from_date_entry.set_date(today)
        self.to_date_entry.set_date(today)

        self.current_search_keyword = ""
        self.search_var.set("")

        self.refresh_ui()
    def search_announcements(self):

            keyword = self.search_var.get().strip()

            self.current_search_keyword = keyword

            self.refresh_ui()


    # ================= ADD REPLY =================
    def add_reply(self, announcement_id, textbox):
        try:
            reply_text = textbox.get("1.0", "end-1c").strip()

            if not reply_text or reply_text == "Write a reply...":
                return

            # Save reply to database
            self.db.insert_reply(announcement_id, self.user, reply_text)

            # Clear textbox after sending
            textbox.delete("1.0", "end")
            textbox.insert("1.0", "Write a reply...")
            textbox.configure(text_color="#888888")
            textbox.configure(height=35)

            # Refresh UI
            self.refresh_ui()

        except Exception as e:
            messagebox.showerror("Error", str(e))
    def send_with_ctrl_enter(self, event, announcement_id, textbox):
        self.add_reply(announcement_id, textbox)
        return "break"  # Prevents a new line after sending
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
    
    def show_announcement_menu(self, button, row):
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
            command=lambda r=row: self.edit_announcement(r)
        ).pack(fill="x", padx=6, pady=(6, 0))

        ctk.CTkButton(
            menu_frame,
            text="✖ Delete",
            height=38,
            fg_color="transparent",
            hover_color=("#FFE5E5", "#4A2A2A"),
            text_color=("black", "white"),
            anchor="w",
            command=lambda i=row["id"]: self.delete_announcement_from_menu(i)
        ).pack(fill="x", padx=6, pady=(0, 6))
    def edit_announcement(self, row):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        self.go_to_create_page(row)


    def delete_announcement_from_menu(self, announcement_id):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        self.handle_delete(announcement_id)
    def edit_reply(self, reply):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        self.pack_forget()

        self.master.edit_reply_page = EditReplyPage(
            self.master,
            self.user,
            reply,
            back_callback=self.back_from_reply_edit
        )
        self.master.edit_reply_page.pack(fill="both", expand=True) 
    def back_from_reply_edit(self):
        self.master.edit_reply_page.destroy()
        self.pack(fill="both", expand=True)
        self.refresh_ui()      
    def delete_reply(self, reply):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        if messagebox.askyesno("Confirm Delete", "Delete this reply?"):
            try:
                self.db.cursor.execute(
                    "DELETE FROM announcement_replies WHERE id=%s AND user_id=%s",
                    (reply["id"], self.user["id"])
                )
                self.db.conn.commit()
                self.refresh_ui()

            except Exception as e:
                messagebox.showerror("Error", str(e))
    # ================= UI =================
    def refresh_ui(self):
        for w in self.container.winfo_children():
            w.destroy()

        try:
            self.db = Database()
            self.db.conn.commit()

            if self.current_view == "company":
                query = """
                    SELECT * FROM announcements
                    WHERE sender_role='admin'
                """
                params = []
            else:
                query = """
                    SELECT * FROM announcements
                    WHERE sender_role='leader'
                    AND created_by=%s
                """
                params = [self.user["full_name"]]

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
                msg = "No announcements found."

                if self.date_filter_active:
                    msg = "No announcements found for selected date."

                if self.current_search_keyword:
                    msg = "No announcements found for your search."

                ctk.CTkLabel(
                    self.container,
                    text=msg,
                    text_color=("black", "white"),
                    font=("Arial", 13)
                ).pack(pady=30)
                return

            for row in rows:
                
        # ================= CARD =================
                card = ctk.CTkFrame(
                        self.container,
                        corner_radius=12,
                        fg_color=("#FFFFFF", "#1E1E1E"),
                        border_width=1,
                        border_color="#2A2A2A"
                    )
                card.pack(fill="x", pady=12, padx=15)

                main = ctk.CTkFrame(card, fg_color="transparent")
                main.pack(fill="x", padx=12, pady=12)

                # ================= AVATAR =================
                name = row.get("created_by", "User")
                initials = "".join([n[0] for n in name.split()[:2]]).upper()

                avatar = ctk.CTkFrame(main, width=40, height=40,
                                      corner_radius=20, fg_color="#2E86C1")
                avatar.pack(side="left", padx=(0, 10), anchor="n")
                avatar.pack_propagate(False)

                ctk.CTkLabel(avatar, text=initials,
                             font=("Arial", 14, "bold"),
                             text_color=("black", "white")).pack(expand=True)

                # ================= RIGHT SIDE =================
                right = ctk.CTkFrame(main, fg_color="transparent")
                right.pack(side="left", fill="both", expand=True, padx=(0, 5))

                top = ctk.CTkFrame(right, fg_color="transparent")
                top.pack(fill="x")

                content_frame = ctk.CTkFrame(right, fg_color="transparent")
                CONTENT_PADX = 20
                content_frame.pack(fill="x", padx=0)

                # ✅ FIX: define FIRST
                time_str = row['created_at'].strftime("%Y-%m-%d | %I:%M %p")

                # LEFT SIDE
                ctk.CTkLabel(
                    top,
                    text=name,
                    font=("Arial", 13, "bold"),
                    text_color=("black", "white")
                ).pack(side="left")

                ctk.CTkLabel(
                    top,
                    text=time_str,
                    font=("Arial", 10),
                    text_color="#888"
                ).pack(side="left", padx=10)


                # ================= RIGHT SIDE BUTTONS (YOUR CODE STYLE) =================
                if self.current_view == "team":
                    ann_menu_btn = ctk.CTkButton(
                        top,
                        text="⋯",
                        width=30,
                        height=24,
                        fg_color="transparent",
                        hover_color=("#E5E5E5", "#333333"),
                        text_color=("black", "white"),
                        font=("Arial", 16, "bold")
                    )
                    ann_menu_btn.pack(side="right")

                    ann_menu_btn.configure(
                        command=lambda b=ann_menu_btn, r=row: self.show_announcement_menu(b, r)
                    )
                               # TITLE
                is_dark = ctk.get_appearance_mode() == "Dark"

                title_text = tk.Text(
                    content_frame,
                    height=1,
                    wrap="none",
                    bg="#1E1E1E" if is_dark else "#FFFFFF",
                    fg="white" if is_dark else "black",
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0,
                    font=("Arial", 15, "bold")
                )

                # title_text.pack(anchor="w", padx=CONTENT_PADX, pady=(5, 2), fill="x")

                title = row['title']

                title_text.insert("1.0", title)

                if self.current_search_keyword:

                    lower_title = title.lower()
                    lower_keyword = self.current_search_keyword.lower()

                    start_index = lower_title.find(lower_keyword)

                    while start_index != -1:

                        end_index = start_index + len(self.current_search_keyword)

                        start = f"1.{start_index}"
                        end = f"1.{end_index}"

                        title_text.tag_add("highlight", start, end)

                        start_index = lower_title.find(
                            lower_keyword,
                            end_index
                        )

                    title_text.tag_config(
                        "highlight",
                        background="#FFD54F",
                        foreground="black"
                    )

                title_text.configure(state="disabled")
                self.create_expandable_message(
                    content_frame  ,
                    row['message'],
                    padx=CONTENT_PADX,
                    keyword=self.current_search_keyword
                )

                # ================= REPLY INPUT =================
                # ================= ACTION AREA =================
                # ================= SHOW REPLIES =================
                self.db.cursor.execute(
                    "SELECT * FROM announcement_replies WHERE announcement_id=%s ORDER BY created_at ASC",
                    (row['id'],)
                )

                replies = self.db.cursor.fetchall()

                MAX_VISIBLE_REPLIES = 2

                if replies:
                    replies_container = ctk.CTkFrame(content_frame, fg_color="transparent")
                    replies_container.pack(fill="x", padx=CONTENT_PADX, pady=(5, 0))
                    def render_replies(show_all=False, replies_list=replies, container=replies_container):
                        for w in container.winfo_children():
                            w.destroy()
                        visible = replies_list if show_all else replies_list[:MAX_VISIBLE_REPLIES]

                        for reply in visible:
                            reply_box = ctk.CTkFrame(
                                container,
                                fg_color=("#F5F5F5", "#2A2A2A"),
                                corner_radius=8
                            )
                            reply_box.pack(fill="x", padx=0, pady=3)

                            r_name = reply.get("created_by", "User")
                            r_msg = reply.get("message", "")
                            if not r_msg.strip():
                                continue
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

                            reply_text = tk.Text(
                                reply_box,
                                wrap="word",
                                height=2,
                                bg="#2A2A2A" if is_dark else "#F5F5F5",
                                fg="white" if is_dark else "black",
                                relief="flat",
                                borderwidth=0,
                                highlightthickness=0,
                                font=("Arial", 12),
                                cursor="arrow",
                                takefocus=0
                            )
                            reply_text.pack(fill="x", anchor="w", padx=8, pady=(0, 5))

                            reply_text.insert("1.0", r_msg)

                            if self.current_search_keyword:
                                lower_reply = r_msg.lower()
                                lower_keyword = self.current_search_keyword.lower()
                                start_index = lower_reply.find(lower_keyword)

                                while start_index != -1:
                                    end_index = start_index + len(self.current_search_keyword)
                                    reply_text.tag_add("highlight", f"1.{start_index}", f"1.{end_index}")
                                    start_index = lower_reply.find(lower_keyword, end_index)

                                reply_text.tag_config(
                                    "highlight",
                                    background="#FFD54F",
                                    foreground="black",
                                    font=("Arial", 12, "bold")
                                )

                            reply_text.configure(state="disabled")

                        if len(replies_list) > MAX_VISIBLE_REPLIES:
                            toggle = ctk.CTkLabel(
                                container,
                                text=f"Show all replies ({len(replies_list)})" if not show_all else "Show less",
                                text_color="#4DA6FF",
                                font=("Arial", 11, "underline"),
                                cursor="hand2"
                            )
                            toggle.pack(anchor="w", padx=0, pady=(2, 5))

                            toggle.bind(
                                "<Button-1>",
                                lambda e, state=show_all, rl=replies_list, c=container:
                                render_replies(not state, rl, c))
                    render_replies(False)
                else:
                    ctk.CTkLabel(
                        content_frame,
                        text="No replies yet.",
                        text_color=("gray40", "#777777"),
                        font=("Arial", 11)
                    ).pack(anchor="w", padx=CONTENT_PADX, pady=(5, 0))

               
                  # ================= REPLY INPUT (FOR BOTH) =================
                reply_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                reply_frame.pack(fill="x", padx=(CONTENT_PADX, CONTENT_PADX), pady=(8, 8))

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
                    command=lambda a_id=row['id'], e=reply_entry: self.add_reply(a_id, e)
                )

                send_btn.grid(row=0,
                    column=1,
                    sticky="se",
                    padx=(0, 0),
                    pady=(0, 0))


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


                def handle_enter(event, a_id=row['id'], box=reply_entry):
                    if event.state & 0x0001:   # Shift + Enter = new line
                        box.insert("insert", "\n")
                        box.after(10, lambda: resize_reply_box(box))
                        return "break"

                    self.add_reply(a_id, box)  # Enter = send
                    return "break"


                reply_entry.bind("<FocusIn>", clear_placeholder)
                reply_entry.bind("<FocusOut>", restore_placeholder)
                reply_entry.bind("<KeyRelease>", on_key_release)
                reply_entry.bind("<Return>", handle_enter)

               
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def handle_delete(self, announcement_id):
        print("DELETE CLICKED")

        confirm = messagebox.askyesno(
            "Confirm",
            "Are you sure to delete?"
        )

        if not confirm:
            return

        try:
            self.db.cursor.execute(
                "DELETE FROM announcements WHERE id=%s AND created_by=%s",
                (announcement_id, self.user['full_name'])
            )
            self.db.conn.commit()

            messagebox.showinfo("Deleted", "Deleted successfully")  # optional

            self.refresh_ui()

        except Exception as e:
            # self.conn.rollback()
            print("ERROR:", e)
            messagebox.showerror("Error", str(e))
    
    def create_expandable_message(self, parent, full_text, padx=20, keyword=""):
        is_dark = ctk.get_appearance_mode() == "Dark"
        preview_length = 80

        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=padx, pady=(6, 8))

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

        return container
    def go_to_create_page(self, row=None):
        self.pack_forget()

        self.master.create_page = CreateTeamPostPage(
            self.master,
            self.user,
            back_callback=self.back_to_main,
            edit_data=row   # 👈 PASS DATA
        )
        self.master.create_page.pack(fill="both", expand=True)
        
    def back_to_main(self):
        self.master.create_page.destroy()
        self.pack(fill="both", expand=True)
        self.switch_view("team")

class EditReplyPage(ctk.CTkFrame):
    def __init__(self, master, user_data, reply_data, back_callback):
        super().__init__(master, fg_color=("white", "#0E0E0E"))

        self.db = Database()
        self.user = user_data
        self.reply_data = reply_data
        self.back_callback = back_callback

        form_frame = ctk.CTkFrame(
            self,
            fg_color=("#FFFFFF", "#1A1A1A"),
            corner_radius=15
        )
        form_frame.pack(pady=30, padx=100, fill="both", expand=True)

        back_btn = ctk.CTkButton(
            form_frame,
            text="← Back",
            width=80,
            fg_color=("#DBDBDB", "#333333"),
            text_color=("black", "white"),
            hover_color=("#CFCFCF", "#444444"),
            corner_radius=8,
            command=self.back_callback
        )
        back_btn.pack(anchor="w", padx=30, pady=(20, 10))

        self.reply_box = ctk.CTkTextbox(
            form_frame,
            height=300,
            corner_radius=10,
            fg_color=("#EEEEEE", "#2A2A2A"),
            text_color=("black", "white"),
            border_width=0,
            font=("Arial", 14)
        )
        self.reply_box.pack(fill="both", expand=True, padx=30, pady=10)

        self.reply_box.insert("1.0", self.reply_data.get("message", ""))

        update_btn = ctk.CTkButton(
            form_frame,
            text="Update Reply",
            width=120,
            height=35,
            corner_radius=10,
            fg_color="#D68910",
            hover_color="#B9770E",
            command=self.save_reply
        )
        update_btn.pack(pady=20)

    def save_reply(self):
        new_msg = self.reply_box.get("1.0", "end-1c").strip()

        if not new_msg:
            messagebox.showwarning("Warning", "Reply cannot be empty")
            return

        try:
            self.db.cursor.execute(
                """
                UPDATE announcement_replies
                SET message=%s
                WHERE id=%s AND user_id=%s
                """,
                (new_msg, self.reply_data["id"], self.user["id"])
            )
            self.db.conn.commit()
            messagebox.showinfo("Success", "Reply updated successfully")
            self.back_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))      
class CreateTeamPostPage(ctk.CTkFrame):
    def __init__(self, master, user_data, back_callback ,edit_data=None):
        super().__init__(master, fg_color=("white", "#0E0E0E"))

        self.db = Database()
        self.user = user_data
        self.back_callback = back_callback
        self.edit_data = edit_data

        # ================= CENTERED FORM =================
        form_frame = ctk.CTkFrame(
            self,
            fg_color=("#FFFFFF", "#1A1A1A"),
            corner_radius=15
        )
        form_frame.pack(pady=30, padx=100, fill="both", expand=True)

        # ================= BACK BUTTON =================
        back_btn = ctk.CTkButton(
            form_frame,
            text="← Back",
            width=80,
            fg_color=("#DBDBDB", "#333333"),
            text_color=("black", "white"),
            hover_color=("#CFCFCF", "#444444"),
            corner_radius=8,
            command=self.back_callback
        )
        back_btn.pack(anchor="w", padx=30, pady=(20, 10))

        # ================= TITLE ENTRY =================
        self.title_ent = ctk.CTkEntry(
            form_frame,
            placeholder_text="Add a subject",
            height=45,
            corner_radius=10,
            fg_color=("#EEEEEE", "#2A2A2A"),
            text_color=("black", "white"),
            border_width=0,
            font=("Arial", 14)
        )
        self.title_ent.pack(fill="x", padx=30, pady=10)

        # ================= MESSAGE TEXTBOX =================
        self.msg_ent = ctk.CTkTextbox(
            form_frame,
            height=300,
            corner_radius=10,
            fg_color=("#EEEEEE", "#2A2A2A"),
            text_color=("black", "white"),
            border_width=0,
            font=("Arial", 14)
        )
        self.msg_ent.pack(fill="both", expand=True, padx=30, pady=10)
        if self.edit_data:
            self.title_ent.insert(0, self.edit_data['title'])
            self.msg_ent.insert("1.0", self.edit_data['message'])

        # ================= POST BUTTON =================
        post_btn = ctk.CTkButton(
            form_frame,
            text="Update Now" if self.edit_data else "Post",
            width=60,
            height=35,
            corner_radius=10,
            fg_color="#D68910",
            hover_color="#B9770E",
            command=self.save
        )
        post_btn.pack(pady=20)

    def save(self):
        title = self.title_ent.get().strip()
        message = self.msg_ent.get("1.0", "end-1c").strip()

        if not title or not message:
            messagebox.showwarning("Warning", "Please fill all fields.")
            return

        try:
            if self.edit_data:
                self.db.cursor.execute(
                    "UPDATE announcements SET title=%s, message=%s WHERE id=%s AND created_by=%s",
                    (title, message, self.edit_data['id'], self.user['full_name'])
                )
            else:
                # 1. Insert the announcement (Existing code)
                self.db.cursor.execute(
                    "INSERT INTO announcements (title, message, sender_role, created_by, created_at) VALUES (%s, %s, %s, %s, NOW())",
                    (title, message, "leader", self.user['full_name'])
                )

                # 2. ADD THIS: Create notifications for all Members
                # We use the keyword 'announcement' so the badge logic can find it
                notif_msg = f"New Team Announcement: {title}"
                self.db.cursor.execute(
                    """
                    INSERT INTO notifications (user_id, message, is_read, created_at)
                    SELECT id, %s, 0, NOW() FROM users WHERE role = 'member'
                    """, 
                    (notif_msg,)
                )

            self.db.conn.commit()
            messagebox.showinfo("Success", "Saved successfully")
            self.back_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))