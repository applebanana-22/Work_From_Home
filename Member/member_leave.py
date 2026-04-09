import customtkinter as ctk
from database import Database
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

class MemberLeave(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.show_list_view()

    def clear_view(self):
        for widget in self.container.winfo_children(): widget.destroy()

    def show_list_view(self):
        self.clear_view()
        header = ctk.CTkFrame(self.container, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="My Leave Requests", font=("Arial", 22, "bold")).pack(side="left")
        ctk.CTkButton(header, text="+ Apply for Leave", fg_color="#3498DB", command=self.show_form_view).pack(side="right")

        self.list_f = ctk.CTkScrollableFrame(self.container, label_text="Request History")
        self.list_f.pack(fill="both", expand=True, padx=30, pady=10)
        self.refresh_list()

    def show_form_view(self):
        self.clear_view()
        ctk.CTkButton(self.container, text="← Back", width=80, fg_color="#4A4A4A", command=self.show_list_view).pack(anchor="w", padx=30, pady=10)

        form_card = ctk.CTkFrame(self.container, corner_radius=12)
        form_card.pack(pady=10, padx=30, fill="x")
        inner = ctk.CTkFrame(form_card, fg_color="transparent")
        inner.pack(pady=30, padx=30, fill="x")

        # --- DATE RANGE TOGGLE ---
        self.use_range_var = ctk.BooleanVar(value=False)
        self.range_check = ctk.CTkSwitch(inner, text="Enable Date Range (Long Leave)", 
                                         variable=self.use_range_var, command=self.update_day_count)
        self.range_check.grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="w")

        # --- START & END DATES ---
        ctk.CTkLabel(inner, text="Start Date:").grid(row=1, column=0, sticky="w", padx=10)
        self.start_cal = DateEntry(inner, width=20, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.start_cal.grid(row=2, column=0, padx=10, pady=(0, 15), sticky="w")

        ctk.CTkLabel(inner, text="End Date:").grid(row=1, column=1, sticky="w", padx=10)
        self.end_cal = DateEntry(inner, width=20, background='#3498DB', date_pattern='yyyy-mm-dd')
        self.end_cal.grid(row=2, column=1, padx=10, pady=(0, 15), sticky="w")

        # --- LEAVE TYPE ---
        ctk.CTkLabel(inner, text="Leave Type:").grid(row=3, column=0, sticky="w", padx=10)
        self.type_var = ctk.StringVar(value="Sick Leave")
        ctk.CTkOptionMenu(inner, values=["Sick Leave", "Casual Leave", "Vacation"], 
                          variable=self.type_var, width=250).grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="w")

        # --- HALF DAY CHECKBOX ---
        self.add_half_var = ctk.BooleanVar(value=False)
        self.half_day_check = ctk.CTkCheckBox(inner, text="Add Half-Day (+0.5 days)", 
                                              variable=self.add_half_var, command=self.update_day_count)
        self.half_day_check.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="w")

        # --- DURATION DISPLAY ---
        self.count_lbl = ctk.CTkLabel(inner, text="Total Duration: 0 Day(s)", font=("Arial", 16, "bold"), text_color="gray")
        self.count_lbl.grid(row=6, column=0, sticky="w", padx=10, pady=(0, 15))

        # --- REASON ---
        ctk.CTkLabel(inner, text="Reason:").grid(row=7, column=0, sticky="w", padx=10)
        self.reason_txt = ctk.CTkTextbox(inner, height=80, width=500)
        self.reason_txt.grid(row=8, column=0, columnspan=2, padx=10, pady=(0, 20), sticky="w")

        # --- SUBMIT ---
        ctk.CTkButton(inner, text="Submit Request", fg_color="#10B981", height=40, width=200, 
                      command=self.submit_leave).grid(row=9, column=0, columnspan=2, pady=10)

        self.start_cal.bind("<<DateEntrySelected>>", lambda e: self.update_day_count())
        self.end_cal.bind("<<DateEntrySelected>>", lambda e: self.update_day_count())
        self.update_day_count()

    def update_day_count(self):
        total = 0.0
        # ၁ ရက်ပဲယူတာလား ဒါမှမဟုတ် ရက်ရှည် (Range) လား စစ်ဆေးပါတယ်
        if self.use_range_var.get():
            start = self.start_cal.get_date()
            end = self.end_cal.get_date()
            diff = (end - start).days + 1
            if diff > 0:
                total = float(diff)
        else:
            # Range ပိတ်ထားရင် Default ၁ ရက်လို့ ယူဆပါတယ် (Half-day မဟုတ်ရင်)
            total = 1.0 if not self.add_half_var.get() else 0.0

        if self.add_half_var.get():
            total += 0.5 if self.use_range_var.get() else 0.5
            
        if total == 0:
            self.count_lbl.configure(text="Total Duration: 0 Day(s)", text_color="gray")
        else:
            self.count_lbl.configure(text=f"Total Duration: {total} Day(s)", text_color="#3498DB")
        return total

    def submit_leave(self):
        total = self.update_day_count()
        if total <= 0:
            messagebox.showerror("Error", "Duration cannot be 0.")
            return
            
        l_type = self.type_var.get()
        start = self.start_cal.get_date().strftime('%Y-%m-%d')
        end = self.end_cal.get_date().strftime('%Y-%m-%d') if self.use_range_var.get() else start
        reason = self.reason_txt.get("1.0", "end-1c")
        is_hd = 1 if self.add_half_var.get() else 0

        try:
            sql = """INSERT INTO leave_requests (user_id, leave_type, start_date, end_date, reason, is_half_day, total_days) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            self.db.cursor.execute(sql, (self.user['id'], l_type, start, end, reason, is_hd, total))
            
            # ပြင်ဆင်ရန်: .connection အစား .conn ကို သုံးပါ
            self.db.conn.commit() 
            
            messagebox.showinfo("Success", f"Request Sent! Total: {total} Days")
            self.show_list_view()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def refresh_list(self):
        for w in self.list_f.winfo_children(): w.destroy()
        # total_days ကို တိုက်ရိုက်ယူသုံးလိုက်ပါပြီ
        query = "SELECT * FROM leave_requests WHERE user_id = %s ORDER BY id DESC"
        self.db.cursor.execute(query, (self.user['id'],))
        
        for r in self.db.cursor.fetchall():
            card = ctk.CTkFrame(self.list_f, fg_color=("#F0F0F0", "#252525"), corner_radius=8)
            card.pack(fill="x", pady=5, padx=10)
            
            days = r['total_days']
            info = f"📅 {r['start_date']} to {r['end_date']} ({days} Days)\nType: {r['leave_type']} | Reason: {r['reason']}"
            
            ctk.CTkLabel(card, text=info, justify="left").pack(side="left", padx=15, pady=10)
            status_color = {"Pending": "#F39C12", "Approved": "#27AE60", "Rejected": "#E74C3C"}
            ctk.CTkLabel(card, text=r['status'], text_color=status_color.get(r['status'], "gray"), 
                         font=("Arial", 12, "bold")).pack(side="right", padx=15)