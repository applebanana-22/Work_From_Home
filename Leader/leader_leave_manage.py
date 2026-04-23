import customtkinter as ctk
from database import Database
from tkinter import messagebox

# Class name ကို import error မတက်အောင် LeaderLeaveManage လို့ ပြောင်းထားပါတယ်
class LeaderLeaveManage(ctk.CTkFrame):
    def __init__(self, master, user, sidebar_ref=None):
        super().__init__(master, fg_color="#121212")
        self.db = Database()
        self.user = user
        self.sidebar_ref = sidebar_ref
        self.notif_window = None 
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=40, pady=30)
        
        self.show_management_view()

    def clear_view(self):
        for widget in self.container.winfo_children(): 
            widget.destroy()

    def create_header(self, title, subtitle):
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        left_side = ctk.CTkFrame(header, fg_color="transparent")
        left_side.pack(side="left")
        ctk.CTkLabel(left_side, text=title, font=("Segoe UI", 28, "bold"), text_color="#FFFFFF").pack(anchor="w")
        ctk.CTkLabel(left_side, text=subtitle, font=("Segoe UI", 13), text_color="#888888").pack(anchor="w")

        right_side = ctk.CTkFrame(header, fg_color="transparent")
        right_side.pack(side="right")

        self.notif_btn = ctk.CTkButton(right_side, text="🔔", width=40, height=40, 
                                       fg_color="#1E1E1E", hover_color="#2D2D2D",
                                       font=("Arial", 18), command=self.open_notifications)
        self.notif_btn.pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(right_side, text="🔄 Refresh Board", font=("Segoe UI", 13, "bold"), 
                      fg_color="#6264A7", hover_color="#4F5191", height=40, 
                      corner_radius=10, command=self.show_management_view).pack(side="right", padx=5)

    def show_management_view(self):
        self.clear_view()
        self.create_header("Team Management", "Review and respond to team leave requests")
        
        ctk.CTkLabel(self.container, text="⚡ PENDING APPROVALS", font=("Segoe UI", 12, "bold"), text_color="#3498DB").pack(anchor="w", pady=(10, 5))
        
        self.scroll_f = ctk.CTkScrollableFrame(self.container, fg_color="transparent", height=300)
        self.scroll_f.pack(fill="x", pady=5)
        self.load_pending_requests()

        ctk.CTkLabel(self.container, text="📋 RECENT DECISIONS", font=("Segoe UI", 12, "bold"), text_color="#888888").pack(anchor="w", pady=(20, 5))
        self.history_f = ctk.CTkScrollableFrame(self.container, fg_color="#1E1E1E", corner_radius=15, height=200)
        self.history_f.pack(fill="both", expand=True)
        self.load_history()

    def load_pending_requests(self):
        for w in self.scroll_f.winfo_children(): w.destroy()
        try:
            sql = """SELECT lr.*, u.full_name 
                     FROM leave_requests lr 
                     JOIN users u ON lr.user_id = u.id 
                     WHERE u.team_id = %s AND lr.status = 'Pending' 
                     ORDER BY lr.created_at DESC"""
            self.db.cursor.execute(sql, (self.user['team_id'],))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(self.scroll_f, text="No pending requests", font=("Segoe UI", 13), text_color="#555555").pack(pady=40)
                return

            for r in rows:
                card = ctk.CTkFrame(self.scroll_f, fg_color="#1E1E1E", corner_radius=12, border_width=1, border_color="#2D2D2D")
                card.pack(fill="x", pady=5, padx=2)
                
                inner = ctk.CTkFrame(card, fg_color="transparent")
                inner.pack(fill="x", padx=15, pady=12)

                txt_f = ctk.CTkFrame(inner, fg_color="transparent")
                txt_f.pack(side="left")
                ctk.CTkLabel(txt_f, text=f"{r['full_name']} (ID: E{r['user_id']})", font=("Segoe UI", 15, "bold")).pack(anchor="w")
                ctk.CTkLabel(txt_f, text=f"📅 {r['start_date']} to {r['end_date']} | {r['total_days']} Days", 
                             font=("Segoe UI", 12), text_color="#888888").pack(anchor="w")

                btn_f = ctk.CTkFrame(inner, fg_color="transparent")
                btn_f.pack(side="right")
                ctk.CTkButton(btn_f, text="Approve", width=90, fg_color="#27AE60", hover_color="#1E8449", 
                              command=lambda x=r['id']: self.update_status(x, 'Approved')).pack(side="left", padx=5)
                ctk.CTkButton(btn_f, text="Reject", width=90, fg_color="#E74C3C", hover_color="#C0392B", 
                              command=lambda x=r['id']: self.update_status(x, 'Rejected')).pack(side="left")
        except Exception as e: print(f"Load Error: {e}")

    def update_status(self, req_id, status):
        try:
            self.db.cursor.execute("UPDATE leave_requests SET status = %s WHERE id = %s", (status, req_id))
            msg = f"Your leave request has been {status}."
            self.db.cursor.execute("""INSERT INTO notifications (user_id, message, is_read, created_at) 
                                     SELECT user_id, %s, 0, NOW() FROM leave_requests WHERE id = %s""", (msg, req_id))
            self.db.conn.commit()
            messagebox.showinfo("Success", f"Request marked as {status}")
            self.show_management_view()
        except Exception as e: messagebox.showerror("Database Error", str(e))

    def load_history(self):
        try:
            self.db.cursor.execute("""SELECT lr.*, u.full_name FROM leave_requests lr 
                                     JOIN users u ON lr.user_id = u.id 
                                     WHERE u.team_id = %s AND lr.status != 'Pending' 
                                     ORDER BY lr.id DESC LIMIT 10""", (self.user['team_id'],))
            for r in self.db.cursor.fetchall():
                row = ctk.CTkFrame(self.history_f, fg_color="transparent")
                row.pack(fill="x", padx=15, pady=8)
                color = "#27AE60" if r['status'] == "Approved" else "#E74C3C"
                ctk.CTkLabel(row, text=f"{r['full_name']} — {r['leave_type']}", font=("Segoe UI", 13)).pack(side="left")
                ctk.CTkLabel(row, text=r['status'].upper(), font=("Segoe UI", 11, "bold"), text_color=color).pack(side="right")
        except: pass

    def open_notifications(self):
        if self.notif_window and self.notif_window.winfo_exists():
            self.notif_window.focus()
            return
        
        self.notif_window = ctk.CTkToplevel(self)
        self.notif_window.title("Leader Activity Feed")
        self.notif_window.geometry("400x500")
        self.notif_window.configure(fg_color="#121212")
        self.notif_window.attributes("-topmost", True)
        
        ctk.CTkLabel(self.notif_window, text="Activity Feed", font=("Segoe UI", 20, "bold")).pack(pady=20)
        scroll = ctk.CTkScrollableFrame(self.notif_window, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=15, pady=5)

        try:
            self.db.cursor.execute("SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC LIMIT 15", (self.user['id'],))
            notifs = self.db.cursor.fetchall()
            if not notifs:
                ctk.CTkLabel(scroll, text="No new activity", text_color="#555555").pack(pady=40)
            else:
                for n in notifs:
                    item = ctk.CTkFrame(scroll, fg_color="#1E1E1E", corner_radius=10)
                    item.pack(fill="x", pady=5)
                    ctk.CTkLabel(item, text=n['message'], font=("Segoe UI", 12), wraplength=330, justify="left", padx=15, pady=10).pack()
            
            self.db.cursor.execute("UPDATE notifications SET is_read = 1 WHERE user_id = %s", (self.user['id'],))
            self.db.conn.commit()
            if self.sidebar_ref:
                self.sidebar_ref.refresh_sidebar_badge()
        except: pass