import customtkinter as ctk
from database import Database
from tkinter import messagebox

class LeaderLeaveManage(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user
        
        header = ctk.CTkLabel(self, text="Team Leave Requests", font=("Arial", 24, "bold"))
        header.pack(pady=20, padx=30, anchor="w")

        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Pending Requests")
        self.list_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.load_requests()

    def load_requests(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        
        # Query to get leaves and user names
        query = """
            SELECT lr.*, u.full_name 
            FROM leave_requests lr
            JOIN users u ON lr.user_id = u.id
            WHERE lr.status = 'Pending'
            ORDER BY lr.id DESC
        """
        self.db.cursor.execute(query)
        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(self.list_frame, text="No pending requests.").pack(pady=20)
            return

        for r in rows:
            card = ctk.CTkFrame(self.list_frame, fg_color=("#F0F0F0", "#252525"))
            card.pack(fill="x", pady=5, padx=10)

            # Calculate days
            days = (r['end_date'] - r['start_date']).days + 1
            if r['is_half_day']: days += 0.5

            txt = f"👤 {r['full_name']} | {r['leave_type']}\n📅 {r['start_date']} to {r['end_date']} ({days} Days)\n📝 Reason: {r['reason']}"
            ctk.CTkLabel(card, text=txt, justify="left").pack(side="left", padx=15, pady=10)

            # Action Buttons
            btn_f = ctk.CTkFrame(card, fg_color="transparent")
            btn_f.pack(side="right", padx=15)

            ctk.CTkButton(btn_f, text="Approve", fg_color="#27AE60", width=80, 
                          command=lambda i=r['id']: self.update_status(i, 'Approved')).pack(side="top", pady=2)
            ctk.CTkButton(btn_f, text="Reject", fg_color="#E74C3C", width=80,
                          command=lambda i=r['id']: self.update_status(i, 'Rejected')).pack(side="top", pady=2)

    def update_status(self, request_id, status):
        try:
            self.db.cursor.execute("UPDATE leave_requests SET status = %s WHERE id = %s", (status, request_id))
            self.db.conn.commit()
            messagebox.showinfo("Success", f"Request {status}")
            self.load_requests()
        except Exception as e:
            messagebox.showerror("Error", str(e))