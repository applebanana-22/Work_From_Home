import customtkinter as ctk
from database import Database
from tkinter import messagebox

class LeaderLeaveManage(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user
        
        # Header
        header = ctk.CTkLabel(self, text="Team Leave Requests", font=("Arial", 24, "bold"))
        header.pack(pady=20, padx=30, anchor="w")

        # --- Section 1: Pending Requests ---
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Pending Requests", height=300)
        self.list_frame.pack(fill="x", padx=30, pady=10)

        # --- Section 2: Request History ---
        self.history_label = ctk.CTkLabel(self, text="📜 Leave History (Approved/Rejected)", font=("Arial", 16, "bold"), text_color="gray")
        self.history_label.pack(anchor="w", padx=35, pady=(20, 0))

        self.history_frame = ctk.CTkScrollableFrame(self, label_text="History Logs", height=300)
        self.history_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.refresh_all_data()

    def refresh_all_data(self):
        """View နှစ်ခုလုံးကို Refresh လုပ်ခြင်း"""
        self.load_requests()
        self.load_history()

    def load_requests(self):
        """လက်ရှိ Pending ဖြစ်နေသော Request များကိုပြရန်"""
        for w in self.list_frame.winfo_children(): w.destroy()
        
        # Leader ရဲ့ Team ID နဲ့ကိုက်ညီတဲ့ Member တွေရဲ့ Pending Leave တွေကိုပဲ ပြပါမယ်
        query = """
            SELECT lr.*, u.full_name 
            FROM leave_requests lr
            JOIN users u ON lr.user_id = u.id
            WHERE lr.status = 'Pending' AND u.team_id = %s
            ORDER BY lr.id DESC
        """
        self.db.cursor.execute(query, (self.user.get('team_id'),))
        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(self.list_frame, text="No pending requests.", text_color="gray").pack(pady=20)
            return

        for r in rows:
            card = ctk.CTkFrame(self.list_frame, fg_color=("#F0F0F0", "#252525"))
            card.pack(fill="x", pady=5, padx=10)

            days = (r['end_date'] - r['start_date']).days + 1
            txt = f"👤 {r['full_name']} | {r['leave_type']}\n📅 {r['start_date']} to {r['end_date']} ({days} Days)\n📝 Reason: {r['reason']}"
            ctk.CTkLabel(card, text=txt, justify="left").pack(side="left", padx=15, pady=10)

            btn_f = ctk.CTkFrame(card, fg_color="transparent")
            btn_f.pack(side="right", padx=15)

            ctk.CTkButton(btn_f, text="Approve", fg_color="#27AE60", width=80, 
                          command=lambda i=r['id']: self.update_status(i, 'Approved')).pack(side="top", pady=2)
            ctk.CTkButton(btn_f, text="Reject", fg_color="#E74C3C", width=80,
                          command=lambda i=r['id']: self.update_status(i, 'Rejected')).pack(side="top", pady=2)

    def load_history(self):
        """Approve သို့မဟုတ် Reject လုပ်ပြီးသား History များကိုပြရန်"""
        for w in self.history_frame.winfo_children(): w.destroy()
        
        query = """
            SELECT lr.*, u.full_name 
            FROM leave_requests lr
            JOIN users u ON lr.user_id = u.id
            WHERE lr.status IN ('Approved', 'Rejected') AND u.team_id = %s
            ORDER BY lr.id DESC
        """
        self.db.cursor.execute(query, (self.user.get('team_id'),))
        rows = self.db.cursor.fetchall()

        if not rows:
            ctk.CTkLabel(self.history_frame, text="No history records.", text_color="gray").pack(pady=20)
            return

        for r in rows:
            card = ctk.CTkFrame(self.history_frame, fg_color=("#F9F9F9", "#1E1E1E"), corner_radius=8)
            card.pack(fill="x", pady=3, padx=10)

            status_color = "#27AE60" if r['status'] == 'Approved' else "#E74C3C"
            
            info = f"👤 {r['full_name']} | {r['leave_type']} | 📅 {r['start_date']}"
            ctk.CTkLabel(card, text=info, font=("Arial", 12)).pack(side="left", padx=15, pady=8)
            
            ctk.CTkLabel(card, text=r['status'], text_color=status_color, font=("Arial", 12, "bold")).pack(side="right", padx=15)

    def update_status(self, request_id, status):
        try:
            self.db.cursor.execute("UPDATE leave_requests SET status = %s WHERE id = %s", (status, request_id))
            self.db.conn.commit()
            messagebox.showinfo("Success", f"Request {status}")
            self.refresh_all_data() # Data အားလုံးကို Update ပြန်လုပ်ပါ
        except Exception as e:
            messagebox.showerror("Error", str(e))