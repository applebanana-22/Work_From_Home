import customtkinter as ctk
from Member.report_popup import ReportPopup  # We will create this next
from database import Database

class MemberReportFrame(ctk.CTkFrame):
    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.db = Database()
        self.configure(fg_color="transparent")

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(self.header, text="Daily Report History", 
                     font=("Arial", 24, "bold"), text_color="#00fbff").pack(side="left")

        self.add_btn = ctk.CTkButton(
            self.header, text="+ Add Daily Report", 
            fg_color="#1f538d", hover_color="#14375e",
            command=self.open_report_popup
        )
        self.add_btn.pack(side="right")

        # --- Report List (Table Header) ---
        self.list_header = ctk.CTkFrame(self, fg_color="#2b2b2b", height=40)
        self.list_header.pack(fill="x", padx=30, pady=(10, 0))
        
        ctk.CTkLabel(self.list_header, text="Date", width=150).pack(side="left", padx=10)
        ctk.CTkLabel(self.list_header, text="Category", width=150).pack(side="left", padx=10)
        ctk.CTkLabel(self.list_header, text="Description Summary").pack(side="left", padx=10)

        # --- Scrollable List ---
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=25, pady=10)

        self.refresh_reports()

    def refresh_reports(self):
        """Fetch all reports for this user and display them"""
        for w in self.scroll.winfo_children(): w.destroy()
        try:
            query = "SELECT * FROM daily_reports WHERE user_id = %s ORDER BY report_date DESC"
            self.db.cursor.execute(query, (self.user['id'],))
            reports = self.db.cursor.fetchall()

            for r in reports:
                row = ctk.CTkFrame(self.scroll, fg_color="#1e1e1e", height=45)
                row.pack(fill="x", pady=2)
                
                ctk.CTkLabel(row, text=str(r['report_date']), width=150, text_color="gray70").pack(side="left", padx=10)
                ctk.CTkLabel(row, text=r.get('category', 'General'), width=150, text_color="#3498DB").pack(side="left", padx=10)
                
                # Truncate description for the list view
                desc = r['tasks'][:60] + "..." if len(r['tasks']) > 60 else r['tasks']
                ctk.CTkLabel(row, text=desc, anchor="w").pack(side="left", padx=10, fill="x")
        except Exception as e:
            print(f"Report List Error: {e}")

    def open_report_popup(self):
        """Open the popup window"""
        popup = ReportPopup(self.user, on_save_callback=self.refresh_reports)
        popup.grab_set() # Focus on popup