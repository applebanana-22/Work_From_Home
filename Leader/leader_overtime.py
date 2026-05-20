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
            width=120,
            height=28,
            corner_radius=10,
            fg_color=("#F9F9FA", "#343638"),       
            border_color=("#979DA2", "#565B5E"),   
            border_width=2.5,                        
            text_color=("gray10", "#DCE4EE"),      
            hover_color=("#E5E5E7", "#2B2D2F"),   
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

        self.popup = ctk.CTkToplevel(self.winfo_toplevel())
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
        
        # Automatic Theme Constants (Tuples) - like member_overtime.py
        self.COLOR_CARD_BG = ("#FFFFFF", "#1E1E1E")
        self.COLOR_BORDER = ("#DBDBDB", "#2C2C2C")
        self.COLOR_TEXT_MAIN = ("#1A1A2A", "#E8EDF2")
        self.COLOR_TEXT_SEC = ("#555555", "#AAB7C4")
        self.COLOR_TEXT_TER = ("#777777", "#718096")
        self.COLOR_SCROLL_BG = ("#F5F5F5", "#1A1A1A")
        self.COLOR_CONTAINER_BG = ("#F0F0F0", "#252525")
        
        # Initialize member and project maps
        self.member_map = {}
        self.project_map = {}
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create pages container with original side margins
        self.pages = ctk.CTkFrame(self, fg_color="transparent")
        self.pages.grid(row=0, column=0, sticky="nsew", padx=0, pady=20)
        self.pages.grid_rowconfigure(0, weight=1)
        self.pages.grid_columnconfigure(0, weight=1)
        
        # Initialize all pages
        self.create_main_page()
        self.create_add_page()
        self.create_edit_page()
        self.create_member_requests_page()
        
        # Show main page initially
        self.show_page("main")
        
        # Start auto-cancellation check
        self.check_overdue_requests()

    def _show_message(self, message, message_type="info", duration=3000):
        """
        Displays a transient message in the top-right corner of the master window.
        message_type: "info", "warning", "error", "success"
        """
        # Determine colors based on message_type
        if message_type == "error":
            bg_color = "#E74C3C"  # Red
            text_color = "white"
        elif message_type == "warning":
            bg_color = "#F39C12"  # Orange
            text_color = "white"
        elif message_type == "success":
            bg_color = "#27AE60"  # Green
            text_color = "white"
        else:  # info
            bg_color = "#3498DB"  # Blue
            text_color = "white"

        # Create a frame for the message
        message_frame = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color=bg_color,
            corner_radius=8
        )
        # Position in the top right corner, with some padding
        message_frame.place(relx=1.0, rely=0, x=-20, y=20, anchor="ne") 

        ctk.CTkLabel(
            message_frame,
            text=message,
            text_color=text_color,
            font=("Arial", 12, "bold"),
            wraplength=250 # Wrap text if too long
        ).pack(padx=15, pady=10)

        # Destroy the message after 'duration' milliseconds
        self.winfo_toplevel().after(duration, message_frame.destroy)

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
        for page in [self.main_page, self.add_page, self.edit_page, self.member_requests_page]:
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
        elif page_name == "member_requests":
            self.member_requests_page.grid(row=0, column=0, sticky="nsew")
            self.load_member_requests()

    def create_main_page(self):
        self.main_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.main_page.grid_rowconfigure(2, weight=1)  # List frame
        self.main_page.grid_columnconfigure(0, weight=1)
        
        # Header with original spacing
        header = ctk.CTkFrame(self.main_page, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=80, pady=20)

        ctk.CTkLabel(
            header,
            text="🕒 Overtime Management",
            font=("Arial", 22, "bold")
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="Request OT from member",
            fg_color="#2980B9",
            hover_color="#21618C",
            height=40,
            corner_radius=10,
            command=lambda: self.show_page("member_requests")
        ).pack(side="right", padx=(0, 10)) # Added padding to separate buttons

        ctk.CTkButton(
            header,
            text="+ Add Overtime",
            fg_color="#10B981",
            hover_color="#0E9769",
            height=40,
            corner_radius=10,
            command=lambda: self.show_page("add")
        ).pack(side="right")

        # Filter section with original design
        filter_frame = ctk.CTkFrame(
            self.main_page,
            fg_color=self.COLOR_CONTAINER_BG,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        filter_frame.grid(row=1, column=0, sticky="ew", padx=80, pady=(4, 10))

        # Load member and project data
        self.load_member_project_data()
        
        # Filter widgets with original layout
        # --- Member Search Dropdown ---
        self.member_search = ctk.CTkComboBox(
            filter_frame,
            values=self.member_names,
            width=120,              
            corner_radius=10,
            command=lambda v: self.load_data() 
        )
        self.member_search.set("Member...") # Acts as placeholder
        self.member_search.pack(side="left", padx=(10, 5), pady=15)

        self.project_search = ctk.CTkComboBox(
            filter_frame,
            values=self.project_names,
            width=120,             
            corner_radius=10,
            command=lambda v: self.load_data() 
        )
        self.project_search.set("Project...") # Acts as placeholder
        self.project_search.pack(side="left", padx=(10, 5), pady=15)

        self.status_filter = ctk.CTkComboBox(
            filter_frame,
            values=["All", "Pending", "Accepted", "Rejected", "Cancelled"],
            width=100,
            corner_radius=10,
            command=lambda v: self.load_data()
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
            text="🔍 Filter",
            width=80,
            height=32,            # Matched height for alignment
            corner_radius=14,      # Matched corner radius
            font=("Arial", 12, "bold"),
            fg_color="#2471A3",
            hover_color="#1A5276",
            command=self.refresh_ui
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="✖ Clear",
            width=80,
            height=32,
            corner_radius=14,
            font=("Arial", 12, "bold"),
            fg_color="#566573",
            hover_color="#424949",
            command=self.clear_filters
        ).pack(side="right", padx=5)

        # List frame with original design but improved height
        self.list_frame = ctk.CTkScrollableFrame(
            self.main_page,
            fg_color=self.COLOR_SCROLL_BG,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDER,
            height=400  # Fixed height
        )
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=80, pady=(0, 10))

    def create_add_page(self):
        self.add_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.add_page.grid_rowconfigure(1, weight=1)
        self.add_page.grid_columnconfigure(0, weight=1)
        
        # Back button
        back_btn = ctk.CTkButton(
            self.add_page,
            text="← Back to List",
            text_color=("black", "white"),
            width=100,
            fg_color=("#DBDBDB", "#333333"), 
            # hover_color="#2A2A2A",
            font=("Arial", 12),
            height=35,
            command=lambda: self.show_page("main")
        )
        back_btn.grid(row=0, column=0, sticky="nw", padx=80, pady=(10, 0))
        
        # Create scrollable container for the form
        self.add_scrollable = ctk.CTkScrollableFrame(
            self.add_page,
            fg_color="transparent"
        )
        self.add_scrollable.grid(row=1, column=0, sticky="nsew", padx=80, pady=10)
        self.add_scrollable.grid_columnconfigure(0, weight=1)

        # Form frame inside scrollable container
        form_frame = ctk.CTkFrame(
            self.add_scrollable,
            fg_color=self.COLOR_CONTAINER_BG,
            corner_radius=15,
            border_width=1,
            border_color=self.COLOR_BORDER
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
        
        self.member_cb = ctk.CTkComboBox(
            content_frame,
            values=self.member_names,
            width=350,
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            # button_color="#1E2A3A",
            # button_hover_color="#2C3E50"
        )
        self.member_cb.set("Select member...")
        self.member_cb.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # Project field
        ctk.CTkLabel(
            content_frame,
            text="📁 Project *",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).grid(row=2, column=0, sticky="w", pady=(5, 5))
        
        self.project_cb = ctk.CTkComboBox(
            content_frame,
            values=self.project_names,
            width=350,
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            # button_color="#1E2A3A",
            # button_hover_color="#2C3E50"
        )
        self.project_cb.set("Select project...")
        self.project_cb.grid(row=3, column=0, sticky="ew", pady=(0, 15))

        # Date field - DO NOT allow past dates (allow_past=False)
        ctk.CTkLabel(
            content_frame,
            text="📅 Date *",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).grid(row=4, column=0, sticky="w", pady=(5, 5))
        
        # self.date_ent = DatePickerButton(content_frame, initial_date=date.today(), allow_past=False)
        # self.date_ent.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self.date_ent = DatePickerButton(
            content_frame,              # Using filter_frame for horizontal alignment
            initial_date=date.today(), 
            allow_past=False
        )

        # Align to the left with padding to separate it from the previous widget
        self.date_ent.grid(row=5, column=0, sticky="w", padx=10, pady=(0, 15))

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
        
        self.reason_ent = ctk.CTkTextbox(content_frame, height=120, fg_color=self.COLOR_CARD_BG, border_width=1, border_color=self.COLOR_BORDER)
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
        if hasattr(self.member_cb, 'entry'):
            self.member_cb.entry.delete(0, "end")
        else:
            self.member_cb.set("Select member...")

        if hasattr(self.project_cb, 'entry'):
            self.project_cb.entry.delete(0, "end")
        else:
            self.project_cb.set("Select project...")

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

        # Reset all borders to default before validation
        default_border_color = self.COLOR_BORDER
        self.member_cb.configure(border_color=default_border_color)
        self.project_cb.configure(border_color=default_border_color)
        self.date_ent.btn.configure(border_color=default_border_color)
        self.hours_ent.configure(border_color=default_border_color)
        self.reason_ent.configure(border_color=default_border_color)

        if not member_id:
            self._show_message("Please select a valid member", "error")
            self.member_cb.configure(border_color="red")
            return
        
        if not project_id:
            self._show_message("Please select a valid project", "error")
            self.project_cb.configure(border_color="red")
            return

        try:
            hours = float(self.hours_ent.get())
            if hours <= 0 or hours > 24:
                self._show_message("Hours must be between 1 and 24", "error")
                self.hours_ent.configure(border_color="red")
                return
        except ValueError:
            self._show_message("Please enter valid hours (e.g., 2.5, 4, 8)", "error")
            self.hours_ent.configure(border_color="red")
            return

        selected_date = self.date_ent.get_date()
        if not selected_date:
            self._show_message("Please select a date", "error")
            self.date_ent.btn.configure(border_color="red")
            return
        
        # Check if date is in the past
        if selected_date < date.today():
            self._show_message("Cannot select a past date for overtime request!", "error")
            self.date_ent.btn.configure(border_color="red")
            return

        ot_date = selected_date.strftime('%Y-%m-%d')
        reason = self.reason_ent.get("1.0", "end").strip()

        if not reason:
            self._show_message("Please provide reason/tasks for overtime", "error")
            self.reason_ent.configure(border_color="red")
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

        # THIS PART TRIGGERS THE BADGE
        msg = f"New Overtime Request for {ot_date}."
        self.db.cursor.execute("""
            INSERT INTO notifications (user_id, message, is_read, created_at) 
            VALUES (%s, %s, 0, NOW())""", (member_id, msg))

        try:
            self.db.conn.commit()
            self._show_message(f"Overtime request for {member_name} has been submitted successfully!", "success")
            self.show_page("main")
        except Exception as e:
            self.db.conn.rollback()
            self._show_message(f"System Error: {e}", "error")

    def create_member_requests_page(self):
        # Placeholder for the new page to display member overtime requests
        self.member_requests_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.member_requests_page.grid_rowconfigure(1, weight=1)
        self.member_requests_page.grid_columnconfigure(0, weight=1)

        # Create a header frame for the back button and title
        header_frame = ctk.CTkFrame(self.member_requests_page, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=80, pady=(10, 20))
        header_frame.grid_columnconfigure(1, weight=1) # Allow the title column to expand

        # Back button
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back to List",
            text_color=("black", "white"),
            width=100,
            fg_color=("#DBDBDB", "#333333"),
            font=("Arial", 12),
            height=35,
            command=lambda: self.show_page("main")
        )
        back_btn.grid(row=0, column=0, sticky="w")

        # Title
        ctk.CTkLabel(
            header_frame,
            text="Member Overtime Requests",
            font=("Arial", 22, "bold")
        ).grid(row=0, column=1, sticky="w", padx=(20, 0))

        self.member_requests_list_frame = ctk.CTkScrollableFrame(
            self.member_requests_page,
            fg_color=self.COLOR_SCROLL_BG,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDER,
            height=400
        )
        self.member_requests_list_frame.grid(row=1, column=0, sticky="nsew", padx=80, pady=(0, 10))

        self.load_member_requests() # This method will fetch and display the requests

    def load_member_requests(self):
        """Load and display overtime requests from members."""
        for widget in self.member_requests_list_frame.winfo_children():
            widget.destroy()

        # Query to get all pending overtime requests from members in the leader's team
        query = """
            SELECT o.*, u.full_name, p.project_name
            FROM overtime_requests o
            JOIN users u ON o.member_id = u.id
            JOIN projects p ON o.project_id = p.id
            WHERE u.team_id = %s AND o.status = 'Pending'
            ORDER BY o.created_at DESC
        """
        self.db.cursor.execute(query, (self.team_id,))
        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(
                self.member_requests_list_frame,
                text="📭 No pending overtime requests from members.",
                font=("Arial", 14),
                text_color="#888888"
            ).pack(pady=40)
            return

        for row in rows:
            self._create_member_request_card(row)

    def _create_member_request_card(self, row):
        """Creates a card for a member's overtime request."""
        card = ctk.CTkFrame(
            self.member_requests_list_frame,
            corner_radius=12,
            fg_color=self.COLOR_CONTAINER_BG,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        card.pack(fill="x", padx=15, pady=10)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=12)

        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)

        # Top row: Member Name and Date
        top_row = ctk.CTkFrame(left, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            top_row,
            text=f"👤 {row['full_name']} 📅 {row['ot_date'].strftime('%Y-%m-%d')}",
            font=("Arial", 14, "bold"),
            text_color=self.COLOR_TEXT_MAIN
        ).pack(side="left", anchor="w")

        # Middle row: Project and Hours
        middle_row = ctk.CTkFrame(left, fg_color="transparent")
        middle_row.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            middle_row,
            text=f"📁 {row['project_name']} ⏱️ {row['hours']:.2f} hours",
            font=("Arial", 12),
            text_color=self.COLOR_TEXT_SEC
        ).pack(side="left", anchor="w")

        # Reason/Tasks
        if row['reason']:
            ctk.CTkLabel(
                left,
                text=f"💬 {row['reason']}",
                font=("Arial", 11, "italic"),
                text_color=self.COLOR_TEXT_TER,
                wraplength=400,
                justify="left"
            ).pack(fill="x", anchor="w", pady=(0, 5))

        # Right section for status badge and action buttons
        right_section = ctk.CTkFrame(content, fg_color="transparent")
        right_section.pack(side="right", fill="y")

        # Status Badge
        status_config = {
            'Pending': {'text': 'Pending', 'color': '#F39C12', 'icon': '⏳'},
            'Accepted': {'text': 'Accepted', 'color': '#2ECC71', 'icon': '✅'},
            'Rejected': {'text': 'Rejected', 'color': '#E74C3C', 'icon': '❌'},
            'Cancelled': {'text': 'Cancelled', 'color': '#7F8C8D', 'icon': '🚫'}
        }
        config = status_config.get(row['status'], {'text': row['status'], 'color': '#888888', 'icon': '❓'})

        badge_content = ctk.CTkFrame(
            right_section,
            fg_color=self.COLOR_CARD_BG,
            corner_radius=12,
            height=25,
            width=80
        )
        badge_content.pack(pady=3)
        badge_content.pack_propagate(False)

        ctk.CTkLabel(
            badge_content,
            text=f"{config['icon']} {config['text']}",
            font=("Arial", 11, "bold"),
            text_color=config['color']
        ).pack()

        # Action Buttons Frame
        action_frame = ctk.CTkFrame(right_section, fg_color="transparent")
        action_frame.pack()

        # Approve Button (only for Pending requests)
        if row['status'] == 'Pending':
            approve_btn = ctk.CTkButton(
                action_frame,
                text="Approve",
                width=60,
                height=30,
                corner_radius=14,
                fg_color="#2ECC71",
                hover_color="#27AE60",
                font=("Arial", 11),
                command=lambda id=row['id']: self._update_member_request_status(id, 'Accepted')
            )
            approve_btn.pack(pady=3)

            # Reject Button (only for Pending requests)
            reject_btn = ctk.CTkButton(
                action_frame,
                text="Reject",
                width=60,
                height=30,
                corner_radius=14,
                fg_color="#E74C3C",
                hover_color="#C0392B",
                font=("Arial", 11),
                command=lambda id=row['id']: self._show_reject_dialog(id)
            )
            reject_btn.pack(pady=3)

    def _update_member_request_status(self, request_id, new_status, reject_reason=None):
        """Updates the status of a member's overtime request."""
        try:
            if new_status == 'Rejected' and reject_reason:
                self.db.cursor.execute("""
                    UPDATE overtime_requests
                    SET status = %s, rejected_reason = %s
                    WHERE id = %s
                """, (new_status, reject_reason, request_id))
            else:
                self.db.cursor.execute("""
                    UPDATE overtime_requests
                    SET status = %s
                    WHERE id = %s
                """, (new_status, request_id))

            # Notify the member
            self.db.cursor.execute("SELECT member_id, ot_date FROM overtime_requests WHERE id = %s", (request_id,))
            request_info = self.db.cursor.fetchone()
            if request_info:
                member_id = request_info['member_id']
                ot_date = request_info['ot_date'].strftime('%Y-%m-%d')
                if new_status == 'Accepted':
                    msg = f"Your overtime request for {ot_date} has been Accepted."
                elif new_status == 'Rejected':
                    msg = f"Your overtime request for {ot_date} has been Rejected. Reason: {reject_reason}"
                else:
                    msg = f"Your overtime request for {ot_date} status changed to {new_status}."

                self.db.cursor.execute("""
                    INSERT INTO notifications (user_id, message, is_read, created_at)
                    VALUES (%s, %s, 0, NOW())
                """, (member_id, msg))

            self.db.conn.commit()
            self._show_message(f"Request {new_status} successfully!", "success")
            self.load_member_requests() # Refresh the list
        except Exception as e:
            self.db.conn.rollback()
            self._show_message(f"System Error: {e}", "error")

    def _show_reject_dialog(self, request_id):
        """Shows a dialog for the leader to enter a rejection reason."""
        dialog = ctk.CTkInputDialog(
            text="Enter reason for rejection:",
            title="Reject Overtime Request"
        )
        reason = dialog.get_input()
        if reason:
            self._update_member_request_status(request_id, 'Rejected', reason)
        else:
            self._show_message("Rejection cancelled or no reason provided.", "info")

    def create_edit_page(self):
        self.edit_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.edit_page.grid_rowconfigure(1, weight=1)
        self.edit_page.grid_columnconfigure(0, weight=1)
        
        # Back button
        back_btn = ctk.CTkButton(
            self.edit_page,
            text="← Back to List",
            text_color=("black", "white"),
            width=100,
            fg_color=("#DBDBDB", "#333333"), 
            # hover_color="#2A2A2A",
            font=("Arial", 12),
            height=35,
            command=lambda: self.show_page("main")
        )
        back_btn.grid(row=0, column=0, sticky="nw", padx=80, pady=(10, 0))

        # Create scrollable container for the form
        self.edit_scrollable = ctk.CTkScrollableFrame(
            self.edit_page,
            fg_color="transparent"
        )
        self.edit_scrollable.grid(row=1, column=0, sticky="nsew", padx=80, pady=10)
        self.edit_scrollable.grid_columnconfigure(0, weight=1)

        # Form frame inside scrollable container
        self.edit_form = ctk.CTkFrame(
            self.edit_scrollable,
            fg_color=self.COLOR_CONTAINER_BG,
            corner_radius=15,
            border_width=1,
            border_color=self.COLOR_BORDER
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
            fg_color=self.COLOR_CARD_BG,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        reason_display.grid(row=5, column=0, sticky="ew", pady=(0, 15))
        reason_display.insert("1.0", row['reason'] or "-")
        reason_display.configure(state="disabled")

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
                fg_color=self.COLOR_TEXT_SEC,
                border_width=1,
                border_color=self.COLOR_BORDER
            )
            reject_display.grid(row=7, column=0, sticky="ew", pady=(0, 15))
            reject_display.insert("1.0", row['rejected_reason'])
            reject_display.configure(state="disabled")

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
            
            
        # ctk.CTkButton(
        #     btn_frame,
        #     text="← Back to List",
        #     width=80,
        #     fg_color=("#DBDBDB", "#333333"),   # light/dark adaptive colors
        #     text_color=("black", "white"),     # adaptive text colors
        #     hover_color="#616A6B",             # subtle hover effect
        #     font=("Arial", 13),
        #     command=lambda: self.show_page("main")
        # ).pack(side="left", padx=10, pady=10)


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

        try:
            self.db.cursor.execute("""
                UPDATE overtime_requests
                SET hours = %s
                WHERE id = %s AND status = 'Pending'
            """, (hours, ot_id))
            
            self.db.conn.commit()
            self._show_message("Overtime request updated successfully!", "success")
            self.show_page("main")
        except Exception as e:
            self.db.conn.rollback()
            self._show_message(f"System Error: {e}", "error")

    def clear_filters(self):
        """Clear all filter fields"""
        self.member_search.set("Member...") 
        self.project_search.set("Project...")
        if hasattr(self.date_filter, 'clear'):
            self.date_filter.clear()
        else:
            self.date_filter.delete(0, "end")
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
        if member and member != "Member...":
            query += " AND u.full_name LIKE %s"
            params.append(f"%{member}%")

        project = self.project_search.get().strip()
        if project and project != "Project...":
            query += " AND p.project_name LIKE %s"
            params.append(f"%{project}%")

        status = self.status_filter.get()
        if status and status not in ["All", "Status..."]:
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
                fg_color=self.COLOR_CONTAINER_BG,
                border_width=1,
                border_color=self.COLOR_BORDER
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
                font=("Arial", 11, "bold"),
                text_color=("#000000", "#888888")
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
                font=("Arial", 12, "bold"),
                text_color=("#000000", "#AAAAAA")
            ).pack(side="left", padx=(15, 0))

            # Show warning if pending and overdue
            if row['status'] == 'Pending' and row['ot_date'] < date.today():
                warning_frame = ctk.CTkFrame(left, fg_color=self.COLOR_TEXT_SEC, corner_radius=6)
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
                reject_frame = ctk.CTkFrame(left, fg_color=self.COLOR_TEXT_TER, corner_radius=6)
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
                "Accepted": {"color": "#27AE60", "bg": "#1A3D2A", "icon": "✓", "text": "Accepted"},
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
                    width=60,
                    height=30,
                    corner_radius=14,
                    fg_color="#E74C3C",
                    hover_color="#C0392B",
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
                        width=60,
                        height=30,
                        corner_radius=14,
                        fg_color="#F39C12",
                        hover_color="#D68910",
                        font=("Arial", 11),
                        command=lambda r=row: self.edit_request(r)
                    )
                    edit_btn.pack(pady=3)
                else:
                    # Show warning for overdue pending
                    overdue_badge = ctk.CTkFrame(
                        action_frame,
                        fg_color=self.COLOR_TEXT_SEC,
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
            self._show_message("Request not found!", "error")
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
            try:
                self.db.cursor.execute("DELETE FROM overtime_requests WHERE id = %s", (request_id,))
                self.db.conn.commit()
                self._show_message("Overtime request deleted successfully!", "success")
                self.refresh_ui()
            except Exception as e:
                self.db.conn.rollback()
                self._show_message(f"System Error: {e}", "error")