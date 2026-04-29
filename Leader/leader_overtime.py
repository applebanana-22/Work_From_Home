import customtkinter as ctk
from database import Database
from tkinter import messagebox
from tkinter import ttk
from datetime import date, datetime, timedelta
from tkcalendar import Calendar
import threading

class DatePickerButton(ctk.CTkFrame):
    def __init__(self, master, initial_date=None, min_date=None, allow_past=True):
        super().__init__(master, fg_color="transparent")

        self._date = initial_date
        self._open = False
        self.allow_past = allow_past

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Custom.Calendar",
            background="#1A1A2E",
            foreground="white",
            headersbackground="#16213E",
            headersforeground="#4FC3F7",
            selectbackground="#3498DB",
            selectforeground="white",
            normalbackground="#1A1A2E",
            normalforeground="#CCCCCC",
            weekendbackground="#1A1A2E",
            weekendforeground="#F39C12",
            othermonthforeground="#555555",
            bordercolor="#2A2A4A",
            relief="flat"
        )

        self.btn = ctk.CTkButton(
            self,
            text=self._fmt(),
            width=170,
            height=36,
            corner_radius=10,
            fg_color="#1E2A3A",
            hover_color="#2C3E50",
            border_width=1,
            border_color="#3D5166",
            anchor="w",
            command=self.toggle
        )
        self.btn.pack()

        self.panel = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color="#141E2B",
            corner_radius=12,
            border_width=1,
            border_color="#2A3A4A"
        )

        today = datetime.today().date()
        
        # Set mindate based on allow_past parameter
        mindate = today if not allow_past else None

        self.cal = Calendar(
            self.panel,
            style="Custom.Calendar",
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            year=(self._date or today).year,
            month=(self._date or today).month,
            day=(self._date or today).day,
            mindate=mindate
        )
        self.cal.pack(padx=8, pady=8)

        self.cal.bind("<<CalendarSelected>>", self._select)

    def toggle(self):
        if self._open:
            self.panel.place_forget()
        else:
            self.panel.lift()
            self.panel.place(in_=self, x=0, y=self.btn.winfo_height() + 2)
        self._open = not self._open

    def _select(self, event):
        selected = self.cal.get_date()
        self._date = datetime.strptime(selected, "%Y-%m-%d").date()
        self.btn.configure(text=self._fmt())
        self.toggle()

    def _fmt(self):
        return f" 📅 {self._date.strftime('%Y-%m-%d')}" if self._date else " 📅 Select Date"

    def get_date(self):
        return self._date

    def clear(self):
        self._date = None
        self.btn.configure(text=" 📅 Select Date")

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

        # Bind mouse wheel to only scroll dropdown, not parent
        self.popup.bind("<MouseWheel>", self.on_dropdown_scroll)

        self.listbox = ctk.CTkScrollableFrame(self.popup, height=150)
        self.listbox.pack(fill="both", expand=True)

    def on_dropdown_scroll(self, event):
        """Handle scrolling within dropdown only"""
        # This prevents the parent frame from scrolling
        if hasattr(self.listbox, '_parent_canvas'):
            self.listbox._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"

    def show_dropdown(self, data):
        self.create_dropdown()

        for w in self.listbox.winfo_children():
            w.destroy()

        for item in data:
            btn = ctk.CTkButton(
                self.listbox,
                text=item,
                anchor="w",
                fg_color="transparent",
                hover_color="#333333",
                text_color="white",
                command=lambda v=item: self.select(v)
            )
            btn.pack(fill="x", padx=5, pady=2)
            
            # Bind mouse wheel to each button to prevent propagation
            btn.bind("<MouseWheel>", self.on_dropdown_scroll)

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

