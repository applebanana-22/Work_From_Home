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
        self._is_destroyed = False
        self._after_id = None
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

        # Start auto-refresh for the button badge
        self.auto_refresh()
        
        # Start auto-cancellation check
        self.check_overdue_requests()

    def _get_widget_font(self, widget):
        try:
            f = widget.cget('font')
            if f:
                return f
        except Exception:
            pass
        return ("Helvetica", 10)

    def _set_field_error(self, widget, message, parent=None):
        """Highlight a widget and show an inline error message below it."""
        parent = parent or getattr(widget, "master", None)
        self._clear_field_error(widget)
        try:
            widget.configure(border_color="#E74C3C", border_width=2)
        except Exception:
            pass

        font = self._get_widget_font(widget)
        try:
            # Handle CTkFont object
            size = font.cget("size")
            family = font.cget("family")
            error_font = (family, size - 2 if size > 8 else size)
        except AttributeError:
            # Handle tuple
            size = font[1]
            family = font[0]
            error_font = (family, size - 2 if size > 8 else size)

        err = ctk.CTkLabel(
            parent,
            text=message,
            text_color="#E74C3C",
            fg_color="transparent",
            font=error_font,
        )

        widget._error_label = err

        try:
            info = widget.grid_info()
            if info and isinstance(info, dict) and 'row' in info and 'column' in info:
                try:
                    r = int(info.get('row', 0))
                    c = int(info.get('column', 0))
                    colspan = int(info.get('columnspan', 1) or 1)

                    parent.update_idletasks()
                    conflict = False
                    for w in parent.winfo_children():
                        try:
                            gi = w.grid_info()
                            if gi and isinstance(gi, dict) and int(gi.get('row', -999)) == r + 1 and int(gi.get('column', -999)) == c:
                                conflict = True
                                break
                        except Exception:
                            continue

                    if conflict:
                        widget.update_idletasks()
                        above_x = None
                        for w in parent.winfo_children():
                            try:
                                gi = w.grid_info()
                                if gi and isinstance(gi, dict) and int(gi.get('row', -999)) == r - 1 and int(gi.get('column', -999)) == c:
                                    above_x = w.winfo_x()
                                    break
                            except Exception:
                                continue

                        x = above_x if above_x is not None else widget.winfo_x()
                        y = widget.winfo_y() + widget.winfo_height() + 2
                        err.place(in_=parent, x=x, y=y, anchor='nw')
                        err.lift()
                        return

                    err.grid(row=r + 1, column=c, columnspan=colspan, sticky='w', padx=8, pady=(0, 0))
                    return
                except Exception:
                    pass
        except Exception:
            pass

        try:
            err.pack(after=widget, anchor="w", padx=8, pady=(0, 0))
        except Exception:
            try:
                err.pack(anchor="w", padx=8, pady=(0, 0))
            except Exception:
                pass

    def _clear_field_error(self, widget):
        """Remove inline error and restore widget border."""
        try:
            if hasattr(widget, "_error_label") and widget._error_label:
                widget._error_label.destroy()
                widget._error_label = None
        except Exception:
            pass
        try:
            # reset border to a thin neutral line if supported
            widget.configure(border_color=None, border_width=1)
        except Exception:
            try:
                widget.configure(border_color=None)
            except Exception:
                pass

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
            self.mark_member_requests_as_read()

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
        self.member_req_btn = ctk.CTkButton(
            header,
            text="Request OT from member",
            fg_color="#2980B9",
            hover_color="#21618C",
            width=210,
            height=40,
            corner_radius=10,
            font=("Arial", 12, "bold"),
            command=lambda: self.show_page("member_requests")
        )
        self.member_req_btn.pack(side="right", padx=10)

        # Create the badge label for the button
        self.btn_badge = ctk.CTkLabel(
            self.member_req_btn,
            text="",
            font=("Arial", 10, "bold"),
            fg_color="#E74C3C",
            text_color="white",
            width=20, height=20, corner_radius=10
        )
        self.btn_badge.place_forget() # Hide initially

        ctk.CTkButton(
            header,
            text="+ Add Overtime",
            fg_color="#10B981",
            hover_color="#0E9769",
            width=160,
            height=40,
            corner_radius=10,
            font=("Arial", 12, "bold"),
            command=lambda: self.show_page("add")
        ).pack(side="right", padx=10)

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
            height=36,
            corner_radius=10,
            state="readonly",
            command=lambda v: self.load_data() 
        )
        self.member_search.set("Member...") # Acts as placeholder
        self.member_search.pack(side="left", padx=(10, 5), pady=10)

        self.project_search = ctk.CTkComboBox(
            filter_frame,
            values=self.project_names,
            width=120,             
            height=36,
            corner_radius=10,
            state="readonly",
            command=lambda v: self.load_data() 
        )
        self.project_search.set("Project...") # Acts as placeholder
        self.project_search.pack(side="left", padx=(10, 5), pady=10)

        self.status_filter = ctk.CTkComboBox(
            filter_frame,
            values=["All", "Pending", "Accepted", "Rejected", "Cancelled"],
            width=100,
            height=36,
            corner_radius=10,
            state="readonly",
            command=lambda v: self.load_data()
        )
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=5, pady=10)

        # Date filter - default to today and allow past dates (allow_past=True)
        self.date_filter = DatePickerButton(filter_frame, initial_date=None, allow_past=True)
        self.date_filter.pack(side="left", padx=5, pady=10)

        # Filter buttons with original design
        btn_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)

        # Swap positions: Clear sits to the right of Filter visually by packing Clear first then Filter
        ctk.CTkButton(
            btn_frame,
            text="✖ Clear",
            width=60,
            height=36,
            corner_radius=8,
            font=("Arial", 11, "bold"),
            fg_color="#566573",
            hover_color="#424949",
            command=self.clear_filters
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="🔍 Filter",
            width=60,
            height=36,
            corner_radius=8,
            font=("Arial", 11, "bold"),
            fg_color="#2471A3",
            hover_color="#1A5276",
            command=self.refresh_ui
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
                text="← Back",
                width=80,
                height=36,
                fg_color=("#DBDBDB", "#333333"),
                text_color=("black", "white"),
                hover_color=("#CFCFCF", "#444444"),
                corner_radius=8,
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
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Load data if not loaded
        if not hasattr(self, 'member_map'):
            self.load_member_project_data()
        
        # Member field
        member_label_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        member_label_frame.grid(row=0, column=0, sticky="w", pady=(8, 4), padx=(0, 10))
        ctk.CTkLabel(
            member_label_frame,
            text="👤 Member",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).pack(side="left")
        ctk.CTkLabel(
            member_label_frame,
            text=" *",
            text_color="#E74C3C",
            font=("Arial", 14, "bold"),
        ).pack(side="left")
        
        self.member_cb = ctk.CTkComboBox(
            content_frame,
            values=self.member_names,
            width=300,
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            state="readonly",
            # button_color="#1E2A3A",
            # button_hover_color="#2C3E50"
        )
        self.member_cb.set("Select member...")
        self.member_cb.grid(row=1, column=0, sticky="ew", pady=(0, 8), padx=(0, 10))

        # Inline error label for member
        self.member_error_label = ctk.CTkLabel(
            content_frame,
            text="",
            text_color="#E74C3C",
            fg_color="transparent",
            font=("Arial", 10)
        )
        self.member_error_label.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 8))

        # Project field
        project_label_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        project_label_frame.grid(row=0, column=1, sticky="w", pady=(8, 4))
        ctk.CTkLabel(
            project_label_frame,
            text="📁 Project",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).pack(side="left")
        ctk.CTkLabel(
            project_label_frame,
            text=" *",
            text_color="#E74C3C",
            font=("Arial", 14, "bold"),
        ).pack(side="left")
        
        self.project_cb = ctk.CTkComboBox(
            content_frame,
            values=self.project_names,
            width=300,
            corner_radius=10,
            fg_color=self.COLOR_CARD_BG,
            state="readonly",
            # button_color="#1E2A3A",
            # button_hover_color="#2C3E50"
        )
        self.project_cb.set("Select project...")
        self.project_cb.grid(row=1, column=1, sticky="ew", pady=(0, 8))

        # Inline error label for project
        self.project_error_label = ctk.CTkLabel(
            content_frame,
            text="",
            text_color="#E74C3C",
            fg_color="transparent",
            font=("Arial", 10)
        )
        self.project_error_label.grid(row=2, column=1, sticky="w", padx=8, pady=(0, 8))

        # Date field - DO NOT allow past dates (allow_past=False)
        date_label_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        date_label_frame.grid(row=3, column=0, sticky="w", pady=(8, 4), padx=(0, 10))
        ctk.CTkLabel(
            date_label_frame,
            text="📅 Date",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).pack(side="left")
        ctk.CTkLabel(
            date_label_frame,
            text=" *",
            text_color="#E74C3C",
            font=("Arial", 14, "bold"),
        ).pack(side="left")
        
        self.date_ent = DatePickerButton(
            content_frame,
            initial_date=None, 
            allow_past=False
        )

        # Align to the left with padding to separate it from the previous widget
        self.date_ent.grid(row=4, column=0, sticky="w", padx=10, pady=(0, 8))

        # Inline error label for date
        self.date_error_label = ctk.CTkLabel(
            content_frame,
            text="",
            text_color="#E74C3C",
            fg_color="transparent",
            font=("Arial", 10)
        )
        self.date_error_label.grid(row=5, column=0, sticky="w", padx=16, pady=(0, 8))

        # Hours field
        hours_label_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        hours_label_frame.grid(row=3, column=1, sticky="w", pady=(8, 4))
        ctk.CTkLabel(
            hours_label_frame,
            text="⏱️ Hours",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).pack(side="left")
        ctk.CTkLabel(
            hours_label_frame,
            text=" *",
            text_color="#E74C3C",
            font=("Arial", 14, "bold"),
        ).pack(side="left")
        ctk.CTkLabel(
            hours_label_frame,
            text=" (1-8 hours)",
            font=("Arial", 12),
            anchor="w"
        ).pack(side="left")
        
        self.hours_ent = ctk.CTkEntry(content_frame, placeholder_text="e.g., 2.5 (1-8)", width=300, height=40)
        self.hours_ent.grid(row=4, column=1, sticky="ew", pady=(0, 8))

        # Inline error label for hours
        self.hours_error_label = ctk.CTkLabel(
            content_frame,
            text="",
            text_color="#E74C3C",
            fg_color="transparent",
            font=("Arial", 10)
        )
        self.hours_error_label.grid(row=5, column=1, sticky="w", padx=8, pady=(0, 8))

        # Reason field
        reason_label_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        reason_label_frame.grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 4))
        ctk.CTkLabel(
            reason_label_frame,
            text="💬 Reason / Tasks",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).pack(side="left")
        ctk.CTkLabel(
            reason_label_frame,
            text=" *",
            text_color="#E74C3C",
            font=("Arial", 14, "bold"),
        ).pack(side="left")
        
        self.reason_ent = ctk.CTkTextbox(content_frame, height=100, fg_color=self.COLOR_CARD_BG, border_width=1, border_color=self.COLOR_BORDER)
        self.reason_ent.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # Inline error label for reason
        self.reason_error_label = ctk.CTkLabel(
            content_frame,
            text="",
            text_color="#E74C3C",
            fg_color="transparent",
            font=("Arial", 10)
        )
        self.reason_error_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 8))

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
        self.hours_ent.delete(0, "end")
        self.reason_ent.delete("1.0", "end")

        # Clear any validation errors
        self._clear_field_error(self.member_cb)
        self._clear_field_error(self.project_cb)
        self._clear_field_error(self.date_ent.btn)
        self._clear_field_error(self.hours_ent)
        self._clear_field_error(self.reason_ent)
        # Also clear predefined inline labels
        try: self.member_error_label.configure(text="")
        except Exception: pass
        try: self.project_error_label.configure(text="")
        except Exception: pass
        try: self.date_error_label.configure(text="")
        except Exception: pass
        try: self.hours_error_label.configure(text="")
        except Exception: pass
        try: self.reason_error_label.configure(text="")
        except Exception: pass

    def _validate_add_form(self):
        is_valid = True

        # Clear previous errors (borders/dynamic labels)
        self._clear_field_error(self.member_cb)
        self._clear_field_error(self.project_cb)
        self._clear_field_error(self.date_ent.btn)
        self._clear_field_error(self.hours_ent)
        self._clear_field_error(self.reason_ent)
        # Clear predefined inline labels
        try: self.member_error_label.configure(text="")
        except Exception: pass
        try: self.project_error_label.configure(text="")
        except Exception: pass
        try: self.date_error_label.configure(text="")
        except Exception: pass
        try: self.hours_error_label.configure(text="")
        except Exception: pass
        try: self.reason_error_label.configure(text="")
        except Exception: pass
        
        # Validate member
        if self.member_cb.get() == "Select member..." or not self.member_cb.get().strip():
            try:
                self.member_cb.configure(border_color="#E74C3C", border_width=2)
            except Exception:
                pass
            try:
                self.member_error_label.configure(text="Please select a valid member")
            except Exception:
                pass
            is_valid = False
        
        # Validate project
        if self.project_cb.get() == "Select project..." or not self.project_cb.get().strip():
            try:
                self.project_cb.configure(border_color="#E74C3C", border_width=2)
            except Exception:
                pass
            try:
                self.project_error_label.configure(text="Please select a valid project")
            except Exception:
                pass
            is_valid = False

        # Validate hours
        try:
            hours_str = self.hours_ent.get()
            if not hours_str.strip():
                raise ValueError("Empty input")
            hours = float(hours_str)
            if not (1 <= hours <= 8):
                try:
                    self.hours_ent.configure(border_color="#E74C3C", border_width=2)
                except Exception:
                    pass
                try:
                    self.hours_error_label.configure(text="Hours must be between 1 and 8")
                except Exception:
                    pass
                is_valid = False
        except (ValueError, TypeError):
            try:
                self.hours_ent.configure(border_color="#E74C3C", border_width=2)
            except Exception:
                pass
            try:
                self.hours_error_label.configure(text="Please enter valid hours (e.g., 2.5, 4, 8)")
            except Exception:
                pass
            is_valid = False

        # Validate date
        ot_date = self.date_ent.get_date()
        if not ot_date:
            try:
                self.date_ent.btn.configure(border_color="#E74C3C", border_width=2)
            except Exception:
                pass
            try:
                self.date_error_label.configure(text="Please select a date")
            except Exception:
                pass
            is_valid = False
        elif ot_date < date.today():
            try:
                self.date_ent.btn.configure(border_color="#E74C3C", border_width=2)
            except Exception:
                pass
            try:
                self.date_error_label.configure(text="Cannot select a past date for overtime request!")
            except Exception:
                pass
            is_valid = False

        # Validate reason
        if not self.reason_ent.get("1.0", "end-1c").strip():
            try:
                self.reason_ent.configure(border_color="#E74C3C", border_width=2)
            except Exception:
                pass
            try:
                self.reason_error_label.configure(text="Please provide reason/tasks for overtime")
            except Exception:
                pass
            is_valid = False
            
        return is_valid

    def save_overtime(self):
        """Save the new overtime request"""
        if not self._validate_add_form():
            return

        member_name = self.member_cb.get()
        project_name = self.project_cb.get()
        member_id = self.member_map.get(member_name)
        project_id = self.project_map.get(project_name)
        hours = float(self.hours_ent.get())
        selected_date = self.date_ent.get_date()
        ot_date = selected_date.strftime('%Y-%m-%d')
        reason = self.reason_ent.get("1.0", "end-1c").strip()

        # Check for duplicate - only check for Pending and Accepted status (not Rejected or Cancelled)
        # NEW LOGIC: Total hours for the day must not exceed 8
        self.db.cursor.execute("""
            SELECT SUM(hours) as total_hours FROM overtime_requests 
            WHERE member_id = %s 
            AND DATE(ot_date) = %s
            AND status IN ('Pending', 'Accepted')
        """, (member_id, ot_date))
        result = self.db.cursor.fetchone()
        existing_hours = float(result['total_hours'] or 0)

        if existing_hours + hours > 8:
            remaining = 8 - existing_hours
            msg = f"Total OT cannot exceed 8 hours. {member_name} has {remaining:g}h remaining." if remaining > 0 else f"{member_name} reached 8h OT limit."
            self._show_message(msg, "warning")
            return

        # Save to database
        self.db.cursor.execute("""
            INSERT INTO overtime_requests
            (member_id, project_id, ot_date, hours, reason, status, created_by)
            VALUES (%s, %s, %s, %s, %s, 'Pending', %s)
        """, (member_id, project_id, ot_date, hours, reason, self.user['id']))

        # THIS PART TRIGGERS THE BADGE
        msg = f"New Overtime Request for {ot_date}."
        self.db.cursor.execute("""
            INSERT INTO notifications (user_id, message, is_read, created_at) 
            VALUES (%s, %s, 0, NOW())""", (member_id, msg))

        try:
            self.db.conn.commit()
            # No need to clear inline errors with the new system

            self._show_message(f"Overtime request for {member_name} has been submitted successfully!", "success")
            self.show_page("main")
        except Exception as e:
            self.db.conn.rollback()
            self._show_message(f"System Error: {e}", "error")

    def create_member_requests_page(self):
        # Create the Requests page with Pending / History tabs (copied UI pattern)
        self.member_requests_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.member_requests_page.grid_rowconfigure(2, weight=1)
        self.member_requests_page.grid_columnconfigure(0, weight=1)

        # Header with back button and segmented tab
        header = ctk.CTkFrame(self.member_requests_page, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=80, pady=(10, 10))

        back_btn = ctk.CTkButton(
            header,
            text="← Back",
            width=80,
            height = 36,
            fg_color=("#DBDBDB", "#333333"),
            text_color=("black", "white"),
            hover_color=("#CFCFCF", "#444444"),
            corner_radius=8,
            command=lambda: self.show_page("main")
        )
        back_btn.pack(side="left")

        self.member_segment = ctk.CTkSegmentedButton(
            header,
            values=["📋 Pending", "📜 History"],
            command=self._on_member_segment_change,
            font=("Arial", 13, "bold"),
            fg_color=self.COLOR_CONTAINER_BG,
            selected_color=("#3498DB", "#1F538D"),
            unselected_color=self.COLOR_CARD_BG,
            text_color=self.COLOR_TEXT_MAIN,
            corner_radius=12,
            height=36
        )
        self.member_segment.pack(side="right")
        self.member_segment.set("📋 Pending")

        # Content frames for Pending and History
        self.member_pending_frame = ctk.CTkScrollableFrame(
            self.member_requests_page,
            fg_color=self.COLOR_SCROLL_BG,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        self.member_history_frame = ctk.CTkScrollableFrame(
            self.member_requests_page,
            fg_color=self.COLOR_SCROLL_BG,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDER
        )

        # Default show pending
        self.member_pending_frame.grid(row=2, column=0, sticky="nsew", padx=80, pady=(0, 10))
        self.load_member_requests()

    def load_member_requests(self):
        """Dispatcher: load member requests according to current tab selection."""
        sel = getattr(self, 'member_segment', None)
        tab = sel.get() if sel else "📋 Pending"

        if tab == "📋 Pending":
            # show pending frame
            try:
                self.member_history_frame.grid_forget()
            except Exception:
                pass
            self.member_pending_frame.grid(row=2, column=0, sticky="nsew", padx=80, pady=(0, 10))
            self._load_member_pending()
        else:
            try:
                self.member_pending_frame.grid_forget()
            except Exception:
                pass
            self.member_history_frame.grid(row=2, column=0, sticky="nsew", padx=80, pady=(0, 10))
            self._load_member_history()
        
    def _load_member_pending(self):
        """Load pending requests created by members (exclude those created by this leader)."""
        # clear frame
        for w in self.member_pending_frame.winfo_children():
            w.destroy()

        query = """
            SELECT o.*, u.full_name, p.project_name
            FROM overtime_requests o
            JOIN users u ON o.member_id = u.id
            JOIN projects p ON o.project_id = p.id
            WHERE u.team_id = %s AND o.status = 'Pending' AND (o.created_by IS NULL OR o.created_by != %s)
            ORDER BY o.created_at DESC
        """
        self.db.cursor.execute(query, (self.team_id, self.user['id']))
        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(
                self.member_pending_frame,
                text="📭 No pending overtime requests from members.",
                font=("Arial", 14),
                text_color="#888888"
            ).pack(pady=40)
            return

        for row in rows:
            self._create_member_request_card(row, parent=self.member_pending_frame)

    def _load_member_history(self):
        """Load member-created requests with non-pending status."""
        for w in self.member_history_frame.winfo_children():
            w.destroy()

        query = """
            SELECT o.*, u.full_name, p.project_name
            FROM overtime_requests o
            JOIN users u ON o.member_id = u.id
            JOIN projects p ON o.project_id = p.id
            WHERE u.team_id = %s AND o.status != 'Pending' AND (o.created_by IS NULL OR o.created_by != %s)
            ORDER BY o.created_at DESC
        """
        self.db.cursor.execute(query, (self.team_id, self.user['id']))
        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(
                self.member_history_frame,
                text="📭 No history requests from members.",
                font=("Arial", 14),
                text_color="#888888"
            ).pack(pady=40)
            return

        for row in rows:
            self._create_member_request_card(row, parent=self.member_history_frame)

    def _on_member_segment_change(self, value):
        """Handle segment tab changes for member requests page."""
        try:
            self.member_segment.set(value)
        except Exception:
            pass
        self.load_member_requests()

    def _create_member_request_card(self, row, parent=None):
        """Creates a card for a member's overtime request inside `parent` frame."""
        parent = parent or getattr(self, 'member_pending_frame', self.member_requests_page)

        # Compact layout when rendering history cards to save vertical space
        compact = (parent is getattr(self, 'member_history_frame', None))
        card_pad_y = 6 if compact else 10
        content_padx = 12 if compact else 15
        content_pady = 8 if compact else 12
        top_row_pad = (0, 6) if compact else (0, 8)
        middle_row_pad = (0, 4) if compact else (0, 5)


        # For history cards, use a fixed compact height to reduce vertical size
        if compact:
            fixed_height = 120
            card = ctk.CTkFrame(
                parent,
                corner_radius=12,
                fg_color=self.COLOR_CONTAINER_BG,
                border_width=1,
                border_color=self.COLOR_BORDER,
                height=fixed_height
            )
            card.pack(fill="x", padx=12, pady=card_pad_y)
            # prevent the card resizing to children so height stays fixed
            try:
                card.pack_propagate(False)
            except Exception:
                pass
        else:
            card = ctk.CTkFrame(
                parent,
                corner_radius=12,
                fg_color=self.COLOR_CONTAINER_BG,
                border_width=1,
                border_color=self.COLOR_BORDER
            )
            card.pack(fill="x", padx=12, pady=card_pad_y)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=content_padx, pady=content_pady)

        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)

        # Top row: Name and date
        top_row = ctk.CTkFrame(left, fg_color="transparent")
        top_row.pack(fill="x", pady=top_row_pad)

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
        middle_row.pack(fill="x", pady=middle_row_pad)

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

        # Reason (if available) - shorten preview when compact
        if row.get('reason') and row['reason'].strip():
            max_len = 80 if compact else 100
            reason_text = row['reason'][:max_len] + ("..." if len(row['reason']) > max_len else "")
            ctk.CTkLabel(
                left,
                text=f"💬 {reason_text}",
                font=("Arial", 11),
                text_color="#888888",
                anchor="w"
            ).pack(fill="x", pady=(4 if compact else 5, 0))

        # Right side - Status Badge and Action Buttons
        right_section = ctk.CTkFrame(content, fg_color="transparent")
        right_section.pack(side="right", fill="y")

        # Use an internal grid inside right_section so we can vertically center the badge
        try:
            right_section.grid_rowconfigure(0, weight=1)
            right_section.grid_columnconfigure(0, weight=1)
        except Exception:
            pass

        middle_container = ctk.CTkFrame(right_section, fg_color="transparent")
        # place the middle_container to fill available space so child can center
        try:
            middle_container.grid(row=0, column=0, sticky="nsew")
        except Exception:
            # fallback to pack if grid not available for some reason
            middle_container.pack(expand=True, fill="both")

        status_config = {
            "Pending": {"color": "#F39C12", "bg": "#3D2E1A", "icon": "⏳", "text": "Pending"},
            "Accepted": {"color": "#27AE60", "bg": "#1A3D2A", "icon": "✓", "text": "Accepted"},
            "Approved": {"color": "#2ECC71", "bg": "#1A4D2A", "icon": "✓", "text": "Approved"},
            "Rejected": {"color": "#E74C3C", "bg": "#4A1A1A", "icon": "✗", "text": "Rejected"},
            "Cancelled": {"color": "#95A5A6", "bg": "#2A3A3A", "icon": "⊗", "text": "Cancelled"}
        }
        config = status_config.get(row['status'], {"color": "#AAAAAA", "bg": "#2A2A2A", "icon": "•", "text": row['status']})

        # badge sizing depends on compact mode
        badge_h = 24 if compact else 30
        badge_w = 90 if compact else 100
        badge_pad_bottom = (0, 6) if compact else (0, 10)

        # create an inner frame that will be centered inside middle_container
        inner = ctk.CTkFrame(middle_container, fg_color="transparent")
        inner.pack(expand=True)

        # If this is the member pending page and the request is Pending, skip rendering the status badge
        skip_badge_on_pending = (row['status'] == 'Pending' and parent is getattr(self, 'member_pending_frame', None))

        if not skip_badge_on_pending:
            badge_frame = ctk.CTkFrame(
                inner,
                fg_color=config['bg'],
                corner_radius=15,
                height=badge_h,
                width=badge_w
            )
            badge_frame.pack()
            try:
                badge_frame.pack_propagate(False)
            except Exception:
                pass

            badge_content = ctk.CTkFrame(badge_frame, fg_color="transparent")
            badge_content.pack(expand=True, fill="both", padx=10, pady=5)

            ctk.CTkLabel(
                badge_content,
                text=f"{config['icon']} {config['text']}",
                font=("Arial", 11, "bold"),
                text_color=config['color']
            ).pack()

        action_frame = ctk.CTkFrame(inner, fg_color="transparent")
        action_frame.pack()

        # For member requests page, leader can Approve/Reject pending requests
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

                # Also add to sec_notifications for the member's internal badge
                self.db.cursor.execute("""
                    INSERT INTO sec_notifications (user_id, message, is_read, created_at)
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
                self._update_member_request_status(request_id, 'Rejected', reason)
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

    def create_edit_page(self):
        self.edit_page = ctk.CTkFrame(self.pages, fg_color="transparent")
        self.edit_page.grid_rowconfigure(1, weight=1)
        self.edit_page.grid_columnconfigure(0, weight=1)
        
        # Back button
        back_btn = ctk.CTkButton(
            self.edit_page,
            text="← Back",
            width=80,
            height=36,
            fg_color=("#DBDBDB", "#333333"),
            text_color=("black", "white"),
            hover_color=("#CFCFCF", "#444444"),
            corner_radius=8,
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

        # Reason field
        is_editable = (row['status'] == 'Pending' and row['ot_date'] >= date.today())
        reason_label_text = "💬 Reason / Tasks:" if is_editable else "💬 Original Reason:"

        ctk.CTkLabel(
            content_frame,
            text=reason_label_text,
            font=("Arial", 13, "bold"),
            text_color="#AAAAAA"
        ).grid(row=4, column=0, sticky="w", pady=(15, 5))
        
        self.edit_reason = ctk.CTkTextbox(
            content_frame,
            height=100,
            fg_color=self.COLOR_CARD_BG,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        self.edit_reason.grid(row=5, column=0, sticky="ew", pady=(0, 15))
        self.edit_reason.insert("1.0", row['reason'] if row['reason'] else ("" if is_editable else "-"))
        
        if not is_editable:
            self.edit_reason.configure(state="disabled")

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
                    text="← Back",
                    width=80,
                    height = 36,
                    fg_color=("#DBDBDB", "#333333"),
                    text_color=("black", "white"),
                    hover_color=("#CFCFCF", "#444444"),
                    corner_radius=8,
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
            if not (1 <= hours <= 8):
                self._show_message("Hours must be between 1 and 8", "error")
                return
        except ValueError:
            self._show_message("Please enter valid hours (e.g., 2.5, 4, 8)", "error")
            return

        try:
            self.db.cursor.execute("SELECT member_id, DATE(ot_date) as ot_date FROM overtime_requests WHERE id = %s", (ot_id,))
            info = self.db.cursor.fetchone()
            if info:
                self.db.cursor.execute("""
                    SELECT SUM(hours) as total_hours FROM overtime_requests
                    WHERE member_id = %s AND DATE(ot_date) = %s AND status IN ('Pending', 'Accepted') AND id != %s
                """, (info['member_id'], info['ot_date'], ot_id))
                
                other_hours = float(self.db.cursor.fetchone()['total_hours'] or 0)
                
                if other_hours + hours > 8:
                    self._show_message(f"Daily limit exceeded. Remaining: {8-other_hours:g}h", "error")
                    return
        except Exception: pass

        reason = self.edit_reason.get("1.0", "end-1c").strip()
        if not reason:
            self._show_message("Reason field is required.", "error")
            return

        try:
            self.db.cursor.execute("""
                UPDATE overtime_requests
                SET hours = %s, reason = %s
                WHERE id = %s AND status = 'Pending'
            """, (hours, reason, ot_id))
            
            # Notify Member of the update
            self.db.cursor.execute("SELECT member_id, ot_date FROM overtime_requests WHERE id = %s", (ot_id,))
            req_info = self.db.cursor.fetchone()
            if req_info:
                notif_msg = f"overtime request for {req_info['ot_date']} was updated by Leader."
                self.db.cursor.execute("""
                    INSERT INTO notifications (user_id, message, is_read, created_at)
                    VALUES (%s, %s, 0, NOW())
                """, (req_info['member_id'], notif_msg))

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

    def refresh_button_badge(self):
        """Update the badge on the 'Request OT from member' button"""
        try:
            self.db.cursor.execute(
                "SELECT COUNT(*) as cnt FROM sec_notifications "
                "WHERE user_id = %s AND is_read = 0 "
                "AND message LIKE '%%overtime request submitted%%'", (self.user['id'],)
            )
            count = self.db.cursor.fetchone()['cnt']
            
            if count > 0:
                self.btn_badge.configure(text=str(count))
                self.btn_badge.place(relx=0.9, rely=0.5, anchor="center")
            else:
                self.btn_badge.place_forget()
        except Exception as e:
            print(f"Error refreshing button badge: {e}")

    def mark_member_requests_as_read(self):
        """Mark member submission notifications as read in DB"""
        try:
            self.db.cursor.execute(
                "UPDATE sec_notifications SET is_read = 1 "
                "WHERE user_id = %s AND message LIKE '%%overtime request submitted%%'", (self.user['id'],)
            )
            self.db.conn.commit()
            self.refresh_button_badge()
        except Exception as e:
            print(f"Error marking button notifs as read: {e}")

    def auto_refresh(self):
        """Keep the button badge updated in the background"""
        if self._is_destroyed:
            return
            
        self.refresh_button_badge()
        
        # Check for new submissions every 10 seconds
        self._after_id = self.after(10000, self.auto_refresh)

    def refresh_ui(self):
        """Refresh the main list view"""
        self.refresh_button_badge()
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
        else:
            # If status is All or not specified, show all statuses by default
            pass

        # Restrict leader view to members in the leader's team
        query += " AND u.team_id = %s AND u.role = 'member'"
        params.append(self.team_id)

        # Only show requests that were created by this leader
        query += " AND o.created_by = %s"
        params.append(self.user['id'])

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
                    corner_radius=8,
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
                        corner_radius=8,
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

    def destroy(self):
        """Clean up background tasks"""
        self._is_destroyed = True
        if self._after_id:
            self.after_cancel(self._after_id)
        super().destroy()