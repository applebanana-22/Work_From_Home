import customtkinter as ctk
from database import Database
from tkinter import messagebox, simpledialog  # simpledialog ကို ထည့်သွင်းထားသည်
from datetime import datetime

class MemberOvertime(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user  # Login ဝင်ထားသော Member data

        # --- Header ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Overtime Management", font=("Arial", 22, "bold")).pack(side="left")

        # --- Section 1: Leader Requests ---
        self.req_label = ctk.CTkLabel(self, text="🔔 Pending Leader Invites", font=("Arial", 14, "bold"), text_color="#3498DB")
        self.req_label.pack(anchor="w", padx=40)

        self.leader_req_f = ctk.CTkScrollableFrame(self, height=220, label_text="Incoming OT Requests")
        self.leader_req_f.pack(fill="x", padx=40, pady=10)

        # --- Section 2: Status & History ---
        self.history_label = ctk.CTkLabel(self, text="📜 My OT History", font=("Arial", 14, "bold"), text_color="gray")
        self.history_label.pack(anchor="w", padx=40, pady=(10, 0))

        self.history_f = ctk.CTkScrollableFrame(self, height=250)
        self.history_f.pack(fill="both", expand=True, padx=40, pady=10)

        self.refresh_all_data()

    def refresh_all_data(self):
        """View နှစ်ခုလုံးကို တစ်ပြိုင်နက် Refresh လုပ်ခြင်း"""
        self.refresh_leader_invites()
        self.refresh_history()

    def refresh_leader_invites(self):
        """Leader ထံမှလာသော Pending OT များကိုပြသရန်"""
        for w in self.leader_req_f.winfo_children(): w.destroy()
        
        query = """
            SELECT o.*, p.project_name 
            FROM overtime o 
            JOIN projects p ON o.project_id = p.id 
            WHERE TRIM(o.member_name) = TRIM(%s) AND o.status = 'Pending'
            ORDER BY o.created_at DESC
        """
        try:
            self.db.cursor.execute(query, (self.user['full_name'],))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(self.leader_req_f, text="No pending requests from leader.", text_color="gray").pack(pady=30)
                return

            for r in rows:
                card = ctk.CTkFrame(self.leader_req_f, fg_color=("#EBF5FB", "#1A252F"), corner_radius=10)
                card.pack(fill="x", pady=5, padx=5)

                txt = f"👤 From: Leader\n📁 Project: {r['project_name']}\n📅 Date: {r['ot_date']} | ⏳ {r['hours']} hrs\n📝 Tasks: {r['reason']}"
                ctk.CTkLabel(card, text=txt, justify="left", font=("Arial", 12)).pack(side="left", padx=15, pady=10)

                # Buttons
                btn_f = ctk.CTkFrame(card, fg_color="transparent")
                btn_f.pack(side="right", padx=15)

                # Accept ခလုတ်
                ctk.CTkButton(btn_f, text="Accept", width=80, fg_color="#27AE60", hover_color="#1E8449",
                              command=lambda id=r['id']: self.update_status(id, 'Accepted')).pack(side="left", padx=5)
                
                # Reject ခလုတ် (Reason တောင်းရန် function ကို ခေါ်မည်)
                ctk.CTkButton(btn_f, text="Reject", width=80, fg_color="#E74C3C", hover_color="#C0392B",
                              command=lambda id=r['id']: self.handle_reject(id)).pack(side="left")

        except Exception as e:
            print(f"Error loading invites: {e}")

    def handle_reject(self, ot_id):
        """Reject နှိပ်လျှင် အကြောင်းပြချက် တောင်းခံခြင်း"""
        # Popup box ဖြင့် အကြောင်းပြချက် တောင်းခြင်း
        reason = simpledialog.askstring("Reject Overtime", "အလုပ်မဆင်းနိုင်ရခြင်း အကြောင်းပြချက် ပေးပါရန်:", parent=self)
        
        if reason: # User က အကြောင်းပြချက် ရိုက်ထည့်ခဲ့မှသာ Update လုပ်မည်
            self.update_status(ot_id, 'Rejected', reason)
        elif reason == "": # စာမရိုက်ဘဲ OK နှိပ်လျှင်
            messagebox.showwarning("Warning", "Reason is required to reject.")
        # Cancel နှိပ်လျှင် ဘာမှမလုပ်ပါ

    def update_status(self, ot_id, new_status, member_note=None):
        """Status ကို Database မှာ Update လုပ်ခြင်း"""
        try:
            if member_note:
                # Reject ဖြစ်ပါက မူလ reason နောက်တွင် member ရဲ့ မှတ်ချက်ကိုပါ တွဲထည့်မည်
                sql = "UPDATE overtime SET status = %s, reason = CONCAT(reason, '\n[Rejected Reason: ', %s, ']') WHERE id = %s"
                self.db.cursor.execute(sql, (new_status, member_note, ot_id))
            else:
                self.db.cursor.execute("UPDATE overtime SET status = %s WHERE id = %s", (new_status, ot_id))
            
            self.db.conn.commit()
            messagebox.showinfo("Success", f"OT Request {new_status}")
            self.refresh_all_data() 
        except Exception as e:
            messagebox.showerror("Error", f"Could not update status: {e}")

    def refresh_history(self):
        """Accepted / Rejected / Approved စာရင်းများကို ပြသရန်"""
        for w in self.history_f.winfo_children(): w.destroy()
        
        query = """
            SELECT o.*, p.project_name 
            FROM overtime o 
            JOIN projects p ON o.project_id = p.id 
            WHERE TRIM(o.member_name) = TRIM(%s) AND o.status != 'Pending'
            ORDER BY o.created_at DESC
        """
        try:
            self.db.cursor.execute(query, (self.user['full_name'],))
            rows = self.db.cursor.fetchall()

            for r in rows:
                card = ctk.CTkFrame(self.history_f, fg_color=("#F9F9F9", "#252525"), corner_radius=8)
                card.pack(fill="x", pady=3, padx=5)

                status_colors = {"Accepted": "#27AE60", "Rejected": "#E74C3C", "Approved": "#2980B9"}
                s_color = status_colors.get(r['status'], "gray")

                info = f"📅 {r['ot_date']} | ⏳ {r['hours']}h | Proj: {r['project_name']}"
                ctk.CTkLabel(card, text=info, font=("Arial", 12)).pack(side="left", padx=15, pady=8)
                
                ctk.CTkLabel(card, text=r['status'], text_color=s_color, font=("Arial", 12, "bold")).pack(side="right", padx=15)

        except Exception as e:
            print(f"Error loading history: {e}")