class LeaderOvertime(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user_data
        self.team_id = self.get_team_id()
        
        # Initialize member and project maps
        self.member_map = {}
        self.project_map = {}
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create pages container with original side margins
        self.pages = ctk.CTkFrame(self, fg_color="transparent")
        self.pages.grid(row=0, column=0, sticky="nsew", padx=120, pady=20)
        self.pages.grid_rowconfigure(0, weight=1)
        self.pages.grid_columnconfigure(0, weight=1)
        
        # Initialize all pages
        self.create_main_page()
        self.create_add_page()
        self.create_edit_page()
        
        # Show main page initially
        self.show_page("main")
        
        # Start auto-cancellation check
        self.check_overdue_requests()

    def get_team_id(self):
        self.db.cursor.execute("SELECT team_id FROM users WHERE id = %s", (self.user['id'],))
        return self.db.cursor.fetchone()['team_id']

    def check_overdue_requests(self):
        """Auto-cancel pending requests that are past their OT date"""
        try:
            today = date.today()
            
            # Update overdue pending requests to 'Cancelled'
            self.db.cursor.execute("""
                UPDATE overtime_requests 
                SET status = 'Cancelled' 
                WHERE status = 'Pending' 
                AND DATE(ot_date) < %s
            """, (today,))
            
            if self.db.cursor.rowcount > 0:
                self.db.conn.commit()
                print(f"Auto-cancelled {self.db.cursor.rowcount} overdue requests")
                # Refresh UI if on main page
                if hasattr(self, 'main_page') and self.main_page.winfo_viewable():
                    self.refresh_ui()
        except Exception as e:
            print(f"Error checking overdue requests: {e}")
        
        # Check again after 1 hour
        self.after(3600000, self.check_overdue_requests)

    def load_member_project_data(self):
        """Load member and project data for dropdowns"""
        # Get member data
        self.db.cursor.execute("""
            SELECT id, full_name FROM users
            WHERE team_id = %s AND role = 'member'
        """, (self.team_id,))
        self.member_map = {m['full_name']: m['id'] for m in self.db.cursor.fetchall()}
        self.member_names = list(self.member_map.keys())

        # Get project data
        self.db.cursor.execute("""
            SELECT id, project_name FROM projects
            WHERE team_id = %s
        """, (self.team_id,))
        self.project_map = {p['project_name']: p['id'] for p in self.db.cursor.fetchall()}
        self.project_names = list(self.project_map.keys())

    def show_page(self, page_name):
        """Show the specified page and hide others"""
        for page in [self.main_page, self.add_page, self.edit_page]:
            page.grid_forget()
            
        if page_name == "main":
            self.main_page.grid(row=0, column=0, sticky="nsew")
            self.check_overdue_requests()  # Check before refreshing
            self.refresh_ui()
        elif page_name == "add":
            self.add_page.grid(row=0, column=0, sticky="nsew")
            self.reset_add_form()
        elif page_name == "edit":
            self.edit_page.grid(row=0, column=0, sticky="nsew")

    def create_main_page(self):
        self.main_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.main_page.grid_rowconfigure(2, weight=1)  # List frame
        
        # Header with original spacing
        header = ctk.CTkFrame(self.main_page, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=15)

        ctk.CTkLabel(
            header,
            text="🕒 Overtime Management",
            font=("Arial", 22, "bold")
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="+ Add Overtime",
            fg_color="#2980B9",
            hover_color="#1F618D",
            height=40,
            command=lambda: self.show_page("add")
        ).pack(side="right")

        # Filter section with original design
        filter_frame = ctk.CTkFrame(
            self.main_page,
            fg_color="#1E1E1E",
            corner_radius=12,
            border_width=1,
            border_color="#2A2A2A"
        )
        filter_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=10)

        # Load member and project data
        self.load_member_project_data()
        
        # Filter widgets with original layout
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
            values=["All", "Pending", "Accepted", "Approved", "Rejected", "Cancelled"],
            width=100,
            height=35,
            fg_color="#2980B9",
            button_color="#1F618D"
        )
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=5)

        # Date filter - allow past dates (allow_past=True)
        self.date_filter = DatePickerButton(filter_frame, allow_past=True)
        self.date_filter.pack(side="left", padx=5)

        # Filter buttons with original design
        btn_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Search",
            fg_color="#2980B9",
            hover_color="#1F618D",
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

        # List frame with original design but improved height
        self.list_frame = ctk.CTkScrollableFrame(
            self.main_page,
            fg_color="#121212",
            corner_radius=12,
            border_width=1,
            border_color="#2A2A2A",
            height=400  # Fixed height
        )
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=0, pady=10)

    def create_add_page(self):
        self.add_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.add_page.grid_rowconfigure(1, weight=1)
        self.add_page.grid_columnconfigure(0, weight=1)
        
        # Back button
        back_btn = ctk.CTkButton(
            self.add_page,
            text="← Back to List",
            fg_color="transparent",
            hover_color="#2A2A2A",
            font=("Arial", 12),
            height=35,
            command=lambda: self.show_page("main")
        )
        back_btn.grid(row=0, column=0, sticky="nw", padx=20, pady=(10, 0))

        # Create scrollable container for the form
        self.add_scrollable = ctk.CTkScrollableFrame(
            self.add_page,
            fg_color="transparent"
        )
        self.add_scrollable.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.add_scrollable.grid_columnconfigure(0, weight=1)

        # Form frame inside scrollable container
        form_frame = ctk.CTkFrame(
            self.add_scrollable,
            fg_color="#1E1E1E",
            corner_radius=15,
            border_width=1,
            border_color="#2A2A2A"
        )
        form_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(2, weight=1)

        # Title
        title_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=30, pady=(25, 15))
        
        ctk.CTkLabel(
            title_frame,
            text="➕ Add New Overtime Request",
            font=("Arial", 20, "bold"),
            text_color="#4A90E2"
        ).pack()

        # Form content
        content_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        content_frame.grid(row=1, column=1, sticky="nsew", padx=30, pady=10)
        
        # Load data if not loaded
        if not hasattr(self, 'member_map'):
            self.load_member_project_data()
        
        # Member field
        ctk.CTkLabel(
            content_frame,
            text="👤 Member *",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(10, 5))
        
        self.member_cb = AutocompleteComboBox(content_frame, self.member_names, width=350, placeholder_text="Select or search member...")
        self.member_cb.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # Project field
        ctk.CTkLabel(
            content_frame,
            text="📁 Project *",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).grid(row=2, column=0, sticky="w", pady=(5, 5))
        
        self.project_cb = AutocompleteComboBox(content_frame, self.project_names, width=350, placeholder_text="Select or search project...")
        self.project_cb.grid(row=3, column=0, sticky="ew", pady=(0, 15))

        # Date field - DO NOT allow past dates (allow_past=False)
        ctk.CTkLabel(
            content_frame,
            text="📅 Date *",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).grid(row=4, column=0, sticky="w", pady=(5, 5))
        
        self.date_ent = DatePickerButton(content_frame, initial_date=date.today(), allow_past=False)
        self.date_ent.grid(row=5, column=0, sticky="ew", pady=(0, 15))

        # Hours field
        ctk.CTkLabel(
            content_frame,
            text="⏱️ Hours * (1-24 hours)",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).grid(row=6, column=0, sticky="w", pady=(5, 5))
        
        self.hours_ent = ctk.CTkEntry(content_frame, placeholder_text="e.g., 2.5, 4, 8", width=350, height=40)
        self.hours_ent.grid(row=7, column=0, sticky="ew", pady=(0, 15))

        # Reason field
        ctk.CTkLabel(
            content_frame,
            text="💬 Reason / Tasks *",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).grid(row=8, column=0, sticky="w", pady=(5, 5))
        
        self.reason_ent = ctk.CTkTextbox(content_frame, height=120, fg_color="#2A2A2A", border_width=1, border_color="#3D5166")
        self.reason_ent.grid(row=9, column=0, sticky="ew", pady=(0, 20))

        # Button frame
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=30, pady=(0, 25))
        
        button_container = ctk.CTkFrame(btn_frame, fg_color="transparent")
        button_container.pack()
        
        ctk.CTkButton(
            button_container,
            text="Cancel",
            fg_color="#7F8C8D",
            hover_color="#616A6B",
            height=40,
            width=120,
            font=("Arial", 13),
            command=lambda: self.show_page("main")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_container,
            text="Submit Request",
            fg_color="#27AE60",
            hover_color="#1E8449",
            height=40,
            width=150,
            font=("Arial", 13, "bold"),
            command=self.save_overtime
        ).pack(side="left", padx=10)

    def reset_add_form(self):
        """Reset the add form to default values"""
        self.member_cb.entry.delete(0, "end")
        self.project_cb.entry.delete(0, "end")
        self.date_ent.clear()
        self.date_ent._date = date.today()
        self.date_ent.btn.configure(text=f" 📅 {date.today().strftime('%Y-%m-%d')}")
        self.hours_ent.delete(0, "end")
        self.reason_ent.delete("1.0", "end")

    def save_overtime(self):
        """Save the new overtime request"""
        member_name = self.member_cb.get()
        project_name = self.project_cb.get()
        member_id = self.member_map.get(member_name)
        project_id = self.project_map.get(project_name)

        if not member_id:
            messagebox.showwarning("Validation Error", "Please select a valid member")
            return
        
        if not project_id:
            messagebox.showwarning("Validation Error", "Please select a valid project")
            return

        try:
            hours = float(self.hours_ent.get())
            if hours <= 0 or hours > 24:
                messagebox.showwarning("Validation Error", "Hours must be between 1 and 24")
                return
        except ValueError:
            messagebox.showwarning("Validation Error", "Please enter valid hours (e.g., 2.5, 4, 8)")
            return

        selected_date = self.date_ent.get_date()
        if not selected_date:
            messagebox.showwarning("Validation Error", "Please select a date")
            return
        
        # Check if date is in the past
        if selected_date < date.today():
            messagebox.showwarning("Validation Error", "Cannot select a past date for overtime request!")
            return

        ot_date = selected_date.strftime('%Y-%m-%d')
        reason = self.reason_ent.get("1.0", "end").strip()

        if not reason:
            messagebox.showwarning("Validation Error", "Please provide reason/tasks for overtime")
            return

        # Check for duplicate - only check for Pending and Accepted status (not Rejected or Cancelled)
        self.db.cursor.execute("""
            SELECT id FROM overtime_requests 
            WHERE member_id = %s 
            AND DATE(ot_date) = %s
            AND status IN ('Pending', 'Accepted')
        """, (member_id, ot_date))
        
        if self.db.cursor.fetchone():
            messagebox.showwarning("Duplicate Error", 
                f"Overtime request for {member_name} on {ot_date} already exists with status 'Pending' or 'Accepted'!\n\n"
                f"Please check existing requests before creating a new one.")
            return

        # Save to database
        self.db.cursor.execute("""
            INSERT INTO overtime_requests
            (member_id, project_id, ot_date, hours, reason, status)
            VALUES (%s, %s, %s, %s, %s, 'Pending')
        """, (member_id, project_id, ot_date, hours, reason))

        self.db.conn.commit()
        messagebox.showinfo("Success", f"✅ Overtime request for {member_name} has been submitted successfully!")
        self.show_page("main")

    def create_edit_page(self):
        self.edit_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.edit_page.grid_rowconfigure(1, weight=1)
        self.edit_page.grid_columnconfigure(0, weight=1)
        
        # Back button
        back_btn = ctk.CTkButton(
            self.edit_page,
            text="← Back to List",
            fg_color="transparent",
            hover_color="#2A2A2A",
            font=("Arial", 12),
            height=35,
            command=lambda: self.show_page("main")
        )
        back_btn.grid(row=0, column=0, sticky="nw", padx=20, pady=(10, 0))

        # Create scrollable container for the form
        self.edit_scrollable = ctk.CTkScrollableFrame(
            self.edit_page,
            fg_color="transparent"
        )
        self.edit_scrollable.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.edit_scrollable.grid_columnconfigure(0, weight=1)

        # Form frame inside scrollable container
        self.edit_form = ctk.CTkFrame(
            self.edit_scrollable,
            fg_color="#1E1E1E",
            corner_radius=15,
            border_width=1,
            border_color="#2A2A2A"
        )
        self.edit_form.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def load_edit_form(self, row):
        """Load edit form with request data"""
        for widget in self.edit_form.winfo_children():
            widget.destroy()

        self.edit_form.grid_columnconfigure(0, weight=1)
        self.edit_form.grid_columnconfigure(2, weight=1)

        # Title
        title_frame = ctk.CTkFrame(self.edit_form, fg_color="transparent")
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=30, pady=(25, 15))
        
        ctk.CTkLabel(
            title_frame,
            text="✏️ Edit Overtime Request",
            font=("Arial", 20, "bold"),
            text_color="#4A90E2"
        ).pack()

        # Content frame
        content_frame = ctk.CTkFrame(self.edit_form, fg_color="transparent")
        content_frame.grid(row=1, column=1, sticky="nsew", padx=30, pady=10)

        # Display read-only info with improved styling
        def create_info_row(label, value, row_num, icon=""):
            frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            frame.grid(row=row_num, column=0, sticky="ew", pady=8)
            
            ctk.CTkLabel(
                frame,
                text=f"{icon} {label}:",
                font=("Arial", 13, "bold"),
                text_color="#AAAAAA",
                width=120,
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                frame,
                text=value,
                font=("Arial", 13),
                anchor="w"
            ).pack(side="left", fill="x", expand=True, padx=(10, 0))

        create_info_row("Member", row['full_name'], 0, "👤")
        create_info_row("Project", row['project_name'], 1, "📁")
        create_info_row("Date", str(row['ot_date']), 2, "📅")
        
        # Status with color
        status_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        status_frame.grid(row=3, column=0, sticky="ew", pady=8)
        
        ctk.CTkLabel(
            status_frame,
            text="📊 Status:",
            font=("Arial", 13, "bold"),
            text_color="#AAAAAA",
            width=120,
            anchor="w"
        ).pack(side="left")
        
        status_color = {
            "Pending": "#F39C12",
            "Accepted": "#27AE60",
            "Approved": "#2ECC71",
            "Rejected": "#E74C3C",
            "Cancelled": "#95A5A6"
        }.get(row['status'], "#AAAAAA")
        
        ctk.CTkLabel(
            status_frame,
            text=row['status'],
            font=("Arial", 13, "bold"),
            text_color=status_color
        ).pack(side="left", padx=(10, 0))

        # Reason display
        ctk.CTkLabel(
            content_frame,
            text="💬 Original Reason:",
            font=("Arial", 13, "bold"),
            text_color="#AAAAAA"
        ).grid(row=4, column=0, sticky="w", pady=(15, 5))
        
        reason_display = ctk.CTkTextbox(
            content_frame,
            height=100,
            fg_color="#2A2A2A",
            state="disabled",
            border_width=1,
            border_color="#3D5166"
        )
        reason_display.grid(row=5, column=0, sticky="ew", pady=(0, 15))
        reason_display.insert("1.0", row['reason'] or "-")

        # Show rejection reason if exists
        if row.get('rejected_reason') and row['rejected_reason'].strip():
            ctk.CTkLabel(
                content_frame,
                text="❌ Rejection Reason:",
                font=("Arial", 13, "bold"),
                text_color="#E74C3C"
            ).grid(row=6, column=0, sticky="w", pady=(10, 5))
            
            reject_display = ctk.CTkTextbox(
                content_frame,
                height=80,
                fg_color="#2A1A1A",
                state="disabled",
                border_width=1,
                border_color="#5C3A3A"
            )
            reject_display.grid(row=7, column=0, sticky="ew", pady=(0, 15))
            reject_display.insert("1.0", row['rejected_reason'])

        # Only show edit fields if status is Pending and date is not past
        if row['status'] == 'Pending':
            # Check if date is past
            if row['ot_date'] < date.today():
                ctk.CTkLabel(
                    content_frame,
                    text="⚠️ This request is overdue and cannot be edited",
                    font=("Arial", 12, "bold"),
                    text_color="#E74C3C"
                ).grid(row=8, column=0, sticky="w", pady=(15, 10))
                
                # Cancel button only
                btn_frame = ctk.CTkFrame(self.edit_form, fg_color="transparent")
                btn_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=30, pady=(20, 25))
                
                ctk.CTkButton(
                    btn_frame,
                    text="Back to List",
                    fg_color="#2980B9",
                    hover_color="#1F618D",
                    height=40,
                    width=120,
                    font=("Arial", 13),
                    command=lambda: self.show_page("main")
                ).pack(pady=10)
            else:
                # Editable hours
                hours_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                hours_frame.grid(row=8, column=0, sticky="ew", pady=(15, 0))
                
                ctk.CTkLabel(
                    hours_frame,
                    text="⏱️ Update Hours:",
                    font=("Arial", 13, "bold"),
                    text_color="#AAAAAA"
                ).pack(side="left", padx=(0, 15))
                
                self.edit_hours = ctk.CTkEntry(hours_frame, width=120, height=40)
                self.edit_hours.pack(side="left")
                self.edit_hours.insert(0, str(row['hours']))

                # Save button
                btn_frame = ctk.CTkFrame(self.edit_form, fg_color="transparent")
                btn_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=30, pady=(20, 25))
                
                button_container = ctk.CTkFrame(btn_frame, fg_color="transparent")
                button_container.pack()
                
                ctk.CTkButton(
                    button_container,
                    text="Cancel",
                    fg_color="#7F8C8D",
                    hover_color="#616A6B",
                    height=40,
                    width=120,
                    font=("Arial", 13),
                    command=lambda: self.show_page("main")
                ).pack(side="left", padx=10)
                
                ctk.CTkButton(
                    button_container,
                    text="Save Changes",
                    fg_color="#2980B9",
                    hover_color="#1F618D",
                    height=40,
                    width=150,
                    font=("Arial", 13, "bold"),
                    command=lambda: self.update_overtime(row['id'])
                ).pack(side="left", padx=10)
        else:
            # Show message that request cannot be edited
            ctk.CTkLabel(
                content_frame,
                text="🔒 This request has been processed and cannot be edited",
                font=("Arial", 12, "italic"),
                text_color="#888888"
            ).grid(row=8, column=0, sticky="w", pady=(15, 10))
            
            # Cancel button only
            btn_frame = ctk.CTkFrame(self.edit_form, fg_color="transparent")
            btn_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=30, pady=(20, 25))
            
            ctk.CTkButton(
                btn_frame,
                text="Back to List",
                fg_color="#2980B9",
                hover_color="#1F618D",
                height=40,
                width=120,
                font=("Arial", 13),
                command=lambda: self.show_page("main")
            ).pack(pady=10)

    def update_overtime(self, ot_id):
        """Update the overtime record"""
        try:
            hours = float(self.edit_hours.get())
            if hours <= 0 or hours > 24:
                messagebox.showerror("Validation Error", "Hours must be between 1 and 24")
                return
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter valid hours (e.g., 2.5, 4, 8)")
            return

        self.db.cursor.execute("""
            UPDATE overtime_requests
            SET hours = %s
            WHERE id = %s AND status = 'Pending'
        """, (hours, ot_id))
        
        self.db.conn.commit()
        messagebox.showinfo("Success", f"✅ Overtime request has been updated successfully!")
        self.show_page("main")

    def clear_filters(self):
        """Clear all filter fields"""
        self.member_search.entry.delete(0, "end")
        self.project_search.entry.delete(0, "end")
        self.date_filter.clear()
        self.status_filter.set("All")
        self.refresh_ui()

    def refresh_ui(self):
        """Refresh the main list view"""
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        # Build query with filters
        query = """
            SELECT o.*, u.full_name, p.project_name
            FROM overtime_requests o
            JOIN users u ON o.member_id = u.id
            JOIN projects p ON o.project_id = p.id
            WHERE 1=1
        """
        params = []

        # Apply filters
        member = self.member_search.get().strip()
        if member:
            query += " AND u.full_name LIKE %s"
            params.append(f"%{member}%")

        project = self.project_search.get().strip()
        if project:
            query += " AND p.project_name LIKE %s"
            params.append(f"%{project}%")

        status = self.status_filter.get()
        if status != "All":
            query += " AND o.status = %s"
            params.append(status)

        date_val = self.date_filter.get_date()
        if date_val:
            query += " AND DATE(o.ot_date) = %s"
            params.append(date_val.strftime('%Y-%m-%d'))

        query += " ORDER BY o.created_at DESC"

        # Execute query
        self.db.cursor.execute(query, tuple(params))
        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(
                self.list_frame,
                text="📭 No overtime requests found",
                font=("Arial", 14),
                text_color="#888888"
            ).pack(pady=40)
            return

        # Display results with improved card design
        for row in rows:
            card = ctk.CTkFrame(
                self.list_frame,
                corner_radius=12,
                fg_color="#1E1E1E",
                border_width=1,
                border_color="#2A2A2A"
            )
            card.pack(fill="x", padx=15, pady=10)

            # Main content
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=15, pady=12)

            # Left side - info
            left = ctk.CTkFrame(content, fg_color="transparent")
            left.pack(side="left", fill="both", expand=True)

            # Top row: Name and date
            top_row = ctk.CTkFrame(left, fg_color="transparent")
            top_row.pack(fill="x", pady=(0, 8))
            
            ctk.CTkLabel(
                top_row,
                text=f"👤 {row['full_name']}",
                font=("Arial", 14, "bold")
            ).pack(side="left")
            
            ctk.CTkLabel(
                top_row,
                text=f"📅 {row['ot_date']}",
                font=("Arial", 11),
                text_color="#888888"
            ).pack(side="left", padx=10)

            # Project and hours
            middle_row = ctk.CTkFrame(left, fg_color="transparent")
            middle_row.pack(fill="x", pady=(0, 5))
            
            ctk.CTkLabel(
                middle_row,
                text=f"📁 {row['project_name']}",
                font=("Arial", 12)
            ).pack(side="left")
            
            ctk.CTkLabel(
                middle_row,
                text=f"⏱️ {row['hours']} hours",
                font=("Arial", 12),
                text_color="#AAAAAA"
            ).pack(side="left", padx=(15, 0))

            # Show warning if pending and overdue
            if row['status'] == 'Pending' and row['ot_date'] < date.today():
                warning_frame = ctk.CTkFrame(left, fg_color="#5C3A3A", corner_radius=6)
                warning_frame.pack(fill="x", pady=(5, 0))
                
                ctk.CTkLabel(
                    warning_frame,
                    text="⚠️ Overdue - This request will be auto-cancelled",
                    font=("Arial", 10, "bold"),
                    text_color="#E74C3C",
                    anchor="w"
                ).pack(fill="x", padx=8, pady=3)

            # Reason (if available)
            if row['reason'] and row['reason'].strip():
                reason_text = row['reason'][:100] + "..." if len(row['reason']) > 100 else row['reason']
                ctk.CTkLabel(
                    left,
                    text=f"💬 {reason_text}",
                    font=("Arial", 11),
                    text_color="#888888",
                    anchor="w"
                ).pack(fill="x", pady=(5, 0))

            # Show rejection reason if status is Rejected
            if row['status'] == 'Rejected' and row.get('rejected_reason') and row['rejected_reason'].strip():
                reject_text = row['rejected_reason'][:100] + "..." if len(row['rejected_reason']) > 100 else row['rejected_reason']
                reject_frame = ctk.CTkFrame(left, fg_color="#3D1E1E", corner_radius=6)
                reject_frame.pack(fill="x", pady=(5, 0))
                
                ctk.CTkLabel(
                    reject_frame,
                    text=f"❌ Rejected: {reject_text}",
                    font=("Arial", 10),
                    text_color="#E74C3C",
                    anchor="w"
                ).pack(fill="x", padx=8, pady=5)

            # Right side - Status Badge and Action Buttons
            right_section = ctk.CTkFrame(content, fg_color="transparent")
            right_section.pack(side="right", fill="y")

            # Modern Status Badge
            status_config = {
                "Pending": {"color": "#F39C12", "bg": "#3D2E1A", "icon": "⏳", "text": "Pending"},
                "Accepted": {"color": "#27AE60", "bg": "#1A3D2A", "icon": "✅", "text": "Accepted"},
                "Approved": {"color": "#2ECC71", "bg": "#1A4D2A", "icon": "✓", "text": "Approved"},
                "Rejected": {"color": "#E74C3C", "bg": "#4A1A1A", "icon": "✗", "text": "Rejected"},
                "Cancelled": {"color": "#95A5A6", "bg": "#2A3A3A", "icon": "⊗", "text": "Cancelled"}
            }
            
            config = status_config.get(row['status'], {"color": "#AAAAAA", "bg": "#2A2A2A", "icon": "•", "text": row['status']})
            
            # Create badge with icon and text
            badge_frame = ctk.CTkFrame(
                right_section,
                fg_color=config['bg'],
                corner_radius=15,
                height=30,
                width=100
            )
            badge_frame.pack(pady=(0, 10))
            badge_frame.pack_propagate(False)
            
            badge_content = ctk.CTkFrame(badge_frame, fg_color="transparent")
            badge_content.pack(expand=True, fill="both", padx=10, pady=5)
            
            ctk.CTkLabel(
                badge_content,
                text=f"{config['icon']} {config['text']}",
                font=("Arial", 11, "bold"),
                text_color=config['color']
            ).pack()

            # Action Buttons Frame
            action_frame = ctk.CTkFrame(right_section, fg_color="transparent")
            action_frame.pack()

            # Delete button for all statuses except Approved
            if row['status'] in ['Pending', 'Cancelled', 'Rejected', 'Accepted']:
                delete_btn = ctk.CTkButton(
                    action_frame,
                    text="Delete",
                    width=80,
                    height=32,
                    fg_color="#C0392B",
                    hover_color="#A93226",
                    font=("Arial", 11),
                    command=lambda id=row['id']: self.delete_request(id)
                )
                delete_btn.pack(pady=3)

            # Edit button only for Pending requests that are not overdue
            if row['status'] == 'Pending':
                if row['ot_date'] >= date.today():
                    edit_btn = ctk.CTkButton(
                        action_frame,
                        text="Edit",
                        width=80,
                        height=32,
                        fg_color="#2980B9",
                        hover_color="#1F618D",
                        font=("Arial", 11),
                        command=lambda r=row: self.edit_request(r)
                    )
                    edit_btn.pack(pady=3)
                else:
                    # Show warning for overdue pending
                    overdue_badge = ctk.CTkFrame(
                        action_frame,
                        fg_color="#4A1A1A",
                        corner_radius=12,
                        height=25,
                        width=80
                    )
                    overdue_badge.pack(pady=3)
                    overdue_badge.pack_propagate(False)
                    
                    ctk.CTkLabel(
                        overdue_badge,
                        text="⚠️ Overdue",
                        font=("Arial", 10, "bold"),
                        text_color="#E74C3C"
                    ).pack(expand=True)

    def edit_request(self, row):
        """Load the edit page with request data"""
        self.load_edit_form(row)
        self.show_page("edit")

    def delete_request(self, request_id):
        """Delete an overtime request"""
        # Get request status for confirmation message
        self.db.cursor.execute("SELECT status FROM overtime_requests WHERE id = %s", (request_id,))
        result = self.db.cursor.fetchone()
        
        if not result:
            messagebox.showerror("Error", "Request not found!")
            return
        
        status = result['status']
        
        # Custom confirmation message based on status
        if status == 'Pending':
            msg = "⚠️ Are you sure you want to delete this PENDING overtime request?\n\nThis action cannot be undone!"
        elif status in ['Accepted', 'Cancelled', 'Rejected']:
            msg = f"⚠️ Are you sure you want to delete this {status} overtime request?\n\nThis action cannot be undone!"
        else:
            msg = "⚠️ Are you sure you want to delete this overtime request?\n\nThis action cannot be undone!"
        
        if messagebox.askyesno("Confirm Delete", msg):
            self.db.cursor.execute("DELETE FROM overtime_requests WHERE id = %s", (request_id,))
            self.db.conn.commit()
            messagebox.showinfo("Success", "✅ Overtime request has been deleted successfully!")
            self.refresh_ui()