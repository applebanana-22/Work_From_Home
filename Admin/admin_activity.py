import customtkinter as ctk
from database import Database
from tkinter import messagebox
from datetime import datetime
 
class AdminAnnouncements(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user_data
        self.edit_id = None
        self.form_visible = False
        self.placeholder = "Type a message..."

        # --- 1. HEADER ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=100, pady=(10, 0))
 
        self.toggle_btn = ctk.CTkButton(self.header_frame, text="+ Create New", width=60, height=35,
                                        corner_radius=20, font=("Arial", 13, "bold"),
                                        fg_color="#27AE60",hover_color="#1E8449", command=self.go_to_form_page)
        self.toggle_btn.pack(side="left")
        
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
 
        # --- TITLE ---
        ctk.CTkLabel(
            self,
            text="Admin Post History",
            font=("Arial", 18, "bold"),
            text_color=("black", "white")
        ).pack(anchor="w", padx=100, pady=(10, 0))
 
        # --- LIST ---
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=100, pady=10)
 
        self.list_frame.configure(
            fg_color=("white", "black"),
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
                    self.db.cursor.execute("UPDATE announcements SET title=%s, message=%s WHERE id=%s", (t, m, self.edit_id))
                else:
                    self.db.cursor.execute("INSERT INTO announcements (title, message, sender_role, created_by) VALUES (%s, %s, 'admin', %s)",
                                           (t, m, self.user['full_name']))
                self.db.conn.commit()
                # self.reset_form()
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Database Error", f"Check your table columns: {e}")
 
    def refresh_list(self):
        for widget in self.list_frame.winfo_children(): widget.destroy()
        try:
            self.db.cursor.execute("SELECT id, title, message, created_at FROM announcements WHERE sender_role = 'admin' ORDER BY created_at DESC")
            for row in self.db.cursor.fetchall():
                
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
               
                header_f = ctk.CTkFrame(text_container, fg_color="transparent")
                header_f.pack(fill="x")
               
                ctk.CTkLabel(header_f, text=row['title'], font=("Arial", 14),text_color=("black", "white")).pack(side="left")
               
                # Format time logic
                post_time = row['created_at'].strftime("%Y-%m-%d | %I:%M %p") if isinstance(row['created_at'], datetime) else str(row['created_at'])
                ctk.CTkLabel(header_f, text=post_time, font=("Arial", 10), text_color=("black", "white")).pack(side="left", padx=15)
                btn_frame = ctk.CTkFrame(header_f, fg_color="transparent")
                btn_frame.pack(side="right")
                ctk.CTkButton(btn_frame, text="Delete", width=70, fg_color="#E74C3C",hover_color="#C0392B" ,command=lambda i=row['id']: self.handle_delete(i)).pack(side="left", padx=5)
                ctk.CTkButton(btn_frame, text="Edit", width=60, fg_color="#2980B9", command=lambda r=row: self.go_to_form_page(r)).pack(side="left", padx=5)
               
                # ctk.CTkLabel(text_container, text=row['message'], font=("Arial", 12), wraplength=450, justify="left", anchor="w", text_color="#121212").pack(fill="x", pady=(2, 0))
                self.create_expandable_message(text_container, row['message'])
                # ================= SHOW REPLIES =================
                self.db.cursor.execute(
                    "SELECT * FROM announcement_replies "
                    "WHERE announcement_id=%s ORDER BY created_at ASC",
                    (row['id'],)
                )
                replies = self.db.cursor.fetchall()

                MAX_VISIBLE_REPLIES = 3

                # Only create replies container if replies exist
                if replies:
                    replies_container = ctk.CTkFrame(
                        text_container,
                        fg_color="transparent"
                    )
                    replies_container.pack(fill="x", padx=5, pady=(5, 0))

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
                            reply_box.pack(fill="x", padx=10, pady=3)

                            r_name = reply.get("created_by", "User")
                            r_msg = reply.get("message", "")
                            r_time = reply["created_at"].strftime("%Y-%m-%d | %I:%M %p")

                            ctk.CTkLabel(
                                reply_box,
                                text=f"{r_name} ({r_time})",
                                font=("Arial", 11, "bold"),
                                text_color=("black", "#DDDDDD")
                            ).pack(anchor="w", padx=8, pady=(3, 0))

                            ctk.CTkLabel(
                                reply_box,
                                text=r_msg,
                                font=("Arial", 12),
                                text_color=("black", "#DDDDDD"),
                                wraplength=600,
                                justify="left"
                            ).pack(anchor="w", padx=8, pady=(0, 5))

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
                            toggle_label.pack(anchor="w", padx=12, pady=(2, 5))

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
                    ).pack(anchor="w", padx=10, pady=(5, 0))

                # ================= REPLY INPUT =================
                reply_frame = ctk.CTkFrame(text_container, fg_color="transparent")
                reply_frame.pack(fill="x", padx=10, pady=(5, 5))

                reply_entry = ctk.CTkTextbox(
                    reply_frame,
                    height=35,
                    corner_radius=8,
                    fg_color=("#EEEEEE", "#2A2A2A"),
                    text_color=("black", "white"),
                    wrap="word"
                )
                reply_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

                # ================= PLACEHOLDER FOR REPLY BOX =================
                placeholder_text = "Write a reply..."

                # Insert placeholder initially
                reply_entry.insert("1.0", placeholder_text)
                reply_entry.configure(text_color="gray")


                def clear_placeholder(event, box=reply_entry, text=placeholder_text):
                    """Remove placeholder when textbox gains focus."""
                    if box.get("1.0", "end-1c") == text:
                        box.delete("1.0", "end")
                        box.configure(text_color="white")


                def restore_placeholder(event, box=reply_entry, text=placeholder_text):
                    """Restore placeholder when textbox loses focus and is empty."""
                    if not box.get("1.0", "end-1c").strip():
                        box.insert("1.0", text)
                        box.configure(text_color="gray")


                # Bind events
                reply_entry.bind("<FocusIn>", clear_placeholder)
                reply_entry.bind("<FocusOut>", restore_placeholder)
                announcement_id = row['id']

                ctk.CTkButton(
                    reply_frame,
                    text="➤",
                    width=35,
                    height=35,
                    fg_color="#0A93F5",
                    hover_color="#0873C4",
                    command=lambda a_id=announcement_id, e=reply_entry: self.add_reply(a_id, e)
                ).pack(side="right")

                reply_entry.bind(
                    "<Control-Return>",
                    lambda event, a_id=announcement_id, e=reply_entry:
                    self.send_with_ctrl_enter(event, a_id, e)
                )
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
            self.refresh_list()
    
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

        # message label
        msg_label = ctk.CTkLabel(
            container,
            text=full_text[:preview_length] + ("..." if len(full_text) > preview_length else ""),
            font=("Arial", 12),
            wraplength=450,
            justify="left",
            anchor="w",
            text_color=("black", "white")
        )
        msg_label.pack(anchor="w")

        # show button ONLY if text is long
        if len(full_text) > preview_length:
            toggle_btn = ctk.CTkButton(
                container,
                text="see more...",
                font=("Arial", 11),
                text_color="#2980B9",
                fg_color="transparent",
                hover=False,
                anchor="w",
                command=toggle
            )
            toggle_btn.pack(anchor="w")
            

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
            textbox.configure(text_color="gray")

            # Refresh UI
            self.refresh_list()

        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def send_with_ctrl_enter(self, event, announcement_id, textbox):
        self.add_reply(announcement_id, textbox)
        return "break"
            
        
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
        container.pack(fill="both", expand=True, padx=100, pady=30)

        # ================= BACK BUTTON =================
        back_btn = ctk.CTkButton(
            container,
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
                self.db.cursor.execute(
                    "INSERT INTO announcements (title, message, sender_role, created_by) VALUES (%s, %s, 'admin', %s)",
                    (t, m, self.user['full_name'])
                )

            self.db.conn.commit()
            messagebox.showinfo("Success", "Saved successfully")
            self.back_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))