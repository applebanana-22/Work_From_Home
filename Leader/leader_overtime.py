import customtkinter as ctk
from database import Database
from tkinter import messagebox
from datetime import date
from tkcalendar import DateEntry, Calendar


# ================= AUTOCOMPLETE =================
class AutocompleteComboBox(ctk.CTkFrame):
    def __init__(self, master, values, width=200, height=35, placeholder_text=""):
        super().__init__(master, fg_color="transparent")

        self.values = values
        self.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self, height=height, width=width, placeholder_text=placeholder_text)
        self.entry.grid(row=0, column=0, sticky="ew")

        self.button = ctk.CTkButton(
            self,
            text="▼",
            width=35,
            height=height,
            fg_color="#2980B9",
            hover_color="#1F618D",
            text_color="white",
            command=self.toggle_dropdown
        )
        self.button.grid(row=0, column=1, padx=(2, 0))

        self.entry.bind("<KeyRelease>", self.on_type)
        self.entry.bind("<FocusOut>", lambda e: self.after(150, self.hide_dropdown))

    def create_dropdown(self):
        if hasattr(self, "popup") and self.popup.winfo_exists():
            return

        self.popup = ctk.CTkToplevel(self)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)

        self.listbox = ctk.CTkScrollableFrame(self.popup, height=150)
        self.listbox.pack(fill="both", expand=True)

    def show_dropdown(self, data):
        self.create_dropdown()

        for w in self.listbox.winfo_children():
            w.destroy()

        for item in data:
            ctk.CTkButton(
                self.listbox,
                text=item,
                anchor="w",
                fg_color="transparent",
                hover_color="#333333",
                text_color="white",
                command=lambda v=item: self.select(v)
            ).pack(fill="x", padx=5, pady=2)

        self.update_idletasks()
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()

        self.popup.geometry(f"{self.entry.winfo_width()}x150+{x}+{y}")
        self.popup.deiconify()

    def hide_dropdown(self):
        if hasattr(self, "popup"):
            self.popup.withdraw()

    def toggle_dropdown(self):
        if hasattr(self, "popup") and self.popup.winfo_viewable():
            self.hide_dropdown()
        else:
            self.show_dropdown(self.values)

    def on_type(self, event):
        text = self.entry.get().lower()
        if not text:
            self.hide_dropdown()
            return

        filtered = [v for v in self.values if text in v.lower()]
        if filtered:
            self.show_dropdown(filtered)
        else:
            self.hide_dropdown()

    def select(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        self.hide_dropdown()

    def get(self):
        return self.entry.get()


# ================= MAIN CLASS =================
class LeaderOvertime(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")

        self.db = Database()
        self.user = user_data

        self.db.cursor.execute(
            "SELECT team_id FROM users WHERE id = %s",
            (self.user['id'],)
        )
        self.team_id = self.db.cursor.fetchone()['team_id']

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # HEADER
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=120, pady=15)

        ctk.CTkLabel(
            header,
            text="🕒 Overtime Management",
            font=("Arial", 22, "bold")
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="+ Add Overtime",
            fg_color="#10B981",
            hover_color="#059669",
            height=40,
            command=self.open_popup
        ).pack(side="right")

        # FILTER
        filter_frame = ctk.CTkFrame(
            self,
            fg_color="#1E1E1E",
            corner_radius=12,
            border_width=1,
            border_color="#2A2A2A"
        )
        filter_frame.grid(row=1, column=0, sticky="ew", padx=115, pady=10)

        self.db.cursor.execute("""
            SELECT full_name FROM users
            WHERE team_id = %s AND role = 'member'
        """, (self.team_id,))

        members = self.db.cursor.fetchall()
        self.member_names = [m['full_name'] for m in members]

        self.db.cursor.execute("""
            SELECT project_name FROM projects
            WHERE team_id = %s
        """, (self.team_id,))

        projects = self.db.cursor.fetchall()
        self.project_names = [p['project_name'] for p in projects]

        self.member_search = AutocompleteComboBox(
            filter_frame,
            values=self.member_names,
            width=120,
            placeholder_text="Member..."
        )
        self.member_search.pack(side="left", padx=(10, 5), pady=15)

        self.project_search = AutocompleteComboBox(
            filter_frame,
            values=self.project_names,
            width=120,
            placeholder_text="Project..."
        )
        self.project_search.pack(side="left", padx=5)

        self.status_filter = ctk.CTkOptionMenu(
            filter_frame,
            values=["All", "Pending", "Approved", "Rejected"],
            width=100,
            height=35,
            fg_color="#2980B9",
            button_color="#1F618D"
        )
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=5)

        self.date_filter = ctk.CTkEntry(
            filter_frame,
            placeholder_text="yyyy-mm-dd",
            width=110,
            height=35
        )
        self.date_filter.pack(side="left", padx=5)
        self.date_filter.bind("<Button-1>", lambda e: self.spawn_calendar(self.date_filter))

        btn_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Search",
            fg_color="#10B981",
            hover_color="#059669",
            height=35,
            width=70,
            command=self.refresh_ui
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Clear",
            fg_color="#7F8C8D",
            hover_color="#616A6B",
            height=35,
            width=70,
            command=self.clear_filters
        ).pack(side="right", padx=5)

        # LIST
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=115, pady=10)

        self.list_frame.configure(fg_color="#121212", corner_radius=12)

        self.refresh_ui()

    def spawn_calendar(self, entry_widget):
        top = ctk.CTkToplevel(self)
        x = entry_widget.winfo_rootx()
        y = entry_widget.winfo_rooty() + entry_widget.winfo_height()
        top.geometry(f"250x280+{x}+{y}")
        top.attributes("-topmost", True)
        top.overrideredirect(True)

        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(fill="both", expand=True)

        def select_date():
            entry_widget.delete(0, "end")
            entry_widget.insert(0, cal.get_date())
            top.destroy()
            if entry_widget == getattr(self, "date_filter", None):
                self.refresh_ui()

        def clear_date():
            entry_widget.delete(0, "end")
            top.destroy()
            if entry_widget == getattr(self, "date_filter", None):
                self.refresh_ui()

        btn_frame = ctk.CTkFrame(top, fg_color="transparent")
        btn_frame.pack(pady=5, fill="x")
        ctk.CTkButton(btn_frame, text="Select", command=select_date, width=100).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Clear", command=clear_date, width=100, fg_color="#C0392B").pack(side="right", padx=10)

    def clear_filters(self):
        self.member_search.entry.delete(0, "end")
        self.project_search.entry.delete(0, "end")
        self.date_filter.delete(0, "end")
        self.status_filter.set("All")
        self.refresh_ui()

    # ================= ADD POPUP =================
    def open_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.geometry("450x620")
        popup.grab_set()

        main_frame = ctk.CTkFrame(popup, fg_color="#1E1E1E", corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="✨ Add Overtime", font=("Arial", 20, "bold")).pack(pady=(15, 15))

        self.db.cursor.execute("""
            SELECT id, full_name FROM users
            WHERE team_id = %s AND role = 'member'
        """, (self.team_id,))
        members = self.db.cursor.fetchall()
        self.member_map = {m['full_name']: m['id'] for m in members}

        self.db.cursor.execute("""
            SELECT id, project_name FROM projects
            WHERE team_id = %s
        """, (self.team_id,))
        
        projects = self.db.cursor.fetchall()
        self.project_map = {p['project_name']: p['id'] for p in projects}

        ctk.CTkLabel(main_frame, text="Member").pack(anchor="w", padx=20)
        member_cb = AutocompleteComboBox(main_frame, list(self.member_map.keys()), width=250)
        member_cb.pack(fill="x", padx=20)

        ctk.CTkLabel(main_frame, text="Project").pack(anchor="w", padx=20, pady=(10, 0))
        project_cb = AutocompleteComboBox(main_frame, list(self.project_map.keys()), width=250)
        project_cb.pack(fill="x", padx=20)

        ctk.CTkLabel(main_frame, text="Date").pack(anchor="w", padx=20, pady=(10, 0))
        date_ent = DateEntry(
            main_frame,
            date_pattern="yyyy-mm-dd",
            mindate=date.today(),
            background="#2980B9",
            font=("Arial", 14)
        )
        date_ent.pack(fill="x", padx=20, ipady=3)

        ctk.CTkLabel(main_frame, text="Hours").pack(anchor="w", padx=20, pady=(10, 0))
        hours_ent = ctk.CTkEntry(main_frame)
        hours_ent.pack(fill="x", padx=20)

        ctk.CTkLabel(main_frame, text="Reason").pack(anchor="w", padx=20, pady=(10, 0))
        reason_ent = ctk.CTkTextbox(main_frame, height=80, fg_color="#2A2A2A")
        reason_ent.pack(fill="x", padx=20)

        def save():
            member_id = self.member_map.get(member_cb.get())
            project_id = self.project_map.get(project_cb.get())

            if not member_id or not project_id:
                messagebox.showwarning("Error", "Invalid member/project")
                return

            try:
                h = float(hours_ent.get())
                if h <= 0 or h > 24:
                    messagebox.showwarning("Error", "Hours must be between 0 and 24")
                    return
            except ValueError:
                messagebox.showwarning("Error", "Hours must be a valid number")
                return

            d_str = date_ent.get_date()

            self.db.cursor.execute("""
                SELECT id FROM overtime_requests 
                WHERE member_id = %s AND DATE(ot_date) = %s
            """, (member_id, d_str))
            
            if self.db.cursor.fetchone():
                messagebox.showwarning("Error", f"Overtime request for this member on {d_str} already exists!")
                return

            self.db.cursor.execute("""
                INSERT INTO overtime_requests
                (member_id, project_id, ot_date, hours, reason, status)
                VALUES (%s,%s,%s,%s,%s,'Pending')
            """, (
                member_id,
                project_id,
                d_str,
                h,
                reason_ent.get("0.0", "end").strip()
            ))

            self.db.conn.commit()
            popup.destroy()
            self.refresh_ui()

        ctk.CTkButton(main_frame, text="Save", fg_color="#10B981", hover_color="#059669", height=40, command=save).pack(pady=20)

    # ================= UPDATE POPUP =================
    def open_update_popup(self, row):
        popup = ctk.CTkToplevel(self)
        popup.geometry("450x540")
        popup.grab_set()

        main_frame = ctk.CTkFrame(popup, fg_color="#1E1E1E", corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="✏️ Update Overtime", font=("Arial", 20, "bold")).pack(pady=(15, 10))

        # Read-only fields styling
        def create_info_row(label_text, value_text):
            row_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=4)
            ctk.CTkLabel(row_frame, text=label_text, font=("Arial", 13, "bold"), text_color="#AAAAAA", width=80, anchor="w").pack(side="left")
            ctk.CTkLabel(row_frame, text=value_text, font=("Arial", 14), text_color="white", anchor="w").pack(side="left")

        create_info_row("Member:", row['full_name'])
        create_info_row("Project:", row['project_name'])
        create_info_row("Date:", str(row['ot_date']))
        create_info_row("Status:", row['status'])

        ctk.CTkLabel(main_frame, text="Reason:", font=("Arial", 13, "bold"), text_color="#AAAAAA").pack(anchor="w", padx=20, pady=(10, 0))
        reason_display = ctk.CTkTextbox(main_frame, height=60, fg_color="#2A2A2A")
        reason_display.pack(fill="x", padx=20, pady=(5, 0))
        reason_display.insert("0.0", row['reason'] or "-")
        reason_display.configure(state="disabled")

        # Editable field: Hours
        ctk.CTkLabel(main_frame, text="Update Hours:").pack(anchor="w", padx=20, pady=(15, 0))
        hours_ent = ctk.CTkEntry(main_frame)
        hours_ent.insert(0, str(row['hours']))
        hours_ent.pack(fill="x", padx=20)

        def save():
            try:
                h = float(hours_ent.get())
                if h <= 0 or h > 24:
                    messagebox.showerror("Error", "Hours must be between 0 and 24.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Hours must be a valid number.")
                return

            self.db.cursor.execute("""
                UPDATE overtime_requests
                SET hours=%s
                WHERE id=%s
            """, (h, row['id']))
            self.db.conn.commit()
            popup.destroy()
            self.refresh_ui()

        ctk.CTkButton(main_frame, text="Save Changes", fg_color="#2980B9", hover_color="#1F618D", height=40, command=save).pack(pady=20)

    # ================= LIST =================
    def refresh_ui(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        query = """
            SELECT o.*, u.full_name, p.project_name
            FROM overtime_requests o
            JOIN users u ON o.member_id = u.id
            JOIN projects p ON o.project_id = p.id
            WHERE 1=1
        """
        params = []

        member_val = self.member_search.get().strip()
        if member_val:
            query += " AND u.full_name LIKE %s"
            params.append(f"%{member_val}%")

        project_val = self.project_search.get().strip()
        if project_val:
            query += " AND p.project_name LIKE %s"
            params.append(f"%{project_val}%")

        # Reason search removed

        status_val = self.status_filter.get()
        if status_val != "All":
            query += " AND o.status = %s"
            params.append(status_val)

        date_val = self.date_filter.get().strip()
        if date_val:
            query += " AND DATE(o.ot_date) = %s"
            params.append(date_val)

        query += " ORDER BY o.created_at DESC"

        self.db.cursor.execute(query, tuple(params))
        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(
                self.list_frame,
                text="No overtime requests found matching your search.",
                font=("Arial", 14, "italic"),
                text_color="#888888"
            ).pack(pady=40)
            return

        for row in rows:
            card = ctk.CTkFrame(
                self.list_frame,
                corner_radius=12,
                fg_color="#1E1E1E",
                border_width=1,
                border_color="#2A2A2A"
            )
            card.pack(fill="x", padx=15, pady=10)

            main = ctk.CTkFrame(card, fg_color="transparent")
            main.pack(fill="x", padx=15, pady=12)

            # LEFT CONTENT
            left = ctk.CTkFrame(main, fg_color="transparent")
            left.pack(side="left", fill="both", expand=True)

            # NAME + DATE
            top = ctk.CTkFrame(left, fg_color="transparent")
            top.pack(fill="x")

            ctk.CTkLabel(
                top,
                text=row['full_name'],
                font=("Arial", 14, "bold"),
                text_color="white"
            ).pack(side="left")

            ctk.CTkLabel(
                top,
                text=str(row['ot_date']),
                font=("Arial", 10),
                text_color="#888"
            ).pack(side="left", padx=10)

            # PROJECT
            ctk.CTkLabel(
                left,
                text=row['project_name'],
                font=("Arial", 13),
                text_color="#DDDDDD"
            ).pack(anchor="w", pady=(5, 2))

            # HOURS + STATUS
            ctk.CTkLabel(
                left,
                text=f"{row['hours']} hours  •  {row['status']}",
                font=("Arial", 12),
                text_color="#AAAAAA"
            ).pack(anchor="w")

            # REASON
            self.create_expandable_message(left, row['reason'] or "-", wrap=600)

            # BUTTONS
            btn_frame = ctk.CTkFrame(main, fg_color="transparent")
            btn_frame.pack(side="right", padx=10)

            ctk.CTkButton(
                btn_frame,
                text="Update",
                width=70,
                fg_color="#2980B9",
                command=lambda r=row: self.open_update_popup(r)
            ).pack(pady=3)

            ctk.CTkButton(
                btn_frame,
                text="Delete",
                width=70,
                fg_color="#C0392B",
                command=lambda rid=row['id']: self.delete_record(rid)
            ).pack(pady=3)

    def create_expandable_message(self, parent, full_text, wrap=500):
        preview_length = 40

        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", anchor="w")

        is_expanded = False

        def toggle():
            nonlocal is_expanded
            is_expanded = not is_expanded

            if is_expanded:
                msg_label.configure(text=full_text)
                toggle_btn.configure(text="see less")
            else:
                msg_label.configure(text=full_text[:preview_length] + "...")
                toggle_btn.configure(text="see more")

        msg_label = ctk.CTkLabel(
            container,
            text=full_text[:preview_length] + ("..." if len(full_text) > preview_length else ""),
            wraplength=wrap,
            justify="left",
            anchor="w",
            text_color="#CCCCCC"
        )
        msg_label.pack(anchor="w")

        if len(full_text) > preview_length:
            toggle_btn = ctk.CTkButton(
                container,
                text="see more...",
                font=("Arial", 11),
                text_color="#2980B9",
                fg_color="transparent",
                hover=False,
                command=toggle
            )
            toggle_btn.pack(anchor="w")

    def delete_record(self, rid):
        if messagebox.askyesno("Confirm", "Delete this record?"):
            self.db.cursor.execute("DELETE FROM overtime_requests WHERE id=%s", (rid,))
            self.db.conn.commit()
            self.refresh_ui()