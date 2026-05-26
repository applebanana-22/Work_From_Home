import customtkinter as ctk
from database import Database
from tkinter import messagebox, simpledialog
from datetime import date, datetime, timedelta
from tkcalendar import Calendar
import threading
from tkinter import ttk

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

    def set_date(self, d):
        self._date = d
        self.cal.selection_set(d)
        self.btn.configure(text=self._fmt())

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

class MemberOvertime(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user  # Login ဝင်ထားသော Member data
        self._is_destroyed = False
        self._after_id = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Automatic Theme Constants (Tuples) - matching member_report.py
        self.COLOR_CARD_BG = ("#FFFFFF", "#1E1E1E")
        self.COLOR_BORDER = ("#DBDBDB", "#2C2C2C")
        self.COLOR_TEXT_MAIN = ("#1A1A2A", "#E8EDF2")
        self.COLOR_TEXT_SEC = ("#555555", "#AAB7C4")
        self.COLOR_TEXT_TER = ("#777777", "#718096")
        self.COLOR_SCROLL_BG = ("#F5F5F5", "#1A1A1A")
        self.COLOR_CONTAINER_BG = ("#F0F0F0", "#252525")

        self.leader_names = []
        self.project_names = []
        self._load_initial_data()

        # Initialize page structure
        self.pages = ctk.CTkFrame(self, fg_color="transparent")
        self.pages.grid(row=0, column=0, sticky="nsew")
        self.pages.grid_rowconfigure(0, weight=1)
        self.pages.grid_columnconfigure(0, weight=1)

        # Initialize all pages
        self.create_main_page()
        self.create_add_page()
        self.create_edit_page()
        
        # Show main page initially
        self.show_page("main")
        
        # Initial data load
        self.refresh_all_data()

        # Start background check for status updates
        self.auto_refresh()

    def _load_initial_data(self):
        """Load leader and project names for the dropdowns."""
        self.leader_names = self._get_leader_names()
        self.project_names = self._get_project_names()

    def _get_project_names(self):
        try:
            self.db.cursor.execute("SELECT project_name FROM projects WHERE team_id = %s ORDER BY project_name", (self.user['team_id'],))
            return [row['project_name'] for row in self.db.cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching project names: {e}")
            return []

    def _get_member_names(self):
        try:
            self.db.cursor.execute("SELECT full_name FROM users WHERE role = 'member' AND team_id = %s ORDER BY full_name", (self.user['team_id'],))
            member_names = [row['full_name'] for row in self.db.cursor.fetchall()]
            print(f"Fetched member names: {member_names}")
            return member_names
        except Exception as e:
            print(f"Error fetching member names: {e}")
            return []

    def _get_user_id_by_full_name(self, full_name):
        try:
            self.db.cursor.execute("SELECT id FROM users WHERE full_name = %s AND team_id = %s", (full_name, self.user['team_id']))
            result = self.db.cursor.fetchone()
            print(f"Fetched user ID for {full_name}: {result}")
            return result['id'] if result else None
        except Exception as e:
            print(f"Error fetching user ID for {full_name}: {e}")
            return None

    def _get_leader_names(self):
        try:
            self.db.cursor.execute("SELECT full_name FROM users WHERE role = 'leader' AND team_id = %s ORDER BY full_name", (self.user['team_id'],))
            leader_names = [row['full_name'] for row in self.db.cursor.fetchall()]
            print(f"Fetched leader names: {leader_names}")
            return leader_names
        except Exception as e:
            print(f"Error fetching leader names: {e}")
            return []

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
        self.master.after(duration, message_frame.destroy)

    def show_page(self, page_name):
        """Show the specified page and hide others"""
        # Hide all pages
        for page in self.pages.winfo_children():
            page.grid_forget()
            
        if page_name == "main":
            self.main_page.grid(row=0, column=0, sticky="nsew")
            self.segmented_btn.set("📋 Pending Requests") # Reset to default tab
            self.show_pending_tab() # Ensure the correct tab is shown
            self.refresh_all_data()
        elif page_name == "add":
            self.add_page.grid(row=0, column=0, sticky="nsew")
            self._refresh_add_form_data() # Refresh dropdowns
            # self.reset_add_form() # We will create this later
        elif page_name == "edit":
            self.edit_page.grid(row=0, column=0, sticky="nsew")

    def create_main_page(self):
        self.main_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.main_page.grid_rowconfigure(2, weight=1) # Main content area
        self.main_page.grid_columnconfigure(0, weight=1)

        # --- Header ---
        header = ctk.CTkFrame(self.main_page, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=60, pady=20)
        
        ctk.CTkLabel(
            header, 
            text="Overtime Management", 
            font=("Arial", 20, "bold"),
            text_color=self.COLOR_TEXT_MAIN
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="+ Add Overtime",
            fg_color="#10B981",
            hover_color="#0E9769",
            height=40,
            corner_radius=10,
            font=("Arial", 12, "bold"),
            command=lambda: self.show_page("add")
        ).pack(side="right")

        # --- Segmented Button for Tab Selection ---
        self.segmented_btn = ctk.CTkSegmentedButton(
            self.main_page,
            values=["📋 Pending Requests", "📜 History"],
            command=self.on_tab_change,
            font=("Arial", 13, "bold"),
            fg_color=self.COLOR_CONTAINER_BG,
            selected_color=("#3498DB", "#1F538D"),
            unselected_color=self.COLOR_CARD_BG,
            text_color=self.COLOR_TEXT_MAIN,
            corner_radius=12,
            height=40
        )
        self.segmented_btn.grid(row=1, column=0, sticky="ew", padx=60, pady=10)
        self.segmented_btn.set("📋 Pending Requests")  # Set default tab

        # --- Badge for History Tab ---
        self.history_badge = ctk.CTkLabel(
            self.segmented_btn,
            text="",
            font=("Arial", 10, "bold"),
            fg_color="#E74C3C",
            text_color="white",
            width=20, height=20,
            corner_radius=10
        )
        self.history_badge.place_forget() # Hide initially

        # --- Content Frame (changes based on selected tab) ---
        self.content_frame = ctk.CTkFrame(self.main_page, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=60, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Create scrollable frames for both tabs
        self.pending_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color=self.COLOR_SCROLL_BG,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        
        self.history_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color=self.COLOR_SCROLL_BG,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDER
        )

    def create_add_page(self):
        self.add_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.add_page.grid_rowconfigure(1, weight=1)
        self.add_page.grid_columnconfigure(0, weight=1)

        # --- Back Button ---
        back_btn = ctk.CTkButton(
            self.add_page,
            text="← Back",
            text_color=("black", "white"),
            width=80,
            fg_color=("#DBDBDB", "#333333"),
            hover_color=("#CFCFCF", "#444444"),
            corner_radius=8,
            height=36,
            command=lambda: self.show_page("main")
        )
        back_btn.grid(row=0, column=0, sticky="nw", padx=60, pady=(10, 0))

        # --- Scrollable Form Container ---
        add_scrollable = ctk.CTkScrollableFrame(self.add_page, fg_color="transparent")
        add_scrollable.grid(row=1, column=0, sticky="nsew", padx=60, pady=10)
        add_scrollable.grid_columnconfigure(0, weight=1)

        # --- Form Frame ---
        form_frame = ctk.CTkFrame(
            add_scrollable,
            fg_color=self.COLOR_CONTAINER_BG,
            corner_radius=15,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        form_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=1)

        # --- Title ---
        title_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=30, pady=(25, 15))
        ctk.CTkLabel(
            title_frame,
            text="➕ Add New Overtime Request",
            font=("Arial", 20, "bold"),
            text_color="#4A90E2"
        ).pack()

        # --- Form Content ---
        content_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        content_frame.grid(row=1, column=1, sticky="nsew", padx=30, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        # --- Leader ---
        leader_label_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        leader_label_frame.grid(row=0, column=0, sticky="w", pady=(10, 5), padx=(0, 10))
        ctk.CTkLabel(leader_label_frame, text="👤 Leader", font=("Arial", 14, "bold"), anchor="w").pack(side="left")
        ctk.CTkLabel(leader_label_frame, text=" *", text_color="#EF4444", font=("Arial", 14, "bold")).pack(side="left")
        self.add_leader_combo = ctk.CTkComboBox(
            content_frame,
            values=self.leader_names,
            width=300,
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            state="readonly",
            border_color=self.COLOR_BORDER,
            button_color=self.COLOR_BORDER,
            border_width=1
        )
        self.add_leader_combo.grid(row=1, column=0, sticky="ew", pady=(0, 0), padx=(0, 10))
        self.leader_error_label = ctk.CTkLabel(content_frame, text="", text_color="#EF4444")
        self.leader_error_label.grid(row=2, column=0, sticky="w", pady=(0, 10), padx=(0, 10))

        # --- Project ---
        project_label_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        project_label_frame.grid(row=0, column=1, sticky="w", pady=(10, 5))
        ctk.CTkLabel(project_label_frame, text="📁 Project", font=("Arial", 14, "bold"), anchor="w").pack(side="left")
        ctk.CTkLabel(project_label_frame, text=" *", text_color="#EF4444", font=("Arial", 14, "bold")).pack(side="left")
        self.add_project_combo = ctk.CTkComboBox(
            content_frame,
            values=self.project_names,
            width=300,
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            state="readonly",
            border_color=self.COLOR_BORDER,
            button_color=self.COLOR_BORDER,
            border_width=1
        )
        self.add_project_combo.grid(row=1, column=1, sticky="ew", pady=(0, 0))
        self.project_error_label = ctk.CTkLabel(content_frame, text="", text_color="#EF4444")
        self.project_error_label.grid(row=2, column=1, sticky="w", pady=(0, 10))

        # --- Date ---
        date_label_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        date_label_frame.grid(row=3, column=0, sticky="w", pady=(5, 5), padx=(0, 10))
        ctk.CTkLabel(date_label_frame, text="📅 Date", font=("Arial", 14, "bold"), anchor="w").pack(side="left")
        ctk.CTkLabel(date_label_frame, text=" *", text_color="#EF4444", font=("Arial", 14, "bold")).pack(side="left")
        self.add_date_picker = DatePickerButton(content_frame, initial_date=None, allow_past=False)
        self.add_date_picker.grid(row=4, column=0, sticky="w", pady=(0, 0), padx=(0, 10))
        self.date_error_label = ctk.CTkLabel(content_frame, text="", text_color="#EF4444")
        self.date_error_label.grid(row=5, column=0, sticky="w", pady=(0, 10), padx=(0, 10))

        # --- Hours ---
        hours_label_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        hours_label_frame.grid(row=3, column=1, sticky="w", pady=(5, 5))
        ctk.CTkLabel(hours_label_frame, text="⏱️ Hours", font=("Arial", 14, "bold"), anchor="w").pack(side="left")
        ctk.CTkLabel(hours_label_frame, text=" *", text_color="#EF4444", font=("Arial", 14, "bold")).pack(side="left")
        ctk.CTkLabel(hours_label_frame, text=" (1-8 hours)", font=("Arial", 12)).pack(side="left")
        self.add_hours_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="e.g., 2.5",
            width=300,
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            border_color=self.COLOR_BORDER,
            border_width=1
        )
        self.add_hours_entry.grid(row=4, column=1, sticky="ew", pady=(0, 8))
        self.hours_error_label = ctk.CTkLabel(content_frame, text="", text_color="#EF4444")
        self.hours_error_label.grid(row=5, column=1, sticky="w", pady=(0, 10))

        # --- Reason ---
        reason_label_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        reason_label_frame.grid(row=6, column=0, columnspan=2, sticky="w", pady=(5, 5))
        ctk.CTkLabel(reason_label_frame, text="📝 Reason / Tasks", font=("Arial", 14, "bold"), anchor="w").pack(side="left")
        ctk.CTkLabel(reason_label_frame, text=" *", text_color="#EF4444", font=("Arial", 14, "bold")).pack(side="left")
        self.add_reason_text = ctk.CTkTextbox(
            content_frame,
            height=100,
            wrap="word",
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            border_color=self.COLOR_BORDER,
            border_width=1
        )
        self.add_reason_text.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 0))
        self.reason_error_label = ctk.CTkLabel(content_frame, text="", text_color="#EF4444")
        self.reason_error_label.grid(row=8, column=0, columnspan=2, sticky="w", pady=(0, 12))

        # --- Buttons ---
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=2, column=1, sticky="e", padx=30, pady=(10, 25))

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=120,
            height=35,
            fg_color=("#E0E0E0", "#555555"),
            text_color=("black", "white"),
            hover_color=("#D0D0D0", "#656565"),
            command=self.reset_add_form
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            button_frame,
            text="Submit Request",
            width=150,
            height=35,
            fg_color="#27AE60",
            hover_color="#1E8449",
            text_color="white",
            command=self._validate_and_submit
        ).pack(side="left")

    def _refresh_add_form_data(self):
        """Refreshes the data in the dropdowns on the add page."""
        self._load_initial_data() # Re-load the data
        
        self.add_leader_combo.configure(values=self.leader_names)
        self.add_project_combo.configure(values=self.project_names)
        
        # Set default values if list is not empty
        if self.leader_names:
            self.add_leader_combo.set("Select leader...")
        else:
            self.add_leader_combo.set("No leaders found")

        if self.project_names:
            self.add_project_combo.set("Select project...")
        else:
            self.add_project_combo.set("No projects found")
    
    def reset_add_form(self):
        """Resets the add overtime request form fields."""
        self.add_leader_combo.set("Select leader...")
        self.add_project_combo.set("Select project...")
        self.add_date_picker.clear()
        self.add_hours_entry.delete(0, ctk.END)
        self.add_reason_text.delete("1.0", ctk.END)
        self._refresh_add_form_data() # Refresh dropdowns with latest data
        
        # Reset error states
        self._set_error_state(self.add_leader_combo, False)
        self._set_error_state(self.add_project_combo, False)
        self._set_error_state(self.add_date_picker.btn, False)
        self._set_error_state(self.add_hours_entry, False)
        self._set_error_state(self.add_reason_text, False)

    def _validate_and_submit(self):
        is_valid = True

        # Reset previous errors
        self.leader_error_label.configure(text="")
        self.add_leader_combo.configure(border_color=self.COLOR_BORDER)
        self.project_error_label.configure(text="")
        self.add_project_combo.configure(border_color=self.COLOR_BORDER)
        self.date_error_label.configure(text="")
        self.add_date_picker.btn.configure(border_color=("#979DA2", "#565B5E"))
        self.hours_error_label.configure(text="")
        self.add_hours_entry.configure(border_color=self.COLOR_BORDER)
        self.reason_error_label.configure(text="")
        self.add_reason_text.configure(border_color=self.COLOR_BORDER)

        # --- Validation ---
        leader_name = self.add_leader_combo.get()
        if not leader_name or leader_name == "Select leader...":
            self.add_leader_combo.configure(border_color="#EF4444")
            self.leader_error_label.configure(text="Please select a valid leader.")
            is_valid = False

        project_name = self.add_project_combo.get()
        if not project_name or project_name == "Select project...":
            self.add_project_combo.configure(border_color="#EF4444")
            self.project_error_label.configure(text="Please select a valid project.")
            is_valid = False

        ot_date = self.add_date_picker.get_date()
        if not ot_date:
            self.add_date_picker.btn.configure(border_color="#EF4444")
            self.date_error_label.configure(text="Please select a valid date.")
            is_valid = False

        hours_str = self.add_hours_entry.get().strip()
        hours = 0
        if not hours_str:
            self.add_hours_entry.configure(border_color="#EF4444")
            self.hours_error_label.configure(text="Hours field cannot be empty.")
            is_valid = False
        else:
            try:
                hours = float(hours_str)
                if not (1 <= hours <= 8):
                    self.add_hours_entry.configure(border_color="#EF4444")
                    self.hours_error_label.configure(text="Hours must be between 1 and 8.")
                    is_valid = False
            except ValueError:
                self.add_hours_entry.configure(border_color="#EF4444")
                self.hours_error_label.configure(text="Please enter a valid number for hours.")
                is_valid = False

        reason = self.add_reason_text.get("1.0", "end-1c").strip()
        if not reason:
            self.add_reason_text.configure(border_color="#EF4444")
            self.reason_error_label.configure(text="The reason/tasks field is required.")
            is_valid = False

        if not is_valid:
            return

        # Get IDs for submission
        leader_id = self._get_user_id_by_full_name(leader_name)

        if not leader_id:
            self.add_leader_combo.configure(border_color="#EF4444")
            self.leader_error_label.configure(text="Selected leader not found in database.")
            return

        # --- Submission ---
        member_id = self.user['id']
        self.submit_overtime_request(member_id, leader_id, project_name, ot_date, hours, reason)

    def _set_error_state(self, widget, is_error):
        """Sets the visual state of a widget based on validation."""
        if is_error:
            widget.configure(border_color="#E74C3C", border_width=2)
        else:
            # Reset to default style
            widget.configure(border_color=self.COLOR_BORDER, border_width=1)
    
    def reset_add_form(self):
        """Resets all fields in the add overtime form."""
        # Reset visual state first
        self._set_error_state(self.add_project_combo, False)
        self._set_error_state(self.add_date_picker.btn, False)
        self._set_error_state(self.add_hours_entry, False)
        self._set_error_state(self.add_reason_text, False)

        self.add_leader_combo.set("Select leader...")
        self.add_project_combo.set("Select project...")
        self.add_date_picker.clear()
        self.add_date_picker.btn.configure(text=" 📅 Select Date")
        self.add_hours_entry.delete(0, "end")
        self.add_reason_text.delete("1.0", "end")
        
        # Update dropdown values
        self.add_project_combo.configure(values=self._get_project_names())
        self.add_leader_combo.configure(values=self._get_leader_names())
        
        self.show_page("main") # Go back to main page on cancel

    def submit_overtime_request(self, member_id, leader_id, project_name, ot_date, hours, reason):
        """Handles database insertion of the new OT request."""
        try:
            # Get project_id from project_name
            self.db.cursor.execute("SELECT id FROM projects WHERE project_name = %s AND team_id = %s", (project_name, self.user['team_id']))
            project_result = self.db.cursor.fetchone()
            if not project_result:
                try:
                    self.add_project_combo.configure(border_color="#EF4444")
                except Exception:
                    pass
                try:
                    self.project_error_label.configure(text="Selected project not found.")
                except Exception:
                    pass
                return
            project_id = project_result['id']

            # Duplicate check: prevent the same member from creating multiple
            # OT requests for the same day with Pending/Accepted status.
            try:
                ot_date_str = ot_date.strftime('%Y-%m-%d') if hasattr(ot_date, 'strftime') else str(ot_date)
            except Exception:
                ot_date_str = str(ot_date)

            self.db.cursor.execute("""
                SELECT SUM(hours) as total_hours FROM overtime_requests
                WHERE member_id = %s AND DATE(ot_date) = %s
                AND status IN ('Pending', 'Accepted')
            """, (member_id, ot_date_str))
            result = self.db.cursor.fetchone()
            existing_hours = float(result['total_hours'] or 0)

            if existing_hours + hours > 8:
                remaining = 8 - existing_hours
                msg = f"Total OT cannot exceed 8 hours per day. Remaining: {remaining:g}h" if remaining > 0 else "Daily OT limit (8h) reached."
                self._show_message(msg, "warning")
                return

            # --- Database Insertion ---
            # Insert only the columns that exist in the current DB schema.
            # The `overtime_requests` table in wfh_system.sql has no `created_by` column,
            # and `created_at` has a default timestamp, so we don't insert those.
            query = """
                INSERT INTO overtime_requests 
                (member_id, project_id, ot_date, hours, reason, status, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            # created_by is the member who submitted the request
            self.db.cursor.execute(query, (
                member_id, project_id, ot_date, hours, reason, 'Pending', member_id
            ))

            # --- Trigger Notification Badge for Leader Button (sec_notifications) ---
            notif_msg = f"overtime request submitted by {self.user['full_name']}."
            notif_sql = "INSERT INTO sec_notifications (user_id, message, is_read, created_at) VALUES (%s, %s, 0, NOW())"
            self.db.cursor.execute(notif_sql, (leader_id, notif_msg))

            # --- Trigger Notification Badge for Leader Sidebar (notifications) ---
            notif_sql_sidebar = "INSERT INTO notifications (user_id, message, is_read, created_at) VALUES (%s, %s, 0, NOW())"
            self.db.cursor.execute(notif_sql_sidebar, (leader_id, notif_msg))

            self.db.conn.commit()

            # Clear any inline errors / reset visual state
            try:
                self._set_error_state(self.add_leader_combo, False)
                self._set_error_state(self.add_project_combo, False)
                self._set_error_state(self.add_date_picker.btn, False)
                self._set_error_state(self.add_hours_entry, False)
                self._set_error_state(self.add_reason_text, False)
            except Exception:
                pass
            try:
                self.leader_error_label.configure(text="")
                self.project_error_label.configure(text="")
                self.date_error_label.configure(text="")
                self.hours_error_label.configure(text="")
                self.reason_error_label.configure(text="")
            except Exception:
                pass

            self._show_message("Overtime request submitted successfully!", "success")
            self.reset_add_form()
            self.show_page("main")

        except Exception as e:
            # Print and show the actual error, rollback, and do not claim success
            print(f"Error submitting OT request: {e}")
            self.db.conn.rollback()
            self._show_message(f"An error occurred: {e}", "error")

    def on_tab_change(self, value):
        """Handle tab/segmented button change"""
        if value == "📋 Pending Requests":
            self.show_pending_tab()
        elif value == "📜 History":
            self.show_history_tab()
            self.mark_history_as_read()

    def show_pending_tab(self):
        """Show pending requests tab"""
        # Hide history frame, show pending frame
        self.history_frame.grid_forget()
        self.pending_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.refresh_pending_requests()

    def show_history_tab(self):
        """Show history tab"""
        # Hide pending frame, show history frame
        self.pending_frame.grid_forget()
        self.history_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.refresh_history()

    def refresh_all_data(self):
        """Refresh both tabs"""
        self.refresh_pending_requests()
        self.refresh_history()
        self.refresh_history_badge()

    def refresh_history_badge(self):
        """Check for unread leader responses in sec_notifications"""
        try:
            self.db.cursor.execute(
                "SELECT COUNT(*) as cnt FROM sec_notifications "
                "WHERE user_id = %s AND is_read = 0 "
                "AND (message LIKE '%%Accepted%%' OR message LIKE '%%Rejected%%')", 
                (self.user['id'],)
            )
            count = self.db.cursor.fetchone()['cnt']
            
            if count > 0:
                self.history_badge.configure(text=str(count))
                # Position near the "History" segment (right side of button)
                self.history_badge.place(relx=0.95, rely=0.5, anchor="center")
            else:
                self.history_badge.place_forget()
        except: pass

    def mark_history_as_read(self):
        """Mark leader response notifications as read"""
        try:
            self.db.cursor.execute(
                "UPDATE sec_notifications SET is_read = 1 "
                "WHERE user_id = %s AND (message LIKE '%%Accepted%%' OR message LIKE '%%Rejected%%')",
                (self.user['id'],)
            )
            self.db.conn.commit()
            self.refresh_history_badge()
        except: pass

    def auto_refresh(self):
        """Background polling loop"""
        if self._is_destroyed: return
        self.refresh_history_badge()
        self._after_id = self.after(10000, self.auto_refresh) # Every 10 seconds

    def refresh_pending_requests(self):
        """Show pending OT requests from leader"""
        for w in self.pending_frame.winfo_children():
            w.destroy()
        
        query = """
            SELECT o.*, p.project_name, c.full_name AS creator_name, c.role AS creator_role
            FROM overtime_requests o
            JOIN projects p ON o.project_id = p.id
            JOIN users c ON o.created_by = c.id
            WHERE o.member_id = %s AND o.status = 'Pending'
            ORDER BY o.created_at DESC
        """
        try:
            self.db.cursor.execute(query, (self.user['id'],))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(
                    self.pending_frame, 
                    text="✨ No pending requests from leader.",
                    text_color=self.COLOR_TEXT_SEC,
                    font=("Arial", 14)
                ).pack(expand=True, fill="both", pady=50)
                return

            # Show count badge
            count_frame = ctk.CTkFrame(self.pending_frame, fg_color="transparent")
            count_frame.pack(fill="x", pady=(10, 5), padx=10)
            
            ctk.CTkLabel(
                count_frame,
                text=f"📬 You have {len(rows)} pending request(s)",
                font=("Arial", 12, "bold"),
                text_color=self.COLOR_TEXT_MAIN
            ).pack(anchor="w")

            for r in rows:
                card = ctk.CTkFrame(
                    self.pending_frame,
                    fg_color=self.COLOR_CARD_BG,
                    corner_radius=10,
                    border_width=1,
                    border_color=self.COLOR_BORDER
                )
                card.pack(fill="x", pady=8, padx=10)

                # Content
                content_frame = ctk.CTkFrame(card, fg_color="transparent")
                content_frame.pack(fill="x", padx=15, pady=12)

                # Project and Date row
                top_row = ctk.CTkFrame(content_frame, fg_color="transparent")
                top_row.pack(fill="x", pady=(0, 8))
                
                ctk.CTkLabel(
                    top_row,
                    text=f"📁 {r['project_name']}",
                    font=("Arial", 13, "bold"),
                    text_color=self.COLOR_TEXT_MAIN
                ).pack(side="left")
                
                ctk.CTkLabel(
                    top_row,
                    text=f"📅 {r['ot_date']}",
                    font=("Arial", 11),
                    text_color=self.COLOR_TEXT_SEC
                ).pack(side="right")

                # Hours and Details
                details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                details_frame.pack(fill="x", pady=5)
                
                ctk.CTkLabel(
                    details_frame,
                    text=f"⏳ Duration: {r['hours']} hours",
                    font=("Arial", 12),
                    text_color=self.COLOR_TEXT_MAIN
                ).pack(anchor="w")

                # Leader's reason
                if r['reason'] and r['reason'].strip():
                    reason_frame = ctk.CTkFrame(content_frame, fg_color=self.COLOR_CONTAINER_BG, corner_radius=6)
                    reason_frame.pack(fill="x", pady=(8, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text=f"💬 Request Content :",
                        font=("Arial", 11, "bold"),
                        text_color=("#F39C12", "#F39C12")
                    ).pack(anchor="w", padx=10, pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text=r['reason'],
                        font=("Arial", 11),
                        text_color=self.COLOR_TEXT_SEC,
                        wraplength=550,
                        justify="left"
                    ).pack(anchor="w", padx=10, pady=(0, 5))

                # Buttons
                btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                btn_frame.pack(fill="x", pady=(12, 0))

                def _btn(text, color, hover, cmd, width=60, height=30, corner_radius=14):
                    return ctk.CTkButton(
                        btn_frame,
                        text=text,
                        width=width,
                        height=height,
                        corner_radius=corner_radius,
                        fg_color=color,
                        hover_color=hover,
                        font=("Arial", 12, "bold"),
                        text_color="white",
                        command=cmd
                    )

                if r['created_by'] == self.user['id']:
                    # Member created this request - show Edit/Delete
                    _btn("✏ Edit", "#F39C12", "#D68910", 
                        lambda row=r: self.edit_request(row)
                    ).pack(side="left", padx=(0, 10))

                    _btn("🗑 Delete", "#E74C3C", "#C0392B", 
                        lambda id=r['id']: self.delete_request(id)
                    ).pack(side="left")
                else:
                    # Leader created this request - show Accept/Reject
                    _btn("✓ Accept", "#27AE60", "#1E8449", 
                        lambda id=r['id']: self.update_status(id, 'Accepted')
                    ).pack(side="left", padx=(0, 10))

                    _btn("✗ Reject", "#E74C3C", "#C0392B", 
                        lambda id=r['id']: self.handle_reject(id)
                    ).pack(side="left")


        except Exception as e:
            print(f"Error loading pending requests: {e}")
            self._show_message(f"Could not load requests: {e}", "error")

    def refresh_history(self):
        """Show OT request history (non-pending)"""
        for w in self.history_frame.winfo_children():
            w.destroy()
        
        query = """
            SELECT o.*, p.project_name 
            FROM overtime_requests o 
            JOIN projects p ON o.project_id = p.id 
            WHERE o.member_id = %s AND o.status != 'Pending'
            ORDER BY o.created_at DESC
        """
        try:
            self.db.cursor.execute(query, (self.user['id'],))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(
                    self.history_frame, 
                    text="📭 No overtime history yet.",
                    text_color=self.COLOR_TEXT_SEC,
                    font=("Arial", 14)
                ).pack(expand=True, fill="both", pady=50)
                return

            # Show history count
            count_frame = ctk.CTkFrame(self.history_frame, fg_color="transparent")
            count_frame.pack(fill="x", pady=(10, 5), padx=10)
            
            ctk.CTkLabel(
                count_frame,
                text=f"📊 Total records: {len(rows)}",
                font=("Arial", 12, "bold"),
                text_color=self.COLOR_TEXT_MAIN
            ).pack(anchor="w")

            for r in rows:
                card = ctk.CTkFrame(
                    self.history_frame, 
                    fg_color=self.COLOR_CARD_BG, 
                    corner_radius=10,
                    border_width=1,
                    border_color=self.COLOR_BORDER
                )
                card.pack(fill="x", pady=8, padx=10)

                status_colors = {
                    "Accepted": self.COLOR_TEXT_MAIN, 
                    "Rejected": ("#E74C3C", "#E74C3C"), 
                    "Approved": ("#2980B9", "#2980B9")
                }
                s_color = status_colors.get(r['status'], self.COLOR_TEXT_SEC)

                # Content
                content_frame = ctk.CTkFrame(card, fg_color="transparent")
                content_frame.pack(fill="x", padx=15, pady=12)
                
                # First row: Project, Date, and Status
                top_row = ctk.CTkFrame(content_frame, fg_color="transparent")
                top_row.pack(fill="x", pady=(0, 8))
                
                left_info = f"📁 {r['project_name']}  |  📅 {r['ot_date']}  |  ⏳ {r['hours']} hrs"
                ctk.CTkLabel(
                    top_row, 
                    text=left_info, 
                    font=("Arial", 12),
                    text_color=self.COLOR_TEXT_MAIN
                ).pack(side="left")
                
                ctk.CTkLabel(
                    top_row, 
                    text=r['status'], 
                    text_color=s_color, 
                    font=("Arial", 12, "bold")
                ).pack(side="right")

                # Show Leader's Original Reason
                if r['reason'] and r['reason'].strip():
                    reason_frame = ctk.CTkFrame(content_frame, fg_color=self.COLOR_CONTAINER_BG, corner_radius=6)
                    reason_frame.pack(fill="x", pady=(8, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text="📋 Leader's Reason:",
                        font=("Arial", 11, "bold"),
                        text_color=self.COLOR_TEXT_MAIN
                    ).pack(anchor="w", padx=10, pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text=r['reason'],
                        font=("Arial", 11),
                        text_color=self.COLOR_TEXT_SEC,
                        wraplength=550,
                        justify="left"
                    ).pack(anchor="w", padx=10, pady=(0, 5))

                # Show Member's Rejection Reason (if rejected)
                if r['status'] == 'Rejected' and r.get('rejected_reason') and r['rejected_reason'].strip():
                    reject_frame = ctk.CTkFrame(content_frame, fg_color=("#F8E6E6", "#3D1E1E"), corner_radius=6)
                    reject_frame.pack(fill="x", pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reject_frame,
                        text="❌ Your Rejection Reason:",
                        font=("Arial", 11, "bold"),
                        text_color=("#E74C3C", "#E74C3C")
                    ).pack(anchor="w", padx=10, pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reject_frame,
                        text=r['rejected_reason'],
                        font=("Arial", 11),
                        text_color=self.COLOR_TEXT_SEC,
                        wraplength=550,
                        justify="left"
                    ).pack(anchor="w", padx=10, pady=(0, 5))

        except Exception as e:
            print(f"Error loading history: {e}")
            self._show_message(f"Could not load history: {e}", "error")

    def handle_reject(self, ot_id):
        """Handle reject action with reason input (styled popup)"""
        popup = ctk.CTkToplevel(self)
        popup.title("Reject Overtime")
        
        # Centering logic relative to parent window
        width, height = 400, 250
        popup.update_idletasks()
        parent = self.winfo_toplevel()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        
        popup.resizable(False, False)
        popup.attributes("-topmost", True)
        popup.grab_set()

        ctk.CTkLabel(
            popup, 
            text="Please provide reason for rejection:", 
            font=("Arial", 14, "bold")
        ).pack(pady=(15, 10))

        reason_box = ctk.CTkTextbox(popup, height=100)
        reason_box.pack(fill="x", padx=20)

        def confirm():
            reason = reason_box.get("0.0", "end").strip()
            if reason:
                self.update_status(ot_id, 'Rejected', reason)
                popup.destroy()
            else:
                self._show_message("Reason is required to reject.", "warning")

        def cancel():
            popup.destroy()

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(
            btn_frame, 
            text="✓ Confirm", 
            width=100, 
            height=32,
            corner_radius=14,
            fg_color="#E74C3C", 
            hover_color="#C0392B", 
            text_color="white", 
            command=confirm
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame, 
            text="✗ Cancel", 
            width=100, 
            height=32,
            corner_radius=14,
            fg_color="#95A5A6", 
            hover_color="#7F8C8D", 
            text_color="white", 
            command=cancel
        ).pack(side="left", padx=10)


    def update_status(self, ot_id, new_status, member_note=None):
        """Permanent Fix: Updates status and triggers Leader notification badge"""
        try:
            # 1. Update the Overtime Request itself
            if member_note:
                sql = "UPDATE overtime_requests SET status = %s, rejected_reason = %s WHERE id = %s"
                self.db.cursor.execute(sql, (new_status, member_note, ot_id))
                # MUST use lowercase 'overtime' to trigger leader_menu.py badge logic
                msg = f"overtime request rejected by {self.user['full_name']}"
            else:
                sql = "UPDATE overtime_requests SET status = %s WHERE id = %s"
                self.db.cursor.execute(sql, (new_status, ot_id))
                msg = f"Overtime request accepted by {self.user['full_name']}"
            
            # 2. Add to notification table
            # FIX: Fetch the specific leader who created the request to target the notification
            self.db.cursor.execute("SELECT created_by FROM overtime_requests WHERE id = %s", (ot_id,))
            creator_row = self.db.cursor.fetchone()
            
            if creator_row and creator_row['created_by']:
                notif_sql = "INSERT INTO notifications (user_id, message, is_read, created_at) VALUES (%s, %s, 0, NOW())"
                self.db.cursor.execute(notif_sql, (creator_row['created_by'], msg))
            
            # 3. Commit changes to Database
            self.db.conn.commit()
            
            self._show_message(f"OT Request {new_status}!", "success")
            
            # 4. Refresh UI Tabs
            self.refresh_all_data()
            self.show_page("main") # Go back to main page
                
        except Exception as e:
            if hasattr(self.db, 'conn'):
                self.db.conn.rollback()
            self._show_message(f"System Error: {e}", "error")

    def create_edit_page(self):
        self.edit_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.edit_page.grid_rowconfigure(1, weight=1)
        self.edit_page.grid_columnconfigure(0, weight=1)
        
        # Back button
        back_btn = ctk.CTkButton(
            self.edit_page,
            text="← Back",
            text_color=("black", "white"),
            width=80,
            fg_color=("#DBDBDB", "#333333"),
            hover_color=("#CFCFCF", "#444444"),
            corner_radius=8,
            height=36,
            command=lambda: self.show_page("main")
        )
        back_btn.grid(row=0, column=0, sticky="nw", padx=60, pady=(10, 0))

        # Create scrollable container for the form
        self.edit_scrollable = ctk.CTkScrollableFrame(
            self.edit_page,
            fg_color="transparent"
        )
        self.edit_scrollable.grid(row=1, column=0, sticky="nsew", padx=60, pady=10)
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
        self.edit_form.grid_columnconfigure(0, weight=1)
        self.edit_form.grid_columnconfigure(1, weight=1)
        self.edit_form.grid_columnconfigure(2, weight=1)

    def edit_request(self, row):
        """Load the edit page with request data"""
        self.load_edit_form(row)
        self.show_page("edit")

    def load_edit_form(self, row):
        """Load edit form with request data"""
        for widget in self.edit_form.winfo_children():
            widget.destroy()

        self.edit_form.grid_columnconfigure(0, weight=1)
        self.edit_form.grid_columnconfigure(1, weight=1)
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

        # Display read-only info
        def create_info_row(label, value, row_num, icon=""):
            frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            frame.grid(row=row_num, column=0, sticky="ew", pady=8)
            
            ctk.CTkLabel(
                frame,
                text=f"{icon} {label}:",
                font=("Arial", 13, "bold"),
                text_color=self.COLOR_TEXT_SEC,
                width=120,
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                frame,
                text=value,
                font=("Arial", 13),
                anchor="w",
                text_color=self.COLOR_TEXT_MAIN
            ).pack(side="left", fill="x", expand=True, padx=(10, 0))

        create_info_row("Project", row['project_name'], 0, "📁")
        create_info_row("Date", str(row['ot_date']), 1, "📅")
        
        # Editable hours
        hours_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        hours_frame.grid(row=2, column=0, sticky="ew", pady=(15, 0))
        
        ctk.CTkLabel(
            hours_frame,
            text="⏱️ Hours:",
            font=("Arial", 13, "bold"),
            text_color=self.COLOR_TEXT_SEC,
            width=120,
            anchor="w"
        ).pack(side="left")
        
        self.edit_hours_entry = ctk.CTkEntry(hours_frame, width=120, height=40)
        self.edit_hours_entry.pack(side="left", padx=(10, 0))
        self.edit_hours_entry.insert(0, str(row['hours']))

        # Editable reason
        ctk.CTkLabel(
            content_frame,
            text="📝 Reason / Tasks:",
            font=("Arial", 13, "bold"),
            text_color=self.COLOR_TEXT_SEC
        ).grid(row=3, column=0, sticky="w", pady=(15, 5))
        
        self.edit_reason_text = ctk.CTkTextbox(
            content_frame,
            height=100,
            fg_color=self.COLOR_CARD_BG,
            border_width=1,
            border_color=self.COLOR_BORDER,
            text_color=self.COLOR_TEXT_MAIN
        )
        self.edit_reason_text.grid(row=4, column=0, sticky="ew", pady=(0, 15))
        self.edit_reason_text.insert("1.0", row['reason'] or "")

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

    def update_overtime(self, ot_id):
        """Update the overtime record"""
        try:
            hours_str = self.edit_hours_entry.get().strip()
            if not hours_str:
                self._show_message("Hours field cannot be empty.", "error")
                return
            hours = float(hours_str)
            if not (1 <= hours <= 8):
                self._show_message("Hours must be between 1 and 8.", "error")
                return
        except ValueError:
            self._show_message("Please enter a valid number for hours.", "error")
            return

        reason = self.edit_reason_text.get("1.0", "end-1c").strip()
        if not reason:
            self._show_message("Reason field is required.", "error")
            return

        try:
            # Check total hours for the day excluding current record
            self.db.cursor.execute("""
                SELECT SUM(hours) as total_hours FROM overtime_requests
                WHERE member_id = %s 
                AND DATE(ot_date) = (SELECT DATE(ot_date) FROM overtime_requests WHERE id = %s)
                AND status IN ('Pending', 'Accepted')
                AND id != %s
            """, (self.user['id'], ot_id, ot_id))
            
            result = self.db.cursor.fetchone()
            other_hours = float(result['total_hours'] or 0)
            
            if other_hours + hours > 8:
                remaining = 8 - other_hours
                self._show_message(f"Daily limit exceeded. Remaining: {remaining:g}h", "error")
                return

            self.db.cursor.execute("""
                UPDATE overtime_requests
                SET hours = %s, reason = %s
                WHERE id = %s AND status = 'Pending'
            """, (hours, reason, ot_id))
            
            self.db.conn.commit()
            self._show_message("Overtime request updated successfully!", "success")
            self.show_page("main")
        except Exception as e:
            self.db.conn.rollback()
            self._show_message(f"System Error: {e}", "error")

    def delete_request(self, ot_id):
        """Delete an overtime request"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this pending request?"):
            try:
                self.db.cursor.execute("DELETE FROM overtime_requests WHERE id = %s AND status = 'Pending'", (ot_id,))
                self.db.conn.commit()
                self._show_message("Overtime request deleted successfully!", "success")
                self.refresh_all_data()
            except Exception as e:
                self.db.conn.rollback()
                self._show_message(f"System Error: {e}", "error")

    def destroy(self):
        """Clean up background tasks"""
        self._is_destroyed = True
        if self._after_id:
            self.after_cancel(self._after_id)
        super().destroy()