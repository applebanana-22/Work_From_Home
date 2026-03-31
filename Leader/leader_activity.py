import customtkinter as ctk
from database import Database
from tkinter import messagebox
from datetime import datetime

class LeaderActivity(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user_data
        self.edit_id = None 
        self.form_visible = False
        self.placeholder = "Type a team message..."

        # Configure Grid to force 50/50 split
        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        # --- 1. UPPER HALF: LEADER SECTION (50%) ---
        self.upper_half = ctk.CTkFrame(self, fg_color="transparent")
        self.upper_half.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.leader_header = ctk.CTkFrame(self.upper_half, fg_color="transparent")
        self.leader_header.pack(fill="x", padx=20, pady=(10, 5))

        ctk.CTkLabel(self.leader_header, text="Team Announcements", font=("Arial", 20, "bold")).pack(side="left")

        self.toggle_btn = ctk.CTkButton(self.leader_header, text="+ Create New", width=130, height=35,
                                        corner_radius=20, font=("Arial", 13, "bold"),
                                        fg_color="#D68910", hover_color="#B9770E",
                                        command=self.toggle_form)
        self.toggle_btn.pack(side="right")

        self.form_frame = ctk.CTkFrame(self.upper_half, corner_radius=12, border_width=1, border_color="gray30")
        
        self.title_ent = ctk.CTkEntry(self.form_frame, placeholder_text="Add a subject (Title)", height=40)
        self.title_ent.pack(fill="x", padx=15, pady=(15, 5))

        self.msg_ent = ctk.CTkTextbox(self.form_frame, height=80, border_width=1, text_color="gray")
        self.msg_ent.pack(fill="x", padx=15, pady=5)
        self.msg_ent.insert("0.0", self.placeholder)
        
        self.msg_ent.bind("<FocusIn>", self.clear_placeholder)
        self.msg_ent.bind("<FocusOut>", self.restore_placeholder)

        self.post_btn = ctk.CTkButton(self.form_frame, text="Post to Team", fg_color="#D68910", 
                                      command=self.handle_save)
        self.post_btn.pack(side="right", padx=15, pady=(0, 10))

        self.leader_list = ctk.CTkScrollableFrame(self.upper_half, label_text="Your Post History", 
                                                 label_font=("Arial", 13, "bold"))
        self.leader_list.pack(fill="both", expand=True, padx=20, pady=5)

        # --- SEPARATOR LINE ---
        self.sep = ctk.CTkFrame(self, height=2, fg_color="gray30")
        self.sep.grid(row=0, column=0, sticky="s", padx=40)

        # --- 2. LOWER HALF: ADMIN SECTION (50%) ---
        self.lower_half = ctk.CTkFrame(self, fg_color="transparent")
        self.lower_half.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.admin_header = ctk.CTkFrame(self.lower_half, fg_color="transparent")
        self.admin_header.pack(fill="x", padx=20, pady=(5, 5))
        ctk.CTkLabel(self.admin_header, text="📢 Company News (From Admin)", 
                     font=("Arial", 16, "bold"), text_color="#2E86C1").pack(side="left")

        self.admin_view = ctk.CTkScrollableFrame(self.lower_half, label_text="Global Announcements", 
                                                 border_width=1, border_color="#2E86C1")
        self.admin_view.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.refresh_ui()

    # --- Logic Methods ---
    def clear_placeholder(self, event):
        if self.msg_ent.get("0.0", "end-1c") == self.placeholder:
            self.msg_ent.delete("0.0", "end")
            self.msg_ent.configure(text_color=("black", "white"))

    def restore_placeholder(self, event):
        if not self.msg_ent.get("0.0", "end-1c").strip():
            self.msg_ent.insert("0.0", self.placeholder)
            self.msg_ent.configure(text_color="gray")

    def toggle_form(self):
        if not self.form_visible:
            self.form_frame.pack(after=self.leader_header, fill="x", padx=20, pady=10)
            self.toggle_btn.configure(text="Cancel", fg_color="gray30")
            self.form_visible = True
        else:
            self.reset_form()

    def handle_save(self):
        t, m = self.title_ent.get(), self.msg_ent.get("0.0", "end-1c").strip()
        if not t or not m or m == self.placeholder:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        if messagebox.askyesno("Confirm", "Post this announcement to your team?"):
            try:
                if self.edit_id:
                    self.db.cursor.execute("UPDATE announcements SET title=%s, message=%s WHERE id=%s", (t, m, self.edit_id))
                else:
                    self.db.cursor.execute("INSERT INTO announcements (title, message, sender_role, created_by) VALUES (%s, %s, 'leader', %s)", 
                                           (t, m, self.user['full_name']))
                self.db.conn.commit()
                self.reset_form()
                self.refresh_ui()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def handle_delete(self, ann_id):
        if messagebox.askyesno("Confirm", "Delete this post forever?"):
            self.db.cursor.execute("DELETE FROM announcements WHERE id=%s", (ann_id,))
            self.db.conn.commit()
            self.refresh_ui()

    def prepare_edit(self, row):
        if not self.form_visible: self.toggle_form()
        self.edit_id = row['id']
        self.title_ent.delete(0, 'end'); self.title_ent.insert(0, row['title'])
        self.msg_ent.delete("0.0", "end"); self.msg_ent.insert("0.0", row['message'])
        self.msg_ent.configure(text_color=("black", "white"))
        self.post_btn.configure(text="Update Now", fg_color="#F39C12")

    def refresh_ui(self):
        for w in self.admin_view.winfo_children(): w.destroy()
        for w in self.leader_list.winfo_children(): w.destroy()

        try:
            # 1. Load Leader Feed
            self.db.cursor.execute("SELECT * FROM announcements WHERE sender_role='leader' ORDER BY created_at DESC")
            for row in self.db.cursor.fetchall():
                item = ctk.CTkFrame(self.leader_list, corner_radius=8)
                item.pack(fill="x", pady=5, padx=10)
                
                txt_f = ctk.CTkFrame(item, fg_color="transparent")
                txt_f.pack(side="left", fill="both", expand=True, padx=10, pady=8)
                
                h_f = ctk.CTkFrame(txt_f, fg_color="transparent")
                h_f.pack(fill="x")
                ctk.CTkLabel(h_f, text=row['title'], font=("Arial", 14, "bold")).pack(side="left")
                
                # Time Formatting
                time_str = row['created_at'].strftime("%Y-%m-%d | %I:%M %p") if isinstance(row['created_at'], datetime) else str(row['created_at'])
                ctk.CTkLabel(h_f, text=time_str, font=("Arial", 10), text_color="gray60").pack(side="left", padx=15)
                
                ctk.CTkLabel(txt_f, text=row['message'], wraplength=400, justify="left", text_color="gray80").pack(fill="x")

                btn_f = ctk.CTkFrame(item, fg_color="transparent")
                btn_f.pack(side="right", padx=10)
                ctk.CTkButton(btn_f, text="Delete", width=65, fg_color="#C0392B", command=lambda i=row['id']: self.handle_delete(i)).pack(side="right", padx=2)
                ctk.CTkButton(btn_f, text="Edit", width=55, fg_color="#2980B9", command=lambda r=row: self.prepare_edit(r)).pack(side="right", padx=2)

            # 2. Load Admin Feed
            self.db.cursor.execute("SELECT title, message, created_at FROM announcements WHERE sender_role='admin' ORDER BY created_at DESC")
            for r in self.db.cursor.fetchall():
                f = ctk.CTkFrame(self.admin_view, border_width=1, border_color="gray30")
                f.pack(fill="x", pady=3, padx=10)
                date = r['created_at'].strftime("%Y-%m-%d") if isinstance(r['created_at'], datetime) else str(r['created_at'])
                ctk.CTkLabel(f, text=f"📢 {r['title']} ({date})", font=("Arial", 12, "bold"), anchor="w").pack(fill="x", padx=10, pady=(5,0))
                ctk.CTkLabel(f, text=r['message'], wraplength=450, justify="left", text_color="gray80").pack(fill="x", padx=15, pady=(0,5))
        except Exception as e:
            print(f"UI Refresh Error: {e}")

    def reset_form(self):
        self.form_frame.pack_forget()
        self.edit_id = None
        self.title_ent.delete(0, 'end')
        self.msg_ent.delete("0.0", "end"); self.msg_ent.insert("0.0", self.placeholder)
        self.msg_ent.configure(text_color="gray")
        self.toggle_btn.configure(text="+ Create New", fg_color="#D68910")
        self.post_btn.configure(text="Post to Team", fg_color="#D68910")
        self.form_visible = False