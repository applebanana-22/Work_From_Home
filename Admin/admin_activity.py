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
        # ctk.CTkLabel(self.header_frame, text="Admin Announcements", font=("Arial", 20, "bold")).pack(side="left")
 
        self.toggle_btn = ctk.CTkButton(self.header_frame, text="+ Create New", width=60, height=35,
                                        corner_radius=20, font=("Arial", 13, "bold"),
                                        fg_color="#D68910", hover_color="#B9770E", command=self.toggle_form)
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
            text_color="white"
        ).pack(anchor="w", padx=100, pady=(10, 0))
 
        # --- LIST ---
        self.list_frame = ctk.CTkScrollableFrame(self)
        # self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.list_frame.pack(fill="both", expand=True, padx=100, pady=10)
 
        self.list_frame.configure(
            fg_color="#121212",
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
 
    def toggle_form(self):
        if not self.form_visible:
            self.form_frame.pack(after=self.header_frame, fill="x", padx=100, pady=10)
            self.toggle_btn.configure(text="Cancel",   fg_color="gray30")
            self.form_visible = True
        else:
            self.reset_form()
 
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
                self.reset_form()
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Database Error", f"Check your table columns: {e}")
 
    def reset_form(self):
        self.form_frame.pack_forget()
        self.edit_id = None
        self.title_ent.delete(0, 'end')
        self.msg_ent.delete("0.0", "end")
        self.msg_ent.insert("0.0", self.placeholder)
        self.msg_ent.configure(text_color="gray")
        self.post_btn.configure(text="Post", fg_color="#D68910")
        self.toggle_btn.configure(text="+ Create New",corner_radius=20,   fg_color="#D68910")
        self.form_visible = False
 
    def refresh_list(self):
        for widget in self.list_frame.winfo_children(): widget.destroy()
        try:
            self.db.cursor.execute("SELECT id, title, message, created_at FROM announcements WHERE sender_role = 'admin' ORDER BY created_at DESC")
            for row in self.db.cursor.fetchall():
                item = ctk.CTkFrame(self.list_frame, corner_radius=8)
                item.pack(fill="x", pady=5, padx=10)
               
                text_container = ctk.CTkFrame(item, fg_color="transparent")
                text_container.pack(side="left", fill="both", expand=True, padx=10, pady=8)
               
                header_f = ctk.CTkFrame(text_container, fg_color="transparent")
                header_f.pack(fill="x")
               
                ctk.CTkLabel(header_f, text=row['title'], font=("Arial", 14, "bold"), anchor="w").pack(side="left")
               
                # Format time logic
                post_time = row['created_at'].strftime("%Y-%m-%d | %I:%M %p") if isinstance(row['created_at'], datetime) else str(row['created_at'])
                ctk.CTkLabel(header_f, text=post_time, font=("Arial", 10), text_color="#121212").pack(side="left", padx=15)
               
                # ctk.CTkLabel(text_container, text=row['message'], font=("Arial", 12), wraplength=450, justify="left", anchor="w", text_color="#121212").pack(fill="x", pady=(2, 0))
                self.create_expandable_message(text_container, row['message'])
                btn_frame = ctk.CTkFrame(item, fg_color="transparent")
                btn_frame.pack(side="right", padx=10)
                ctk.CTkButton(btn_frame, text="Delete", width=70, fg_color="#C0392B", command=lambda i=row['id']: self.handle_delete(i)).pack(side="right", padx=2)
                ctk.CTkButton(btn_frame, text="Edit", width=60, fg_color="#2980B9", command=lambda r=row: self.prepare_edit(r)).pack(side="right", padx=2)
        except Exception as e:
            print(f"Fetch Error: {e}")
 
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
        preview_length = 30   # control short text length

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
            text_color="#121212"
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
 