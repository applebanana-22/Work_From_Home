
import customtkinter as ctk
from database import Database
from tkinter import messagebox, simpledialog
from datetime import datetime

# Configure global CustomTkinter appearance settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


# --- Leave Detail Popup Window (Premium Enterprise UI) ---
class LeaveDetailWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, request_id, leave_type, total_days, date_range, start_date, end_date, start_shift, end_shift, reason=""):
        super().__init__(parent)
        self.title("Leave Request Detail Breakdown")
        self.geometry("480x620")
        self.resizable(False, False)
        self.configure(fg_color=("#F8FAFC", "#0F172A"))  # Slate Light/Dark Background
        
        # Center window on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (480 // 2)
        y = (self.winfo_screenheight() // 2) - (620 // 2)
        self.geometry(f"+{x}+{y}")
        
        self.attributes("-topmost", True)
        self.grab_set()
        self.db = db

        self.protocol("WM_DELETE_WINDOW", self.safe_close)

        # Header Section
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(30, 15), padx=28)
        
        ctk.CTkLabel(header_frame, text="📋 Day-by-Day Breakdown", 
                     font=("Segoe UI", 22, "bold"), 
                     text_color=("#1E293B", "#F1F5F9")).pack(anchor="w")
        
        ctk.CTkLabel(header_frame, text="Detailed schedule of the requested leave period.", 
                     font=("Segoe UI", 12), 
                     text_color=("#64748B", "#94A3B8")).pack(anchor="w", pady=(4, 0))
        
        # Info Summary Card
        info_frame = ctk.CTkFrame(self, fg_color=("#FFFFFF", "#1E293B"), 
                                  border_width=1, border_color=("#E2E8F0", "#334155"), 
                                  corner_radius=16)
        info_frame.pack(fill="x", padx=28, pady=5)
        
        day_str = "Day" if float(total_days) <= 1.0 else "Days"
        
        ctk.CTkLabel(info_frame, text=f"Type: {leave_type}", font=("Segoe UI", 14, "bold"), text_color=("#334155", "#CBD5E1")).pack(anchor="w", padx=20, pady=(16, 4))
        ctk.CTkLabel(info_frame, text=f"Duration: {date_range}", font=("Segoe UI", 12), text_color=("#64748B", "#94A3B8")).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(info_frame, text=f"Total Leave: {total_days} {day_str}", font=("Segoe UI", 16, "bold"), text_color="#10B981").pack(anchor="w", padx=20, pady=(4, 16))

        # Reason Display Section
        if reason:
            r_frame = ctk.CTkFrame(self, fg_color="transparent")
            r_frame.pack(fill="x", padx=28, pady=12)
            ctk.CTkLabel(r_frame, text="📄 Reason for Leave:", font=("Segoe UI", 12, "bold"), text_color=("#475569", "#94A3B8")).pack(anchor="w", pady=(0, 6))
            
            r_box = ctk.CTkTextbox(r_frame, height=65, fg_color=("#FFFFFF", "#1E293B"), 
                                   border_width=1, border_color=("#E2E8F0", "#334155"), 
                                   corner_radius=10, font=("Segoe UI", 12))
            r_box.insert("1.0", reason)
            r_box.configure(state="disabled")
            r_box.pack(fill="x")

        # Scrollable Breakdown List
        self.list_frame = ctk.CTkScrollableFrame(self, width=410, height=200, 
                                                label_text="Detailed Breakdown Log", 
                                                fg_color=("#FFFFFF", "#1E293B"), 
                                                label_text_color=("#475569", "#94A3B8"),
                                                label_font=("Segoe UI", 12, "bold"), 
                                                border_width=1, border_color=("#E2E8F0", "#334155"),
                                                corner_radius=12)
        self.list_frame.pack(padx=28, pady=10, fill="both", expand=True)
        
        self.load_day_details(request_id)
        
        # Close Button
        ctk.CTkButton(self, text="Close Window", fg_color=("#EF4444", "#DC2626"), hover_color=("#DC2626", "#B91C1C"), 
                      font=("Segoe UI", 13, "bold"), height=44, corner_radius=10, command=self.safe_close).pack(pady=25, padx=28, fill="x")

    def load_day_details(self, request_id):
        try:
            sql = "SELECT leave_date, shift_status FROM leave_details WHERE request_id = %s ORDER BY leave_date ASC"
            self.db.cursor.execute(sql, (request_id,))
            rows = self.db.cursor.fetchall()
            
            for row in rows:
                l_date = row['leave_date']
                date_str = l_date.strftime("%Y-%m-%d") if hasattr(l_date, 'strftime') else str(l_date)
                shift = row['shift_status']
                
                row_frame = ctk.CTkFrame(self.list_frame, fg_color=("#F8FAFC", "#0F172A"), height=45, corner_radius=10, border_width=1, border_color=("#E2E8F0", "#1E293B"))
                row_frame.pack(fill="x", pady=4, padx=5)
                
                icon = "☀️" if shift == "Morning" else "🌙" if shift == "Evening" else "📅"
                color = "#F59E0B" if shift == "Morning" else "#8B5CF6" if shift == "Evening" else "#3B82F6"
                
                ctk.CTkLabel(row_frame, text=f"   {icon}   {date_str}", font=("Segoe UI", 13, "bold"), text_color=("#1E293B", "#F1F5F9")).pack(side="left", padx=15)
                ctk.CTkLabel(row_frame, text=shift, font=("Segoe UI", 12, "bold"), text_color=color).pack(side="right", padx=15)
        except Exception as e:
            print(f"Error loading breakdown: {e}")

    def safe_close(self):
        self.grab_release()
        self.withdraw()
        self.after(100, self.destroy)


