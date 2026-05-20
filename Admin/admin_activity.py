import customtkinter as ctk
from database import Database
from tkinter import messagebox
from datetime import datetime
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
     
class AdminAnnouncements(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user_data
        self.edit_id = None
        self.form_visible = False
        self.placeholder = "Type a message..."
        self.date_filter_active = False
        self.current_search_keyword = ""

        # --- 1. HEADER ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=80, pady=(10, 0))
 
        self.toggle_btn = ctk.CTkButton(self.header_frame, text="+ Create New", width=60, height=35,
                                        corner_radius=20, font=("Arial", 13, "bold"),
                                        fg_color="#10B981",hover_color="#1E8449", command=self.go_to_form_page)
        self.toggle_btn.pack(side="left")
        # ================= SEARCH BOX =================
        self.search_var = ctk.StringVar()

        # ================= SEARCH BOX =================
        self.search_var = ctk.StringVar()

        search_container = ctk.CTkFrame(
                self.header_frame,
                width=260,
                height=42,
                corner_radius=14,
                fg_color=("#F3F2F1", "#2A2A2A"),
                border_width=1,
                border_color="#555555"
            )

        search_container.pack(
                side="right",
                padx=(10, 0),
                pady=(0, 2)
            )
        search_container.pack_propagate(False)

        # search icon
        search_icon = ctk.CTkLabel(
            search_container,
            text="⌕",
            font=("Segoe UI Symbol", 18),
            text_color="#777777"
        )
        search_icon.pack(side="left", padx=(18, 10))

        # entry
        self.search_entry = ctk.CTkEntry(
            search_container,
            textvariable=self.search_var,
            placeholder_text="Look for announcements, replies and more",
            placeholder_text_color="#888888",

            fg_color="transparent",
            bg_color="transparent",

            border_width=0,
            text_color=("black", "white"),

            font=("Arial", 13),
            width=260
        )
        self.search_entry.pack_propagate(False)
        self.search_entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 18),
            pady=6
        )

        # live search
        self.search_entry.bind(
            "<KeyRelease>",
            lambda e: self.search_announcements()
        )

        # live search
        self.search_entry.bind(
            "<KeyRelease>",
            lambda e: self.search_announcements()
        )
                
        # --- DATE FILTER ROW ON TOP RIGHT ---
        filter_row = ctk.CTkFrame(self.header_frame, fg_color="transparent")
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

        self.from_date_entry.pack(
            side="left",
            padx=(0, 12)
        )

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

                text_color=("white"),

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
        # --- TITLE ---
        ctk.CTkLabel(
            self,
            text="Admin Post History",
            font=("Arial", 18, "bold"),
            text_color=("black", "white")
        ).pack(anchor="w", padx=80, pady=(10, 0))

        
        # --- 2. DROP-DOWN FORM ---
        self.form_frame = ctk.CTkFrame(self, corner_radius=10, border_width=1, border_color="gray30")
 
        self.title_ent = ctk.CTkEntry(self.form_frame, placeholder_text="Add a subject (Title)", height=40)
        self.title_ent.pack(fill="x", padx=15, pady=(15, 5))
 
        self.msg_ent = ctk.CTkTextbox(self.form_frame, height=120, border_width=1, text_color="gray")
        self.msg_ent.pack(fill="x", padx=15, pady=5)
        self.msg_ent.insert("0.0", self.placeholder)
       
        self.msg_ent.bind("<FocusIn>", self.clear_placeholder)
        self.msg_ent.bind("<FocusOut>", self.restore_placeholder)
 
        self.btn_row = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.btn_row.pack(fill="x", padx=15, pady=(5, 15))
 
        self.post_btn = ctk.CTkButton(self.btn_row, text="Post", width=100,
                                       fg_color="#D68910",  command=self.handle_save)
        self.post_btn.pack(side="right")
 

        # --- LIST ---
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=80, pady=10)
 
        self.list_frame.configure(
            fg_color=("#D1D1D1", "#444444"),
            corner_radius=12,
            border_width=1,
            border_color="#2A2A2A"
        )
               
        self.refresh_list()
 
    def clear_placeholder(self, event):
        current_text = self.msg_ent.get("0.0", "end-1c")
        if current_text == self.placeholder:
            self.msg_ent.delete("0.0", "end")
            self.msg_ent.configure(text_color=("black", "white"))
 
    def restore_placeholder(self, event):
        current_text = self.msg_ent.get("0.0", "end-1c").strip()
        if not current_text:
            self.msg_ent.insert("0.0", self.placeholder)
            self.msg_ent.configure(text_color="gray")
    
    def handle_save(self):
        t = self.title_ent.get()
        m = self.msg_ent.get("0.0", "end-1c").strip()
       
        if not t or not m or m == self.placeholder:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
 
        if messagebox.askyesno("Confirm", "Post this announcement?"):
            
            try:
                if self.edit_id:
                    self.db.cursor.execute(
                        "UPDATE announcements SET title=%s, message=%s WHERE id=%s AND user_id=%s",
                        (t, m, self.edit_id, self.user["id"])
                    )
                else:
                    self.db.cursor.execute(
                        "INSERT INTO announcements (title, message, sender_role, created_by, user_id) VALUES (%s, %s, 'admin', %s, %s)",
                        (t, m, self.user["full_name"], self.user["id"])
                    )
                self.db.conn.commit()
                # self.reset_form()
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Database Error", f"Check your table columns: {e}")
 
    def refresh_list(self, from_date="", to_date="", search_keyword=""):
        for widget in self.list_frame.winfo_children(): widget.destroy()
        try:
            query = """
                SELECT id, title, message, created_at, created_by, user_id
                FROM announcements
                WHERE sender_role = 'admin'
            """

            params = []

            if from_date:
                query += " AND DATE(created_at) >= %s"
                params.append(from_date)

            if to_date:
                query += " AND DATE(created_at) <= %s"
                params.append(to_date)


            if search_keyword:

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

                keyword_param = f"%{search_keyword}%"

                params.extend([
                    keyword_param,
                    keyword_param,
                    keyword_param
                ])
            query += " ORDER BY created_at DESC"

            self.db.cursor.execute(query, tuple(params))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(
                    self.list_frame,
                    text="No announcements found for selected date.",
                    font=("Arial", 13),
                    text_color=("black", "white")
                ).pack(pady=30)
                return

            for row in rows:
                
                item = ctk.CTkFrame(
                        self.list_frame,
                        corner_radius=10,
                        fg_color= ("white", "#1E1E1E"),# ✅ dark card
                        border_width=1,
                        border_color="#2A2A2A"
                    )
                item.pack(fill="x", pady=5, padx=10)
               
                text_container = ctk.CTkFrame(item, fg_color="transparent")
                text_container.pack(side="left", fill="both", expand=True, padx=10, pady=8)
                CONTENT_PADX = 20
               
                header_f = ctk.CTkFrame(text_container, fg_color="transparent")
                header_f.pack(fill="x")
               
                title_text = row['title']

                is_dark = ctk.get_appearance_mode() == "Dark"

                title_label = tk.Text(
                    header_f,
                    height=1,
                    wrap="none",
                    bg="#1E1E1E" if is_dark else "#FFFFFF",
                    fg="white" if is_dark else "black",
                    insertbackground="white" if is_dark else "black",
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0,
                    font=("Arial", 14, "bold"),
                    cursor="arrow",
                    takefocus=0,
                    selectbackground="#1E1E1E" if is_dark else "#FFFFFF",
                    selectforeground="white" if is_dark else "black",
                )

                title_label.pack(
                    side="left",
                    anchor="w"
                )

                

                title_label.insert("1.0", title_text)
                title_label.configure(
                    width=len(title_text) + 2
                )

                if search_keyword:

                    lower_title = title_text.lower()
                    lower_keyword = search_keyword.lower()

                    start_index = lower_title.find(lower_keyword)

                    while start_index != -1:

                        end_index = start_index + len(search_keyword)

                        start = f"1.{start_index}"
                        end = f"1.{end_index}"

                        title_label.tag_add("highlight", start, end)

                        start_index = lower_title.find(
                            lower_keyword,
                            end_index
                        )

                    title_label.tag_config(
                        "highlight",
                        background="#FFD54F",
                        foreground="black",
                        font=("Arial", 14, "bold")
                    )

                title_label.configure(state="disabled")
               
                # Format time logic
                post_time = row['created_at'].strftime("%Y-%m-%d | %I:%M %p") if isinstance(row['created_at'], datetime) else str(row['created_at'])
                ctk.CTkLabel(header_f, text=post_time, font=("Arial", 10), text_color=("black", "white")).pack(side="left", padx=15)
                
                # only owner can edit/delete post
                if str(row.get("user_id")) == str(self.user.get("id")):
                    menu_btn = ctk.CTkButton(
                        header_f,
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
                        command=lambda b=menu_btn, r=row: self.show_post_menu(b, r)
                    )
                self.create_expandable_message(
                    text_container,
                    row['message'],
                    padx=CONTENT_PADX,
                    keyword=search_keyword
                )
                # ================= SHOW REPLIES =================
                self.db.cursor.execute(
                    "SELECT * FROM announcement_replies "
                    "WHERE announcement_id=%s ORDER BY created_at ASC",
                    (row['id'],)
                )
                replies = self.db.cursor.fetchall()

                MAX_VISIBLE_REPLIES = 2

                # Only create replies container if replies exist
                if replies:
                    replies_container = ctk.CTkFrame(
                        text_container,
                        fg_color="transparent"
                    )
                    replies_container.pack(fill="x", padx=CONTENT_PADX, pady=(5, 0))

                    def render_replies(show_all=False, replies_list=replies, container=replies_container):
                        # Clear previous replies
                        for widget in container.winfo_children():
                            widget.destroy()

                        visible_replies = replies_list if show_all else replies_list[:MAX_VISIBLE_REPLIES]

                        # Display replies
                        for reply in visible_replies:
                            reply_box = ctk.CTkFrame(
                                container,
                                fg_color=("#F5F5F5", "#2A2A2A"),
                                corner_radius=8
                            )
                            reply_box.pack(fill="x", padx=0, pady=3)

                            r_name = reply.get("created_by", "User")
                            r_msg = reply.get("message", "")
                            r_time = reply["created_at"].strftime("%Y-%m-%d | %I:%M %p")

                            # reply header row
                            reply_top = ctk.CTkFrame(reply_box, fg_color="transparent")
                            reply_top.pack(fill="x", padx=8, pady=(3, 0))

                            ctk.CTkLabel(
                                reply_top,
                                text=f"{r_name} ({r_time})",
                                font=("Arial", 11, "bold"),
                                text_color=("black", "#DDDDDD")
                            ).pack(side="left")

                            # only owner can edit/delete reply
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
                                            insertbackground="white" if is_dark else "black",
                                            relief="flat",
                                            borderwidth=0,
                                            highlightthickness=0,
                                            font=("Arial", 12),
                                            cursor="arrow",
                                            takefocus=0,
                                            selectbackground="#1E1E1E" if is_dark else "#FFFFFF",
                                            selectforeground="white" if is_dark else "black",
                                        )

                            reply_text.pack(
                                    fill="x",
                                    anchor="w",
                                    padx=8,
                                    pady=(0, 5)
                                )

                            reply_text.insert("1.0", r_msg)

                        if search_keyword:

                                lower_reply = r_msg.lower()
                                lower_keyword = search_keyword.lower()

                                start_index = lower_reply.find(lower_keyword)

                                while start_index != -1:

                                    end_index = start_index + len(search_keyword)

                                    start = f"1.{start_index}"
                                    end = f"1.{end_index}"

                                    reply_text.tag_add("highlight", start, end)

                                    start_index = lower_reply.find(
                                        lower_keyword,
                                        end_index
                                    )

                        reply_text.tag_config(
                                    "highlight",
                                    background="#FFD54F",
                                    foreground="black",
                                    font=("Arial", 12, "bold")
                                )

                        reply_text.configure(state="disabled")

                                                    # Toggle button
                        if len(replies_list) > MAX_VISIBLE_REPLIES:
                            toggle_text = (
                                f"Show all replies ({len(replies_list)})"
                                if not show_all else "Show less"
                                
                            )

                            toggle_label = ctk.CTkLabel(
                                container,
                                text=toggle_text,
                                text_color="#4DA6FF",
                                font=("Arial", 11, "underline"),
                                cursor="hand2"
                            )
                            toggle_label.pack(anchor="w", padx=0, pady=(2, 5))

                            toggle_label.bind(
                                "<Button-1>",
                                lambda e, state=show_all, rl=replies_list, c=container:
                                    render_replies(not state, rl, c)
                            )
                    render_replies(False)
                    
                if not replies:
                    ctk.CTkLabel(
                        text_container,
                        text="No replies yet.",
                        font=("Arial", 11),
                        text_color="#777777"
                    ).pack(anchor="w", padx=CONTENT_PADX, pady=(5, 0))

             # ================= REPLY INPUT =================
                reply_frame = ctk.CTkFrame(text_container, fg_color="transparent")
                reply_frame.pack(fill="x", padx=(CONTENT_PADX, CONTENT_PADX), pady=(8, 8))

                reply_frame.grid_columnconfigure(0, weight=1)
                reply_frame.grid_columnconfigure(1, weight=0)
                reply_frame.grid_rowconfigure(0, weight=1)

                placeholder_text = "Write a reply..."

                reply_entry = ctk.CTkTextbox(
                    reply_frame,
                    height=35,
                    corner_radius=8,
                    fg_color=("#EEEEEE", "#2A2A2A"),
                    text_color="#888888",
                    wrap="word",
                    font=("Arial", 13),
                    border_width=0
                )

                reply_entry.grid(
                    row=0,
                    column=0,
                    sticky="ew",
                    padx=(0, 10),
                    pady=0
                )

                reply_entry.insert("1.0", placeholder_text)
                announcement_id = row["id"]

                send_btn = ctk.CTkButton(
                    reply_frame,
                    text="➤",
                    width=45,
                    height=35,
                    corner_radius=8,
                    fg_color="#0A93F5",
                    hover_color="#087ACC",
                    border_width=0,
                    font=("Arial", 18),
                    command=lambda a_id=announcement_id, e=reply_entry: self.add_reply(a_id, e)
                )

                send_btn.grid(
                    row=0,
                    column=1,
                    sticky="se",
                    padx=(0, 0),
                    pady=(0, 0)
                )


                def resize_reply_box(box=reply_entry, frame=reply_frame, btn=send_btn):
                    text = box.get("1.0", "end-1c")

                    if text == placeholder_text or not text.strip():
                        new_height = 35
                    else:
                        lines = int(box.index("end-1c").split(".")[0])
                        new_height = 35 + ((lines - 1) * 22)

                        if new_height > 220:
                            new_height = 220

                    box.configure(height=new_height)

                    # keep send button full size and bottom-right
                    btn.configure(width=45, height=35)
                    btn.grid_configure(sticky="se", pady=(new_height - 35, 0))

                    frame.update_idletasks()


                def clear_reply_placeholder(event, box=reply_entry):
                    if box.get("1.0", "end-1c") == placeholder_text:
                        box.delete("1.0", "end")
                        box.configure(text_color=("black", "white"))
                        resize_reply_box(box)


                def restore_reply_placeholder(event, box=reply_entry):
                    if not box.get("1.0", "end-1c").strip():
                        box.delete("1.0", "end")
                        box.insert("1.0", placeholder_text)
                        box.configure(text_color="#888888")
                        resize_reply_box(box)


                def handle_reply_enter(event, a_id=announcement_id, box=reply_entry):
                    # Shift + Enter = new line
                    if event.state & 0x0001:
                        box.insert("insert", "\n")
                        box.after(10, lambda: resize_reply_box(box))
                        return "break"

                    # Enter only = send
                    self.add_reply(a_id, box)
                    return "break"


                def on_reply_key_release(event, box=reply_entry):
                    resize_reply_box(box)


                reply_entry.bind("<FocusIn>", clear_reply_placeholder)
                reply_entry.bind("<FocusOut>", restore_reply_placeholder)
                reply_entry.bind("<Return>", handle_reply_enter)
                reply_entry.bind("<KeyRelease>", on_reply_key_release)
        except Exception as e:
                messagebox.showerror("Error", str(e))
                
    def prepare_edit(self, row):
        if not self.form_visible: self.toggle_form()
        self.edit_id = row['id']
        self.title_ent.delete(0, 'end')
        self.title_ent.insert(0, row['title'])
        self.msg_ent.delete("0.0", "end")
        self.msg_ent.insert("0.0", row['message'])
        self.msg_ent.configure(text_color=("black", "white"))
        self.post_btn.configure(text="Update Now", fg_color="#F39C12")
 
    def handle_delete(self, ann_id):
        if messagebox.askyesno("Confirm Delete", "Delete this post?"):
            self.db.cursor.execute("DELETE FROM announcements WHERE id=%s", (ann_id,))
            self.db.conn.commit()

            if self.date_filter_active:
                self.apply_date_filter()
            else:
                self.refresh_list(
                search_keyword=self.current_search_keyword
            )
            
    def apply_date_filter(self):
        self.date_filter_active = True

        from_date = str(self.from_date_entry.get_date())
        to_date = str(self.to_date_entry.get_date())

        if not from_date and not to_date:
            self.date_filter_active = False
            self.refresh_list(
            search_keyword=self.current_search_keyword
        )
            return

        self.refresh_list(from_date, to_date)


    def clear_date_filter(self):
        self.date_filter_active = False
        today = datetime.today().date()
        self.from_date_entry.set_date(today)
        self.to_date_entry.set_date(today)
        self.refresh_list(
        search_keyword=self.current_search_keyword
    )
    def search_announcements(self):

        keyword = self.search_var.get().strip()

        self.current_search_keyword = keyword

        self.refresh_list(search_keyword=keyword)
    
    def show_post_menu(self, button, row):

        # toggle close
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()
            self.active_menu = None
            return

        self.active_menu = ctk.CTkToplevel(self)
        self.active_menu.overrideredirect(True)
        self.active_menu.attributes("-topmost", True)
        self.active_menu.configure(fg_color=("#FFFFFF", "#2B2B2B"))

        menu_width = 150
        menu_height = 95

        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height() + 5

        x = x - menu_width + button.winfo_width()

        self.active_menu.geometry(f"{menu_width}x{menu_height}+{x}+{y}")

        menu_frame = ctk.CTkFrame(
            self.active_menu,
            fg_color=("#FFFFFF", "#2B2B2B"),
            corner_radius=8,
            border_width=1,
            border_color="#555555"
        )
        menu_frame.pack(fill="both", expand=True)

        edit_btn = ctk.CTkButton(
            menu_frame,
            text="🖉  Edit",
            height=38,
            fg_color="transparent",
            hover_color=("#EEEEEE", "#3A3A3A"),
            text_color=("black", "white"),
            anchor="w",
            font=("Segoe UI", 13),
            command=lambda r=row: self.menu_edit(r)
        )
        edit_btn.pack(fill="x", padx=6, pady=(6, 0))

        delete_btn = ctk.CTkButton(
            menu_frame,
            text="✖ Delete",
            height=38,
            fg_color="transparent",
            hover_color=("#FFE5E5", "#4A2A2A"),
            text_color=("black", "white"),
            anchor="w",
            command=lambda i=row["id"]: self.menu_delete(i)
        )
        delete_btn.pack(fill="x", padx=6, pady=(0, 6))

        self.after(150, self.bind_close_menu)
    def show_reply_menu(self, button, reply):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        self.active_menu = ctk.CTkToplevel(self)
        self.active_menu.overrideredirect(True)
        self.active_menu.attributes("-topmost", True)
        self.active_menu.configure(fg_color=("#FFFFFF", "#2B2B2B"))

        menu_width = 150
        menu_height = 95

        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height() + 5
        x = x - menu_width + button.winfo_width()

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
            font=("Segoe UI", 13),
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

        self.after(150, self.bind_close_menu) 
        
    def edit_reply(self, reply):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        self.winfo_toplevel().unbind("<Button-1>")

        self.pack_forget()

        self.master.edit_reply_page = EditReplyPage(
            self.master,
            self.user,
            reply_data=reply,
            back_callback=self.back_from_reply_edit
        )
        self.master.edit_reply_page.pack(fill="both", expand=True)



    def delete_reply(self, reply):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()
        self.winfo_toplevel().unbind("<Button-1>")

        if messagebox.askyesno("Confirm Delete", "Delete this reply?"):
            
            self.db.cursor.execute(
            "DELETE FROM announcement_replies WHERE id=%s AND user_id=%s",
            (reply["id"], self.user["id"])
            )
            self.db.conn.commit()

            if self.date_filter_active:
                self.apply_date_filter()
            else:
                self.refresh_list(
                search_keyword=self.current_search_keyword
            )
    def menu_edit(self, row):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        self.winfo_toplevel().unbind("<Button-1>")
        self.go_to_form_page(row)


    def menu_delete(self, ann_id):
        if hasattr(self, "active_menu") and self.active_menu.winfo_exists():
            self.active_menu.destroy()

        self.winfo_toplevel().unbind("<Button-1>")
        self.handle_delete(ann_id)
    def create_expandable_message(self, parent, full_text, padx=20, keyword=""):
        is_dark = ctk.get_appearance_mode() == "Dark"
        preview_length = 80

        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=padx, pady=(6, 8))

        is_expanded = False

        def apply_highlight(text_to_show):

            msg_label.configure(state="normal")

            msg_label.delete("1.0", "end")

            msg_label.insert("1.0", text_to_show)

            msg_label.tag_remove("highlight", "1.0", "end")

            if keyword:

                lower_text = text_to_show.lower()
                lower_keyword = keyword.lower()

                start_index = lower_text.find(lower_keyword)

                while start_index != -1:

                    end_index = start_index + len(keyword)

                    start = f"1.{start_index}"
                    end = f"1.{end_index}"

                    msg_label.tag_add("highlight", start, end)

                    start_index = lower_text.find(lower_keyword, end_index)

                msg_label.tag_config(
                    "highlight",
                    background="#FFD54F",
                    foreground="black",
                    font=("Arial", 12, "bold")
                )

            msg_label.configure(state="disabled")


        def toggle():

            nonlocal is_expanded

            is_expanded = not is_expanded

            if is_expanded:

                apply_highlight(full_text)

                toggle_btn.configure(text="see less")

            else:

                preview_text = (
                    full_text[:preview_length]
                    + ("..." if len(full_text) > preview_length else "")
                )

                apply_highlight(preview_text)

                toggle_btn.configure(text="see more...")
        msg_label = tk.Text(
            container,
            wrap="word",
            height=2,
            bg="#1E1E1E" if is_dark else "#FFFFFF",
            fg="white" if is_dark else "black",
            insertbackground="white" if is_dark else "black",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            selectbackground="#1E1E1E" if is_dark else "#FFFFFF",
            selectforeground="white" if is_dark else "black",
            cursor="arrow",
            takefocus=0,
            font=("Arial", 12)
        )

        msg_label.pack(fill="x", anchor="w")

        display_text = (
            full_text[:preview_length]
            + ("..." if len(full_text) > preview_length else "")
        )

        # insert FIRST
        msg_label.insert("1.0", display_text)

        # highlight keyword
        if keyword:

            lower_text = display_text.lower()
            lower_keyword = keyword.lower()

            start_index = lower_text.find(lower_keyword)

            while start_index != -1:

                end_index = start_index + len(keyword)

                start = f"1.{start_index}"
                end = f"1.{end_index}"

                msg_label.tag_add("highlight", start, end)

                start_index = lower_text.find(lower_keyword, end_index)

            msg_label.tag_config(
                "highlight",
                background="#FFD54F",
                foreground="black",
                font=("Arial", 12, "bold")
            )

        # disable LAST
        msg_label.configure(state="disabled")
        
        if len(full_text) > preview_length:
            toggle_btn = ctk.CTkButton(
                    container,
                    text="see more...",
                    font=("Arial", 11),
                    text_color="#2980B9",
                    fg_color="transparent",
                    hover=False,
                    anchor="w",
                    width=1,
                    height=20,
                    corner_radius=0,
                    border_spacing=0,
                    compound="left",
                    command=toggle
                )
            toggle_btn.pack(anchor="w", padx=(0, 0), pady=(4, 0))

        return container    
    def add_reply(self, announcement_id, textbox):
        try:
            reply_text = textbox.get("1.0", "end-1c").strip()

            # Ignore empty or placeholder text
            if not reply_text or reply_text == "Write a reply...":
                return

            # Save reply to database
            self.db.insert_reply(announcement_id, self.user, reply_text)

            # Reset textbox with placeholder
            textbox.delete("1.0", "end")
            textbox.insert("1.0", "Write a reply...")
            textbox.configure(text_color="#888888")
            textbox.configure(height=35)

            # Refresh UI
            if self.date_filter_active:
                self.apply_date_filter()
            else:
                self.refresh_list(
                search_keyword=self.current_search_keyword
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
        
    def go_to_form_page(self, row=None):
        self.pack_forget()

        self.master.create_page = CreateAnnouncementPage(
            self.master,
            self.user,
            back_callback=self.back_to_main,
            edit_data=row   # 👈 pass data
        )
        self.master.create_page.pack(fill="both", expand=True)


    def back_to_main(self):
        self.master.create_page.destroy()
        self.db = Database()
        self.pack(fill="both", expand=True)
        self.refresh_list()
    
    def back_from_reply_edit(self):
        self.master.edit_reply_page.destroy()
        self.db = Database()
        self.pack(fill="both", expand=True)

        if self.date_filter_active:
            self.apply_date_filter()
        else:
            self.refresh_list(search_keyword=self.current_search_keyword)
        
    def bind_close_menu(self):
    # အရင် bind ရှိရင် ဖျက်
        self.winfo_toplevel().unbind("<Button-1>")

        # အသစ် bind
        self.winfo_toplevel().bind("<Button-1>", self.close_menu_on_click)


    def close_menu_on_click(self, event):
        if not hasattr(self, "active_menu") or not self.active_menu.winfo_exists():
            return

        click_x = event.x_root
        click_y = event.y_root

        menu_x = self.active_menu.winfo_rootx()
        menu_y = self.active_menu.winfo_rooty()
        menu_w = self.active_menu.winfo_width()
        menu_h = self.active_menu.winfo_height()

        inside_menu = (
            menu_x <= click_x <= menu_x + menu_w and
            menu_y <= click_y <= menu_y + menu_h
        )

        if not inside_menu:
            self.active_menu.destroy()
            self.winfo_toplevel().unbind("<Button-1>")
            
            
class EditReplyPage(ctk.CTkFrame):
    def __init__(self, master, user_data, reply_data, back_callback):
        super().__init__(master, fg_color=("white", "#0E0E0E"))

        self.db = Database()
        self.user = user_data
        self.reply_data = reply_data
        self.back_callback = back_callback

        # ================= MAIN CONTAINER =================
        container = ctk.CTkFrame(
            self,
            fg_color=("#FFFFFF", "#1A1A1A"),
            corner_radius=15
        )
        container.pack(fill="both", expand=True, padx=80, pady=30)

        # ================= BACK BUTTON =================
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

        # ================= REPLY TEXTBOX =================
        self.reply_txt = ctk.CTkTextbox(
            container,
            height=300,
            corner_radius=10,
            fg_color="#DADADA",
            text_color="#000000",
            border_width=0,
            font=("Arial", 14)
        )
        self.reply_txt.pack(fill="both", expand=True, padx=30, pady=10)

        self.reply_txt.insert("1.0", self.reply_data.get("message", ""))

        # ================= UPDATE BUTTON =================
        update_btn = ctk.CTkButton(
            container,
            text="Update Now",
            width=100,
            height=35,
            corner_radius=10,
            fg_color="#F1C40F",
            hover_color="#D4AC0D",
            text_color="black",
            command=self.update_reply
        )
        update_btn.pack(pady=20)

    def update_reply(self):
        new_msg = self.reply_txt.get("1.0", "end-1c").strip()

        if not new_msg:
            messagebox.showwarning("Error", "Reply cannot be empty")
            return

        try:
            self.db.cursor.execute(
                "UPDATE announcement_replies SET message=%s WHERE id=%s",
                (new_msg, self.reply_data["id"])
            )
            self.db.conn.commit()

            messagebox.showinfo("Success", "Reply updated successfully")
            self.back_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))
