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

class MemberOvertime(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user  # Login ဝင်ထားသော Member data
        
        # Automatic Theme Constants (Tuples) - matching member_report.py
        self.COLOR_CARD_BG = ("#FFFFFF", "#1E1E1E")
        self.COLOR_BORDER = ("#DBDBDB", "#2C2C2C")
        self.COLOR_TEXT_MAIN = ("#1A1A2A", "#E8EDF2")
        self.COLOR_TEXT_SEC = ("#555555", "#AAB7C4")
        self.COLOR_TEXT_TER = ("#777777", "#718096")
        self.COLOR_SCROLL_BG = ("#F5F5F5", "#1A1A1A")
        self.COLOR_CONTAINER_BG = ("#F0F0F0", "#252525")

        # Initialize page structure
        self.pages = ctk.CTkFrame(self, fg_color="transparent")
        self.pages.grid(row=0, column=0, sticky="nsew")
        self.pages.grid_rowconfigure(0, weight=1)
        self.pages.grid_columnconfigure(0, weight=1)

        # Center the container
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.pages.grid(row=0, column=0) # Remove sticky

        # Initialize all pages
        self.create_main_page()
        self.create_add_page()
        
        # Show main page initially
        self.show_page("main")
        
        # Initial data load
        self.refresh_all_data()

    def _get_project_names(self):
        try:
            self.db.cursor.execute("SELECT project_name FROM projects ORDER BY project_name")
            return [row['project_name'] for row in self.db.cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching project names: {e}")
            return []

    def _get_member_names(self):
        try:
            # Assuming you want to list all members
            self.db.cursor.execute("SELECT full_name FROM users WHERE role = 'member' ORDER BY full_name")
            return [row['full_name'] for row in self.db.cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching member names: {e}")
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
            # self.reset_add_form() # We will create this later

    def create_main_page(self):
        self.main_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.main_page.grid_rowconfigure(2, weight=1) # Content frame
        self.main_page.grid_columnconfigure(0, weight=1)

        # --- Header ---
        header = ctk.CTkFrame(self.main_page, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=80, pady=20)
        
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
        self.segmented_btn.grid(row=1, column=0, sticky="ew", padx=80, pady=10)
        self.segmented_btn.set("📋 Pending Requests")  # Set default tab

        # --- Content Frame (changes based on selected tab) ---
        self.content_frame = ctk.CTkFrame(self.main_page, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=80, pady=10)
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
            text="← Back to List",
            text_color=("black", "white"),
            width=100,
            fg_color=("#DBDBDB", "#333333"),
            font=("Arial", 12),
            height=35,
            command=lambda: self.show_page("main")
        )
        back_btn.grid(row=0, column=0, sticky="nw", padx=80, pady=(10, 0))

        # --- Scrollable Form Container ---
        add_scrollable = ctk.CTkScrollableFrame(self.add_page, fg_color="transparent")
        add_scrollable.grid(row=1, column=0, sticky="nsew", padx=80, pady=10)
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

        # --- Member ---
        ctk.CTkLabel(content_frame, text="👤 Member *", font=("Arial", 14, "bold"), anchor="w").grid(row=0, column=0, sticky="w", pady=(10, 5))
        self.add_member_combo = ctk.CTkComboBox(
            content_frame,
            values=self._get_member_names(),
            width=350,
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            border_color=self.COLOR_BORDER,
            button_color=self.COLOR_BORDER,
            border_width=1
        )
        self.add_member_combo.set("Select member...")
        self.add_member_combo.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # --- Project ---
        ctk.CTkLabel(content_frame, text="📁 Project *", font=("Arial", 14, "bold"), anchor="w").grid(row=2, column=0, sticky="w", pady=(5, 5))
        self.add_project_combo = ctk.CTkComboBox(
            content_frame,
            values=self._get_project_names(),
            width=350,
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            border_color=self.COLOR_BORDER,
            button_color=self.COLOR_BORDER,
            border_width=1
        )
        self.add_project_combo.set("Select project...")
        self.add_project_combo.grid(row=3, column=0, sticky="ew", pady=(0, 15))

        # --- Date ---
        ctk.CTkLabel(content_frame, text="📅 Date *", font=("Arial", 14, "bold"), anchor="w").grid(row=4, column=0, sticky="w", pady=(5, 5))
        self.add_date_picker = DatePickerButton(content_frame, initial_date=date.today(), allow_past=True)
        self.add_date_picker.grid(row=5, column=0, sticky="w", pady=(0, 15))

        # --- Hours ---
        ctk.CTkLabel(content_frame, text="⏱️ Hours * (1-8 hours)", font=("Arial", 14, "bold"), anchor="w").grid(row=6, column=0, sticky="w", pady=(5, 5))
        self.add_hours_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="e.g., 2.5",
            width=350,
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            border_color=self.COLOR_BORDER,
            border_width=1
        )
        self.add_hours_entry.grid(row=7, column=0, sticky="ew", pady=(0, 15))

        # --- Reason ---
        ctk.CTkLabel(content_frame, text="📝 Reason / Tasks *", font=("Arial", 14, "bold"), anchor="w").grid(row=8, column=0, sticky="w", pady=(5, 5))
        self.add_reason_text = ctk.CTkTextbox(
            content_frame,
            height=120,
            wrap="word",
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            border_color=self.COLOR_BORDER,
            border_width=1
        )
        self.add_reason_text.grid(row=9, column=0, sticky="ew", pady=(0, 20))

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
            command=self._validate_and_submit
        ).pack(side="left")
    
    def _validate_and_submit(self):
        # Reset all field appearances to normal
        self._set_error_state(self.add_member_combo, False)
        self._set_error_state(self.add_project_combo, False)
        self._set_error_state(self.add_date_picker.btn, False)
        self._set_error_state(self.add_hours_entry, False)
        self._set_error_state(self.add_reason_text, False)

        # --- Validation ---
        member_name = self.add_member_combo.get()
        if not member_name or member_name == "Select member...":
            self._show_message("Please select a valid member.", "error")
            self._set_error_state(self.add_member_combo, True)
            return

        project_name = self.add_project_combo.get()
        if not project_name or project_name == "Select project...":
            self._show_message("Please select a valid project.", "error")
            self._set_error_state(self.add_project_combo, True)
            return

        ot_date = self.add_date_picker.get_date()
        if not ot_date:
            self._show_message("Please select a valid date.", "error")
            self._set_error_state(self.add_date_picker.btn, True)
            return

        hours_str = self.add_hours_entry.get().strip()
        if not hours_str:
            self._show_message("Hours field cannot be empty.", "error")
            self._set_error_state(self.add_hours_entry, True)
            return
        try:
            hours = float(hours_str)
            if not (1 <= hours <= 8):
                self._show_message("Hours must be between 1 and 8.", "error")
                self._set_error_state(self.add_hours_entry, True)
                return
        except ValueError:
            self._show_message("Please enter a valid number for hours.", "error")
            self._set_error_state(self.add_hours_entry, True)
            return

        reason = self.add_reason_text.get("1.0", "end-1c").strip()
        if not reason:
            self._show_message("The reason/tasks field is required.", "error")
            self._set_error_state(self.add_reason_text, True)
            return

        # --- Submission ---
        self.submit_overtime_request(member_name, project_name, ot_date, hours, reason)

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
        self._set_error_state(self.add_member_combo, False)
        self._set_error_state(self.add_project_combo, False)
        self._set_error_state(self.add_date_picker.btn, False)
        self._set_error_state(self.add_hours_entry, False)
        self._set_error_state(self.add_reason_text, False)

        self.add_member_combo.set("Select member...")
        self.add_project_combo.set("Select project...")
        self.add_date_picker.clear()
        self.add_date_picker.btn.configure(text=" 📅 Select Date")
        self.add_hours_entry.delete(0, "end")
        self.add_reason_text.delete("1.0", "end")
        
        # Update dropdown values
        self.add_project_combo.configure(values=self._get_project_names())
        self.add_member_combo.configure(values=self._get_member_names())
        
        self.show_page("main") # Go back to main page on cancel

    def submit_overtime_request(self, member_name, project_name, ot_date, hours, reason):
        """Handles database insertion of the new OT request."""
        try:
            # Get member_id from member_name
            self.db.cursor.execute("SELECT id FROM users WHERE full_name = %s", (member_name,))
            member_result = self.db.cursor.fetchone()
            if not member_result:
                self._show_message("Selected member not found.", "error")
                return
            member_id = member_result['id']

            # Get project_id from project_name
            self.db.cursor.execute("SELECT id FROM projects WHERE project_name = %s", (project_name,))
            project_result = self.db.cursor.fetchone()
            if not project_result:
                self._show_message("Selected project not found.", "error")
                return
            project_id = project_result['id']

            # --- Database Insertion ---
            query = """
                INSERT INTO overtime_requests 
                (member_id, project_id, ot_date, hours, reason, status, created_at, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            current_time = datetime.now()
            created_by_id = self.user['id'] 
            
            self.db.cursor.execute(query, (
                member_id, project_id, ot_date, hours, reason, 
                'Pending', current_time, created_by_id
            ))
            self.db.conn.commit()
            
            self._show_message("Overtime request submitted successfully!", "success")
            self.reset_add_form()
            self.show_page("main")

        except Exception as e:
            self._show_message(f"An error occurred: {e}", "error")
            self.db.conn.rollback()
            
            self._show_message("Overtime request submitted successfully!", "success")
            self.reset_add_form()
            self.show_page("main") # Switch back to the main page
            
        except Exception as e:
            self.db.conn.rollback()
            self._show_message(f"Database error: {e}", "error")
            print(f"Error submitting OT request: {e}")

    def on_tab_change(self, value):
        """Handle tab/segmented button change"""
        if value == "📋 Pending Requests":
            self.show_pending_tab()
        elif value == "📜 History":
            self.show_history_tab()

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

    def refresh_pending_requests(self):
        """Show pending OT requests from leader"""
        for w in self.pending_frame.winfo_children():
            w.destroy()
        
        query = """
            SELECT o.*, p.project_name 
            FROM overtime_requests o 
            JOIN projects p ON o.project_id = p.id 
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
                        text="💬 Leader's Request:",
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
        popup.geometry("400x250")
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
            width=60, 
            height=30,
            corner_radius=14,
            fg_color="#E74C3C", 
            hover_color="#C0392B", 
            text_color="white", 
            command=confirm
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame, 
            text="✗ Cancel", 
            width=60, 
            height=30,
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
                msg = f"overtime request accepted by {self.user['full_name']}"
            
            # 2. Add to notification table (Matching your Leave Request logic)
            # This SQL finds the 'created_by' (Leader ID) from the projects table 
            # linked to this overtime request.
            req_id = self.db.cursor.lastrowid  # Get the ID of the OT request you just created
            msg = f"{self.user['full_name']} submitted a new overtime request."

            notif_sql = """
                INSERT INTO notifications (user_id, message, is_read, created_at)
                SELECT id, %s, 0, NOW() FROM users 
                WHERE role = 'leader' AND team_id = %s
            """
            self.db.cursor.execute(notif_sql, (msg, self.user.get('team_id')))
            
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