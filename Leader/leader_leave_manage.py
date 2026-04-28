import customtkinter as ctk
from database import Database
from tkinter import messagebox
from datetime import datetime

class LeaderLeaveManage(ctk.CTkFrame):
    def __init__(self, master, user, sidebar_ref=None):
        # Background: White for Light Mode, Deep Charcoal for Dark Mode
        super().__init__(master, fg_color=("#FFFFFF", "#121212"))
        
        self.db = Database()
        self.user = user
        self.sidebar_ref = sidebar_ref
        
        # Define Universal Color Tuples
        self.text_main = ("#000000", "#FFFFFF")
        self.text_sub = ("#555555", "#888888")
        self.card_bg = ("#F9F9F9", "#1A1A1A")
        self.card_border = ("#E0E0E0", "#2D2D2D")

        # Main Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=30)
        
        self.show_management_view()

    def clear_view(self):
        for widget in self.container.winfo_children(): 
            widget.destroy()

    def create_header(self, title, subtitle, show_back=False):
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        left_side = ctk.CTkFrame(header, fg_color="transparent")
        left_side.pack(side="left")
        
        if show_back:
            ctk.CTkButton(left_side, text="←", width=35, height=35, 
                          fg_color=("#E0E0E0", "#2D2D2D"), 
                          text_color=self.text_main,
                          hover_color=("#D0D0D0", "#3D3D3D"), 
                          command=self.show_management_view).pack(side="left", padx=(0, 15))
            
        ctk.CTkLabel(left_side, text=title, font=("Segoe UI", 32, "bold"), 
                     text_color=self.text_main).pack(anchor="w")
        ctk.CTkLabel(left_side, text=subtitle, font=("Segoe UI", 14), 
                     text_color=self.text_sub).pack(anchor="w")

        right_side = ctk.CTkFrame(header, fg_color="transparent")
        right_side.pack(side="right", pady=5)

        if not show_back:
            self.noti_btn = ctk.CTkButton(
                right_side, text="🔔 History", width=110, height=45, 
                fg_color=self.card_bg, border_width=1, border_color=self.card_border,
                text_color=self.text_main,
                hover_color=("#EEEEEE", "#2D2D2D"), font=("Segoe UI", 13, "bold"),
                corner_radius=12, command=self.show_activity_history
            )
            self.noti_btn.pack(side="right", padx=10)

        refresh_cmd = self.show_management_view if not show_back else self.show_activity_history
        ctk.CTkButton(right_side, text="🔄 Refresh", font=("Segoe UI", 13, "bold"), 
                      fg_color="#6264A7", hover_color="#4F5191", height=45, width=100,
                      corner_radius=12, command=refresh_cmd).pack(side="right")

    def show_management_view(self):
        self.clear_view()
        self.create_header("Waiting Approval", "Manage your team's leave requests")
        
        self.scroll_f = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.scroll_f.pack(fill="both", expand=True)
        self.load_pending_requests()

    def load_pending_requests(self):
        for w in self.scroll_f.winfo_children(): w.destroy()
        try:
            self.db.ensure_connection()
            # Smart Logic: Only fetch members in the Leader's specific team
            sql = """SELECT lr.*, u.full_name FROM leave_requests lr 
                     JOIN users u ON lr.user_id = u.id 
                     WHERE u.team_id = (SELECT team_id FROM users WHERE id = %s) 
                     AND lr.status = 'Pending' 
                     ORDER BY lr.created_at DESC"""
            self.db.cursor.execute(sql, (self.user['id'],))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(self.scroll_f, text="No pending requests. ✅", 
                             font=("Segoe UI", 16), text_color=self.text_sub).pack(pady=100)
                return

            for r in rows:
                card = ctk.CTkFrame(self.scroll_f, fg_color=self.card_bg, 
                                    corner_radius=15, border_width=1, border_color=self.card_border)
                card.pack(fill="x", pady=10, padx=5)
                
                inner = ctk.CTkFrame(card, fg_color="transparent")
                inner.pack(fill="x", padx=25, pady=20)

                # Info Section
                info = ctk.CTkFrame(inner, fg_color="transparent")
                info.pack(side="left")
                
                ctk.CTkLabel(info, text=r['full_name'].upper(), font=("Segoe UI", 20, "bold"), 
                             text_color=self.text_main).pack(anchor="w")
                
                req_time = r['created_at'].strftime("%Y-%m-%d %I:%M %p") if r['created_at'] else "N/A"
                ctk.CTkLabel(info, text=f"🕒 Applied: {req_time}", font=("Segoe UI", 12), 
                             text_color="#F39C12").pack(anchor="w", pady=(2, 5))
                
                ctk.CTkLabel(info, text=f"{r['leave_type']} • {r['total_days']} Days", 
                             font=("Segoe UI", 14, "bold"), text_color="#3498DB").pack(anchor="w")

                # Action Buttons
                btn_box = ctk.CTkFrame(inner, fg_color="transparent")
                btn_box.pack(side="right")
                
                ctk.CTkButton(btn_box, text="APPROVE", width=100, height=38, fg_color="#27AE60", 
                              hover_color="#1E8449", font=("Segoe UI", 12, "bold"), corner_radius=8,
                              command=lambda x=r['id']: self.update_status(x, 'Approved')).pack(side="left", padx=5)
                
                ctk.CTkButton(btn_box, text="REJECT", width=100, height=38, fg_color="#E74C3C", 
                              hover_color="#C0392B", font=("Segoe UI", 12, "bold"), corner_radius=8,
                              command=lambda x=r['id']: self.update_status(x, 'Rejected')).pack(side="left", padx=5)
        except Exception as e: print(f"Load Error: {e}")

    def update_status(self, req_id, status):
        if not messagebox.askyesno("Confirm Action", f"Are you sure you want to {status.lower()} this?"):
            return
        try:
            self.db.ensure_connection()
            # Update the request
            self.db.cursor.execute("UPDATE leave_requests SET status = %s WHERE id = %s", (status, req_id))
            
            # Smart Backend: Fetch user_id for notification
            self.db.cursor.execute("SELECT user_id FROM leave_requests WHERE id = %s", (req_id,))
            target_user = self.db.cursor.fetchone()['user_id']

            msg = f"Leave request {status} by Team Leader."
            self.db.cursor.execute("""INSERT INTO notifications (user_id, message, is_read, created_at) 
                                     VALUES (%s, %s, 0, NOW())""", (target_user, msg))
            
            self.db.conn.commit()
            messagebox.showinfo("Success", f"Request {status.lower()}ed.")
            self.show_management_view()
        except Exception as e: messagebox.showerror("Error", str(e))

    def show_activity_history(self):
        self.clear_view()
        self.create_header("Activity History", "All past leave decisions", show_back=True)
        self.history_scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.history_scroll.pack(fill="both", expand=True)
        self.load_full_history()

    def load_full_history(self):
        """Displays processed history with original request time details"""
        try:
            self.db.cursor.execute("""SELECT lr.*, u.full_name FROM leave_requests lr 
                                     JOIN users u ON lr.user_id = u.id 
                                     WHERE u.team_id = %s AND lr.status != 'Pending' 
                                     ORDER BY lr.id DESC""", (self.user['team_id'],))
            rows = self.db.cursor.fetchall()
            
            for r in rows:
                row = ctk.CTkFrame(self.history_scroll, fg_color=self.card_bg, corner_radius=12, border_width=1, border_color=self.card_border)
                row.pack(fill="x", pady=6, padx=5)
                
                color = "#27AE60" if r['status'] == "Approved" else "#E74C3C"
                inner = ctk.CTkFrame(row, fg_color="transparent")
                inner.pack(fill="x", padx=20, pady=15)
                
                # Left Side Data
                left = ctk.CTkFrame(inner, fg_color="transparent")
                left.pack(side="left")
                
                ctk.CTkLabel(left, text=r['full_name'], font=("Segoe UI", 15, "bold")).pack(anchor="w")
                
                req_t = r['created_at'].strftime("%b %d, %Y at %I:%M %p") if r['created_at'] else "N/A"
                ctk.CTkLabel(left, text=f"Request Date: {req_t}", font=("Segoe UI", 11), text_color="#555555").pack(anchor="w")
                ctk.CTkLabel(left, text=f"{r['leave_type']} • {r['total_days']}d ({r['start_date']} to {r['end_date']})", 
                             font=("Segoe UI", 12), text_color="#888888").pack(anchor="w")
                
                # Right Side: Status Badge
                badge_f = ctk.CTkFrame(inner, fg_color=color, corner_radius=8)
                badge_f.pack(side="right")
                ctk.CTkLabel(badge_f, text=r['status'].upper(), font=("Segoe UI", 10, "bold"), text_color="white", padx=12, pady=4).pack()
                
        except Exception as e: print(f"History Load Error: {e}")	