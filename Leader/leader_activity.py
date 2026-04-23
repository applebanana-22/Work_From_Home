import customtkinter as ctk
from database import Database
from tkinter import messagebox
from datetime import datetime, timedelta


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

                # ================= HEADER TABS =================
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=100, pady=(10, 5))

        self.current_view = "company"

        self.company_btn = ctk.CTkButton(
            header,
            text="📢 Company",
            fg_color="#2E86C1",
            command=lambda: self.switch_view("company")
        )
        self.company_btn.pack(side="left", padx=5)

        self.team_btn = ctk.CTkButton(
            header,
            text="👥 Your Announcements",
            fg_color="gray30",
            command=lambda: self.switch_view("team")
        )
        self.team_btn.pack(side="left",  padx=5)
        self.badge_count = 0

        self.badge_label = ctk.CTkLabel(
            header,
            text="",
            text_color=("black", "white"),
            fg_color="red",
            corner_radius=10,
            width=20,
            height=20
        )

        self.badge_label.place_forget()   # hide first
                # RIGHT SIDE (Create Button)
        self.create_btn = ctk.CTkButton(
            header,
            text="+ Create New",
            fg_color="#27AE60",
            hover_color="#1E8449",
            corner_radius=20,
            command=self.go_to_create_page
        )

        self.create_btn.pack(side="right", padx=10)
        self.create_btn.pack_forget()

        # ================= SCROLL AREA =================
        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color=("#F5F5F5", "#121212"),
            corner_radius=12
        )
        self.container.pack(fill="both", expand=True, padx=100, pady=10)

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
            self.badge_label.place_forget()   # ✅ clear badge

        if view == "company":
            self.company_btn.configure(fg_color="#2E86C1")
            self.team_btn.configure(fg_color="gray30")
            self.create_btn.pack_forget()
        else:
            self.company_btn.configure(fg_color="gray30")
            self.team_btn.configure(fg_color="#2E86C1")
            self.create_btn.pack(side="right", padx=10)

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
            textbox.configure(text_color="gray")

            # Refresh UI
            self.refresh_ui()

        except Exception as e:
            messagebox.showerror("Error", str(e))
    def send_with_ctrl_enter(self, event, announcement_id, textbox):
        self.add_reply(announcement_id, textbox)
        return "break"  # Prevents a new line after sending

    # ================= UI =================
    def refresh_ui(self):
        for w in self.container.winfo_children():
            w.destroy()

        try:
            self.db = Database()
            self.db.conn.commit() 
            if self.current_view == "company":
                self.db.cursor.execute("""
                    SELECT * FROM announcements
                    WHERE sender_role='admin'
                    ORDER BY created_at DESC
                """)
            else:
                self.db.cursor.execute("""
                    SELECT * FROM announcements
                    WHERE sender_role='leader'
                    ORDER BY created_at DESC
                """)

            for row in self.db.cursor.fetchall():

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

                # ================= HEADER =================
                top = ctk.CTkFrame(right, fg_color="transparent")
                top.pack(fill="x")

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

                    header_f = top   # 👈 IMPORTANT (match your variable name)

                    btn_frame = ctk.CTkFrame(header_f, fg_color="transparent")
                    btn_frame.pack(side="right")

                    ctk.CTkButton(
                        btn_frame,
                        text="Delete",
                         width=70, 
                         fg_color="#E74C3C",
                         hover_color="#C0392B" ,
                        command=lambda i=row['id']: self.handle_delete(i)
                    ).pack(side="left", padx=5)

                    ctk.CTkButton(
                        btn_frame,
                        text="Edit",
                        width=60,
                        fg_color="#2980B9",
                        command=lambda r=row: self.go_to_create_page(r)
                    ).pack(side="left", padx=5)

                # TITLE
                ctk.CTkLabel(
                    right,
                    text=row['title'],
                    font=("Arial", 15, "bold"),
                    text_color=("black", "white")
                ).pack(anchor="w", pady=(5, 2))
                self.create_expandable_message(right, row['message'])

                # ================= REPLY INPUT =================
                # ================= ACTION AREA =================
                # ================= SHOW REPLIES =================
                self.db.cursor.execute(
                    "SELECT * FROM announcement_replies WHERE announcement_id=%s ORDER BY created_at ASC",
                    (row['id'],)
                )

                replies = self.db.cursor.fetchall()

                MAX_VISIBLE_REPLIES = 3

                if replies:
                    replies_container = ctk.CTkFrame(right, fg_color="transparent")
                    replies_container.pack(fill="x", padx=5, pady=(5, 0))

                    def render_replies(show_all=False, replies_list=replies, container=replies_container):
                        # clear
                        for w in container.winfo_children():
                            w.destroy()

                        visible = replies_list if show_all else replies_list[:MAX_VISIBLE_REPLIES]

                        for reply in visible:
                            reply_box = ctk.CTkFrame(
                                container,
                                fg_color=("#EEEEEE", "#2A2A2A"),
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
                                text_color=("black", "white")
                            ).pack(anchor="w", padx=8, pady=(3, 0))

                            ctk.CTkLabel(
                                reply_box,
                                text=r_msg,
                                font=("Arial", 12),
                                text_color=("black", "white"),
                                wraplength=600,
                                justify="left"
                            ).pack(anchor="w", padx=8, pady=(0, 5))

                        # toggle button
                        if len(replies_list) > MAX_VISIBLE_REPLIES:
                            toggle = ctk.CTkLabel(
                                container,
                                text="Show all replies ({})".format(len(replies_list))
                                if not show_all else "Show less",
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
                        text_color="#777777",
                        font=("Arial", 11)
                    ).pack(anchor="w", padx=10, pady=(5, 0))

               
                  # ================= REPLY INPUT (FOR BOTH) =================
                reply_frame = ctk.CTkFrame(right, fg_color="transparent")
                reply_frame.pack(fill="x", padx=10, pady=(5, 5))

                reply_entry = ctk.CTkTextbox(
                    reply_frame,
                    height=35,           # Fixed height
                    corner_radius=8,
                    fg_color="#AAA7A7", 
                    wrap="word"
                )
                reply_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

               # Placeholder text
                placeholder_text = "Write a reply..."
                reply_entry.insert("1.0", placeholder_text)
                reply_entry.configure(text_color="gray")

                def clear_placeholder(event, box=reply_entry):
                    if box.get("1.0", "end-1c") == placeholder_text:
                        box.delete("1.0", "end")
                        box.configure(text_color=("black", "white"))

                def restore_placeholder(event, box=reply_entry):
                    if not box.get("1.0", "end-1c").strip():
                        box.insert("1.0", placeholder_text)
                        box.configure(text_color="gray")

                reply_entry.bind("<FocusIn>", clear_placeholder)
                reply_entry.bind("<FocusOut>", restore_placeholder)

                # Send button
                ctk.CTkButton(
                    reply_frame,
                    text="➤",
                    width=35,
                    height=35,
                    fg_color="#0A93F5",
                    hover_color="#0873C4",
                    command=lambda a_id=row['id'], e=reply_entry: self.add_reply(a_id, e)
                ).pack(side="right")

                # Bind Ctrl + Enter to send reply
                reply_entry.bind(
                    "<Control-Return>",
                    lambda event, a_id=row['id'], e=reply_entry:
                        self.send_with_ctrl_enter(event, a_id, e)
                )
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

        # Message label
        short_text = full_text[:preview_length] + ("..." if len(full_text) > preview_length else "")

        msg_label = ctk.CTkLabel(
            container,
            text=short_text,
            wraplength=700,
            justify="left",
            text_color=("black", "white")
        )
        msg_label.pack(anchor="w")

        # Show button only if long text
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

        self.current_view = "team"
        self.pack(fill="both", expand=True)

        self.switch_view("team")
        
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
            width=60,
            height=35,
            fg_color="#2E86C1",
            hover_color="#1F618D",
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
                self.db.cursor.execute(
                    "INSERT INTO announcements (title, message, sender_role, created_by, created_at) VALUES (%s, %s, %s, %s, NOW())",
                    (title, message, "leader", self.user['full_name'])
                )

            self.db.conn.commit()
            messagebox.showinfo("Success", "Saved successfully")
            self.back_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))