class CreateAnnouncementPage(ctk.CTkFrame):
    def __init__(self, master, user_data, back_callback, edit_data=None):
        super().__init__(master, fg_color=("white", "#0E0E0E"))  # Dark background
        
        self.db = Database()
        self.user = user_data
        self.back_callback = back_callback
        self.edit_data = edit_data
       

        # ================= MAIN CONTAINER =================
        container = ctk.CTkFrame(
            self,
            fg_color=("#FFFFFF", "#1A1A1A"),
            corner_radius=15
        )
        container.pack(fill="both", expand=True, padx=80, pady=30)

        # ================= BACK BUTTON =================
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

        # ================= TITLE ENTRY =================
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

        # ================= MESSAGE TEXTBOX =================
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
        if self.edit_data:
            self.title_ent.insert(0, self.edit_data['title'])
            self.msg_ent.insert("0.0", self.edit_data['message'])

        # ================= POST BUTTON =================
        post_btn = ctk.CTkButton(
            container,
            text="Update Now" if self.edit_data else "Post",
            width=60,
            height=35,
            corner_radius=10,
            fg_color="#F1C40F",
            hover_color="#D4AC0D",
            text_color="black", 
            command=self.save
        )
        post_btn.pack(pady=20)

    def save(self):
        t = self.title_ent.get()
        m = self.msg_ent.get("0.0", "end-1c").strip()

        if not t or not m:
            messagebox.showwarning("Error", "Fill all fields")
            return

        try:
            if self.edit_data:
                self.db.cursor.execute(
                    "UPDATE announcements SET title=%s, message=%s WHERE id=%s",
                    (t, m, self.edit_data['id'])
                )
            else:
                # 1. Insert the announcement (Existing code)
                self.db.cursor.execute(
                    "INSERT INTO announcements (title, message, sender_role, created_by, user_id) VALUES (%s, %s, 'admin', %s, %s)",
                    (t, m, self.user['full_name'], self.user['id'])
                )
                
                # 2. ADD THIS: Notify all users about the new announcement
                # We use the keyword 'announcement' for the sidebar filter
                notif_msg = f"New Announcement: {t}"
                self.db.cursor.execute(
                    """
                    INSERT INTO notifications (user_id, message, is_read, created_at)
                    SELECT id, %s, 0, NOW() FROM users WHERE id != %s
                    """, 
                    (notif_msg, self.user['id']))
            self.db.conn.commit()
            messagebox.showinfo("Success", "Saved successfully")
            self.back_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))