# --- Leader Dashboard Frame ---
class LeaderLeaveManage(ctk.CTkFrame):
    def __init__(self, master, user, sidebar_ref=None):
        super().__init__(master, fg_color="transparent")
        
        self.db = Database()
        self.user = user
        self.sidebar_ref = sidebar_ref
        self._is_destroyed = False
        self._after_id = None
        
        # Automatic Theme Constants (Tuples) - matching overtime design
        self.COLOR_CARD_BG = ("#FFFFFF", "#1E1E1E")
        self.COLOR_BORDER = ("#DBDBDB", "#2C2C2C")
        self.COLOR_TEXT_MAIN = ("#1A1A2A", "#E8EDF2")
        self.COLOR_TEXT_SEC = ("#555555", "#AAB7C4")
        self.COLOR_SCROLL_BG = ("#F5F5F5", "#1A1A1A")
        self.COLOR_CONTAINER_BG = ("#F0F0F0", "#252525")

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=60, pady=(5, 15))
        self.container.grid_columnconfigure(0, weight=1)
        
        self.show_management_view()
        
        # Start background polling for new requests
        self.auto_refresh()

    def clear_view(self):
        for widget in self.container.winfo_children(): 
            widget.destroy()

    def create_header(self, title, subtitle, show_back=False):
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(5, 10))
        
        if show_back:
            ctk.CTkButton(
                header, text="← Back", width=80, height=36,
                fg_color=("#DBDBDB", "#333333"), text_color=("black", "white"),
                hover_color=("#CFCFCF", "#444444"), corner_radius=8,
                command=self.show_management_view
            ).pack(side="left", padx=(0, 15))

        text_f = ctk.CTkFrame(header, fg_color="transparent")
        text_f.pack(side="left", fill="y")
        ctk.CTkLabel(text_f, text=title, font=("Arial", 20, "bold"), text_color=self.COLOR_TEXT_MAIN).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(text_f, text=subtitle, font=("Arial", 12), text_color=self.COLOR_TEXT_SEC).pack(anchor="w")

    def show_management_view(self):
        self.clear_view()
        self.container.grid_rowconfigure(2, weight=1)

        self.create_header("Team Leave Control", "Real-time management of team leave requests")

        # --- View Switcher ---
        self.view_switch = ctk.CTkSegmentedButton(
            self.container,
            values=["📋 Pending Approval", "📜 Decision Log"],
            command=self.on_view_change,
            font=("Arial", 13, "bold"),
            fg_color=self.COLOR_CONTAINER_BG,
            selected_color=("#3498DB", "#1F538D"),
            unselected_color=self.COLOR_CARD_BG,
            text_color=self.COLOR_TEXT_MAIN,
            corner_radius=12,
            height=40
        )
        self.view_switch.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.view_switch.set("📋 Pending Approval")

        # --- Badge for Switcher (Added for Decision Log) ---
        self.decision_tab_badge = ctk.CTkLabel(self.view_switch, text="", font=("Arial", 10, "bold"), fg_color="#E74C3C", text_color="white", width=20, height=20, corner_radius=10)
        self.decision_tab_badge.place_forget()

        # --- Main Grid Layout ---
        self.main_grid = ctk.CTkFrame(self.container, fg_color="transparent")
        self.main_grid.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self.main_grid.grid_columnconfigure(0, weight=1)
        self.main_grid.grid_columnconfigure(1, weight=1)
        self.main_grid.grid_rowconfigure(0, weight=1)

        # --- Left Column: Pending Approval ---
        self.pending_container = ctk.CTkFrame(self.main_grid, fg_color="transparent")
        self.pending_container.grid_rowconfigure(1, weight=1)
        self.pending_container.grid_columnconfigure(0, weight=1)

        pending_header = ctk.CTkFrame(self.pending_container, fg_color="transparent")
        pending_header.grid(row=0, column=0, sticky="w", pady=(0, 10))
        ctk.CTkLabel(pending_header, text="📋 Pending Approval", font=("Arial", 16, "bold"), text_color=self.COLOR_TEXT_MAIN).pack(side="left")

        self.pending_badge = ctk.CTkLabel(pending_header, text="", font=("Arial", 10, "bold"), fg_color="#E74C3C", text_color="white", width=20, height=20, corner_radius=10)
        self.pending_badge.pack_forget()
        
        self.scroll_f = ctk.CTkScrollableFrame(self.pending_container, fg_color=self.COLOR_SCROLL_BG, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
        self.scroll_f.grid(row=1, column=0, sticky="nsew")

        # --- Right Column: Decision Log ---
        self.history_container = ctk.CTkFrame(self.main_grid, fg_color="transparent")
        self.history_container.grid_rowconfigure(1, weight=1)
        self.history_container.grid_columnconfigure(0, weight=1)

        history_header = ctk.CTkFrame(self.history_container, fg_color="transparent")
        history_header.grid(row=0, column=0, sticky="w", pady=(0, 10))
        ctk.CTkLabel(history_header, text="📜 Decision Log", font=("Arial", 16, "bold"), text_color=self.COLOR_TEXT_MAIN).pack(side="left")

        self.history_badge = ctk.CTkLabel(history_header, text="", font=("Arial", 10, "bold"), fg_color="#E74C3C", text_color="white", width=20, height=20, corner_radius=10)
        self.history_badge.pack_forget()

        self.history_scroll = ctk.CTkScrollableFrame(self.history_container, fg_color=self.COLOR_SCROLL_BG, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
        self.history_scroll.grid(row=1, column=0, sticky="nsew")

        # Initial State
        self.mark_pending_as_read()
        self.on_view_change("📋 Pending Approval")
        self.load_pending_requests()
        self.load_full_history()

    def on_view_change(self, value):
        """Handles switching between pending and decision log views"""
        if value == "📋 Pending Approval":
            self.history_container.grid_forget()
            self.pending_container.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0)
            self.main_grid.grid_columnconfigure(0, weight=1)
            self.main_grid.grid_columnconfigure(1, weight=0)
            self.mark_pending_as_read()
        elif value == "📜 Decision Log":
            self.pending_container.grid_forget()
            self.history_container.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0)
            self.main_grid.grid_columnconfigure(0, weight=0)
            self.main_grid.grid_columnconfigure(1, weight=1)
            self.mark_decision_as_read()

    def load_pending_requests(self):
        for w in self.scroll_f.winfo_children(): w.destroy()
        try:
            self.db.ensure_connection()
            sql = """SELECT lr.*, u.full_name FROM leave_requests lr 
                     JOIN users u ON lr.user_id = u.id 
                     WHERE u.team_id = %s
                     AND lr.status = 'Pending' 
                     ORDER BY lr.created_at DESC"""
            self.db.cursor.execute(sql, (self.user['team_id'],))
            rows = self.db.cursor.fetchall()

            if not rows:
                empty_frame = ctk.CTkFrame(self.scroll_f, fg_color="transparent")
                empty_frame.pack(pady=100, fill="both", expand=True)
                ctk.CTkLabel(empty_frame, text="✨", font=("Arial", 48)).pack()
                ctk.CTkLabel(empty_frame, text="All caught up! No pending requests.", 
                             font=("Arial", 14), text_color=self.COLOR_TEXT_SEC).pack(pady=8)
                return

            for r in rows:
                card = ctk.CTkFrame(self.scroll_f, fg_color=self.COLOR_CARD_BG, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
                card.pack(fill="x", pady=8, padx=5)
                
                inner = ctk.CTkFrame(card, fg_color="transparent")
                inner.pack(fill="x", padx=15, pady=15)

                info = ctk.CTkFrame(inner, fg_color="transparent")
                info.pack(side="left", fill="y")
                ctk.CTkLabel(info, text=r['full_name'].upper(), font=("Arial", 16, "bold"), text_color=self.COLOR_TEXT_MAIN).pack(anchor="w")
                
                req_time = r['created_at'].strftime("%Y-%m-%d %I:%M %p") if r['created_at'] else "N/A"
                ctk.CTkLabel(info, text=f"🕒 Applied: {req_time}", font=("Arial", 11, "bold"), text_color="#F39C12").pack(anchor="w", pady=(3, 6))
                
                day_word = "Day" if float(r['total_days']) <= 1.0 else "Days"
                date_range_str = f"{r['start_date']} — {r['end_date']}"
                ctk.CTkLabel(info, text=f"{r['leave_type']}  •  {r['total_days']} {day_word}", 
                             font=("Arial", 13, "bold"), text_color="#3498DB").pack(anchor="w")

                btn_box = ctk.CTkFrame(inner, fg_color="transparent")
                btn_box.pack(side="right", anchor="center")
                
                ctk.CTkButton(btn_box, text="Approve", width=100, height=38, fg_color="#10B981", 
                              hover_color="#059669", font=("Arial", 12, "bold"), corner_radius=10,
                              command=lambda x=r['id']: self.update_status(x, 'Approved')).pack(side="left", padx=5)
                
                ctk.CTkButton(btn_box, text="Reject", width=100, height=38, fg_color="#EF4444", 
                              hover_color="#DC2626", font=("Arial", 12, "bold"), corner_radius=10,
                              command=lambda x=r['id']: self.update_status(x, 'Rejected')).pack(side="left", padx=5)
                
                self.setup_card_events(card, inner, info, r, date_range_str)

        except Exception as e: 
            print(f"Load Error: {e}")

    def refresh_all_data(self):
        self.load_pending_requests()
        self.load_full_history()
        self.refresh_badges()

    def refresh_badges(self):
        """Refresh both internal badges"""
        self.refresh_pending_badge()
        self.refresh_decision_badge()

    def refresh_pending_badge(self):
        """Check for unread member leave requests in notifications"""
        try:
            self.db.cursor.execute(
                "SELECT COUNT(*) as cnt FROM notifications "
                "WHERE user_id = %s AND is_read = 0 "
                "AND message LIKE '%%requested%%leave%%'", (self.user['id'],)
            )
            count = self.db.cursor.fetchone()['cnt']
            
            if count > 0:
                self.pending_badge.configure(text=str(count))
                self.pending_badge.pack(side="left", padx=10)
            else:
                self.pending_badge.pack_forget()
        except: pass

    def refresh_decision_badge(self):
        """Check for unread decisions (useful for teams with multiple leaders) in notifications"""
        try:
            self.db.cursor.execute(
                "SELECT COUNT(*) as cnt FROM notifications "
                "WHERE user_id = %s AND is_read = 0 "
                "AND (message LIKE '%%Approved%%' OR message LIKE '%%Rejected%%')", 
                (self.user['id'],)
            )
            count = self.db.cursor.fetchone()['cnt']
            
            if count > 0:
                self.history_badge.configure(text=str(count))
                self.history_badge.pack(side="left", padx=10)
                
                # Also update segmented button badge position (right side)
                self.decision_tab_badge.configure(text=str(count))
                self.decision_tab_badge.place(relx=0.95, rely=0.5, anchor="center")
            else:
                self.history_badge.pack_forget()
                self.decision_tab_badge.place_forget()
        except: pass

    def mark_pending_as_read(self):
        """Mark pending leave request notifications as read in notifications"""
        try:
            self.db.cursor.execute(
                "UPDATE notifications SET is_read = 1 "
                "WHERE user_id = %s AND message LIKE '%%requested%%leave%%'", (self.user['id'],)
            )
            self.db.conn.commit()
            self.refresh_pending_badge()
        except: pass

    def mark_decision_as_read(self):
        """Mark decision log notifications as read in notifications"""
        try:
            self.db.cursor.execute(
                "UPDATE notifications SET is_read = 1 "
                "WHERE user_id = %s AND (message LIKE '%%Approved%%' OR message LIKE '%%Rejected%%')",
                (self.user['id'],)
            )
            self.db.conn.commit()
            self.refresh_decision_badge()
        except: pass

    def auto_refresh(self):
        if self._is_destroyed: return
        self.refresh_badges()
        self._after_id = self.after(10000, self.auto_refresh)

    def setup_card_events(self, card, inner, info, data, date_range_str):
        def on_enter(e):
            card.configure(border_color=("#3498DB", "#1F538D"))
        def on_leave(e):
            card.configure(border_color=self.COLOR_BORDER)
            
        for w in [card, inner, info]:
            w.configure(cursor="hand2")
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", lambda event, req_id=data['id'], l_type=data['leave_type'], t_days=data['total_days'],
                                                 d_range=date_range_str, s_d=data['start_date'], e_d=data['end_date'],
                                                 s_s=data['start_shift'], e_s=data['end_shift'], rsn=data['reason']:
                                  self.open_detail_window(req_id, l_type, t_days, d_range, s_d, e_d, s_s, e_s, rsn))

    def open_detail_window(self, request_id, leave_type, total_days, date_range, start_date, end_date, start_shift, end_shift, reason):
        LeaveDetailWindow(self, self.db, request_id, leave_type, total_days, date_range, start_date, end_date, start_shift, end_shift, reason)

    def _show_message(self, message, message_type="info", duration=3000):
        if message_type == "error":
            bg_color = "#E74C3C"
        elif message_type == "warning":
            bg_color = "#F39C12"
        elif message_type == "success":
            bg_color = "#27AE60"
        else:
            bg_color = "#3498DB"

        message_frame = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color=bg_color,
            corner_radius=8
        )
        message_frame.place(relx=1.0, rely=0, x=-20, y=20, anchor="ne")

        ctk.CTkLabel(
            message_frame,
            text=message,
            text_color="white",
            font=("Arial", 12, "bold"),
            wraplength=250
        ).pack(padx=15, pady=10)

        self.after(duration, message_frame.destroy)

    def update_status(self, req_id, status):
        if not messagebox.askyesno("Confirm Action", f"Are you sure you want to {status.lower()} this request?"):
            return
            
        leader_reason = ""
        if status == "Rejected":
            leader_reason = simpledialog.askstring("Reason Required", "Please enter the reason for rejection:", parent=self)
            if leader_reason is None: 
                return
            
            leader_reason = leader_reason.strip()
            if not leader_reason:
                self._show_message("Rejection reason cannot be empty.", "warning")
                return

        try:
            self.db.ensure_connection()
            
            sql_update = "UPDATE leave_requests SET status = %s, leader_reason = %s, updated_at = NOW() WHERE id = %s"
            self.db.cursor.execute(sql_update, (status, leader_reason, req_id))
            
            self.db.cursor.execute("SELECT user_id, leave_type FROM leave_requests WHERE id = %s", (req_id,))
            res_data = self.db.cursor.fetchone()
            
            if not res_data:
                self._show_message("Request records could not be found.", "error")
                return
                
            target_user = res_data['user_id']
            l_type = res_data['leave_type']

            if status == "Rejected":
                msg = f"❌ Your {l_type} request was Rejected. Reason: {leader_reason}"
            else:
                msg = f"✅ Your {l_type} request has been Approved by Team Leader."
                
            self.db.cursor.execute("""INSERT INTO notifications (user_id, message, is_read, created_at) 
                                     VALUES (%s, %s, 0, NOW())""", (target_user, msg))
            
            # Notify other team leaders in notifications so they see it in their Decision Log
            self.db.cursor.execute("""INSERT INTO notifications (user_id, message, is_read, created_at) 
                                     SELECT id, %s, 0, NOW() FROM users 
                                     WHERE role = 'leader' AND team_id = %s AND id != %s""", 
                                  (msg, self.user['team_id'], self.user['id']))

            self.db.conn.commit()
            
            self._show_message(f"Request {status.lower()}ed successfully.", "success")
            self.show_management_view()
            
        except Exception as e: 
            self._show_message(f"Database Error: {str(e)}", "error")

    def load_full_history(self):
        try:
            self.db.ensure_connection()
            self.db.cursor.execute("""SELECT lr.*, u.full_name FROM leave_requests lr 
                                      JOIN users u ON lr.user_id = u.id 
                                      WHERE u.team_id = %s AND lr.status != 'Pending' 
                                      ORDER BY lr.id DESC""", (self.user['team_id'],))
            rows = self.db.cursor.fetchall()
            
            if not rows:
                empty_frame = ctk.CTkFrame(self.history_scroll, fg_color="transparent")
                empty_frame.pack(pady=100, fill="both", expand=True)
                ctk.CTkLabel(empty_frame, text="No records found in activity log.", font=("Arial", 14), text_color=self.COLOR_TEXT_SEC).pack()
                return

            for r in rows:
                card = ctk.CTkFrame(self.history_scroll, fg_color=self.COLOR_CARD_BG, corner_radius=12, border_width=1, border_color=self.COLOR_BORDER)
                card.pack(fill="x", pady=6, padx=5)
                
                is_approved = r['status'] == "Approved"
                color = "#10B981" if is_approved else "#EF4444"
                badge_bg = ("#E6F4EA", "#064E3B") if is_approved else ("#FCE8E6", "#7F1D1D")
                
                inner = ctk.CTkFrame(card, fg_color="transparent")
                inner.pack(fill="x", padx=15, pady=12)
                
                left = ctk.CTkFrame(inner, fg_color="transparent")
                left.pack(side="left", fill="y")
                
                ctk.CTkLabel(left, text=r['full_name'].upper(), font=("Arial", 14, "bold"), text_color=self.COLOR_TEXT_MAIN).pack(anchor="w")
                
                req_t = r['created_at'].strftime("%b %d, %Y at %I:%M %p") if r['created_at'] else "N/A"
                ctk.CTkLabel(left, text=f"Requested on: {req_t}", font=("Arial", 11), text_color=self.COLOR_TEXT_SEC).pack(anchor="w", pady=(1, 4))
                
                day_word = "day" if float(r['total_days']) <= 1.0 else "days"
                date_range_str = f"{r['start_date']} to {r['end_date']}"
                ctk.CTkLabel(left, text=f"{r['leave_type']}  •  {r['total_days']} {day_word} ({date_range_str})", 
                             font=("Arial", 12, "bold"), text_color=("#555555", "#AAB7C4")).pack(anchor="w")
                
                if r.get('leader_reason'):
                    ctk.CTkLabel(left, text=f"💬 Reason: {r['leader_reason']}", font=("Arial", 12, "italic"), text_color=color).pack(anchor="w", pady=(4,0))
                
                badge_f = ctk.CTkFrame(inner, fg_color=badge_bg, corner_radius=12)
                badge_f.pack(side="right", anchor="center")
                ctk.CTkLabel(badge_f, text=r['status'].upper(), font=("Arial", 11, "bold"), text_color=color, padx=14, pady=6).pack()

                self.setup_card_events(card, inner, left, r, date_range_str)
                
        except Exception as e: 
            print(f"History Load Error: {e}")

    def destroy(self):
        self._is_destroyed = True
        if self._after_id:
            self.after_cancel(self._after_id)
        super().destroy()
